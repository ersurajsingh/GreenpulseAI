import json
import time
import random
import threading
import paho.mqtt.client as mqtt

MQTT_BROKER = 'mosquitto'
MQTT_PORT = 1883
TOPIC_WATER = '/greenpulse/raw/water'
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

def publish_sensor_data(client):
    while True:
        water_usage = round(random.uniform(0.1, 0.5), 3)
        temperature = round(random.uniform(20.0, 25.0), 2)
        timestamp = int(time.time() * 1e9)  # nanoseconds
        with job_lock:
            current_job = job_run_id
        payload = {
            'timestamp': timestamp,
            'raw_value': water_usage,
            'temperature_C': temperature,
            'job_run_id': current_job
        }
        client.publish(TOPIC_WATER, json.dumps(payload))
        print(f"Published: {payload}")
        time.sleep(5)

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    # Start the MQTT network loop in a background thread
    threading.Thread(target=client.loop_forever, daemon=True).start()
    # Start publishing sensor data
    publish_sensor_data(client)

if __name__ == "__main__":
    main()
