import json
import time
import random
import threading
import paho.mqtt.client as mqtt

MQTT_BROKER = 'mosquitto'
MQTT_PORT = 1883
TOPIC_POWER = '/greenpulse/raw/power'
TOPIC_START = '/greenpulse/control/start'
TOPIC_STOP = '/greenpulse/control/stop'

job_run_id = 'idle'
job_lock = threading.Lock()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Connected to MQTT broker.')
        client.subscribe([(TOPIC_START, 0), (TOPIC_STOP, 0)])
    else:
        print(f'Failed to connect, return code {rc}')

def on_message(client, userdata, msg):
    global job_run_id
    payload = msg.payload.decode()
    if msg.topic == TOPIC_START:
        try:
            data = json.loads(payload)
            with job_lock:
                job_run_id = data.get('job_run_id', 'idle')
            print(f"Job started: {job_run_id}")
        except Exception:
            print("Invalid start message payload.")
    elif msg.topic == TOPIC_STOP:
        with job_lock:
            job_run_id = 'idle'
        print("Job stopped.")

def publish_power_data(client):
    while True:
        with job_lock:
            current_job = job_run_id
        if current_job == 'idle':
            power = 100.0  # Idle mode: constant low power
        else:
            power = round(random.uniform(300.0, 600.0), 2)  # Active job: fluctuating high power
        timestamp = int(time.time() * 1e9)  # nanoseconds
        payload = {
            'timestamp': timestamp,
            'raw_value': power,
            'job_run_id': current_job
        }
        client.publish(TOPIC_POWER, json.dumps(payload))
        print(f"Published: {payload}")
        time.sleep(1)

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    # Start the MQTT network loop in a background thread
    threading.Thread(target=client.loop_forever, daemon=True).start()
    # Start publishing power data
    publish_power_data(client)

if __name__ == "__main__":
    main()
