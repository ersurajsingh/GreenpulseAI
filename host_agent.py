import time
import json
import paho.mqtt.client as mqtt
from mock_power_reader import read_watts, get_current_job_id

BROKER = 'localhost'
PORT = 1883
TOPIC = 'greenpulse/raw/power'
HOSTNAME = 'gpu-server-01'


def main():
    client = mqtt.Client()
    try:
        client.connect(BROKER, PORT, 60)
    except Exception as e:
        print(f"Failed to connect to MQTT broker: {e}")
        return
    while True:
        watts = read_watts()
        job_id = get_current_job_id()
        payload = {
            'host': HOSTNAME,
            'watts': watts,
            'job_id': job_id
        }
        try:
            client.publish(TOPIC, json.dumps(payload))
            print(f"Published: {payload}")
        except Exception as e:
            print(f"Publish error: {e}")
        time.sleep(1)

if __name__ == "__main__":
    main()
