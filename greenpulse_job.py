import time
import json
import uuid
import paho.mqtt.client as mqtt
from mock_power_reader import set_job_status

class Job:
    def __init__(self, job_name):
        self.job_name = job_name
        self.job_run_id = f"{job_name}_{int(time.time())}_{uuid.uuid4().hex[:6]}"
        self.mqtt_client = mqtt.Client()
        self.mqtt_broker = 'localhost'
        self.mqtt_port = 1883

    def __enter__(self):
        self.mqtt_client.connect(self.mqtt_broker, self.mqtt_port, 60)
        self.mqtt_client.loop_start()
        start_payload = {
            'status': 'start',
            'job_id': self.job_run_id,
            'timestamp': int(time.time())
        }
        self.mqtt_client.publish('greenpulse/control', json.dumps(start_payload))
        set_job_status(True, self.job_run_id)
        return self.job_run_id

    def __exit__(self, exc_type, exc_val, exc_tb):
        stop_payload = {
            'status': 'end',
            'job_id': self.job_run_id,
            'timestamp': int(time.time())
        }
        self.mqtt_client.publish('greenpulse/control', json.dumps(stop_payload))
        set_job_status(False, None)
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()
