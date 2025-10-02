
# Refactored for cumulative metrics and job tracking
import json
import time
import threading
from collections import defaultdict
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point, WritePrecision

# MQTT settings
MQTT_BROKER = 'localhost'
MQTT_PORT = 1883
RAW_TOPIC = 'greenpulse/raw/#'
CONTROL_TOPIC = 'greenpulse/control'

# InfluxDB settings
INFLUXDB_URL = 'http://localhost:8086'
INFLUXDB_TOKEN = 'my-super-secret-token'
INFLUXDB_ORG = 'GreenPulseOrg'
INFLUXDB_BUCKET = 'greenpulse_metrics'

CO2E_FACTOR = 0.632  # kg/kWh

# State
job_metrics = defaultdict(lambda: {
    'cumulative_kwh': 0.0,
    'cumulative_liters': 0.0,
    'cumulative_co2e_kg': 0.0,
    'current_watts': 0.0,
    'last_update': None
})
current_job_id = 'idle'
lock = threading.Lock()

# InfluxDB client
influx_client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = influx_client.write_api(write_options=None)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Connected to MQTT broker.')
        client.subscribe([(RAW_TOPIC, 0), (CONTROL_TOPIC, 0)])
    else:
        print(f'Failed to connect, return code {rc}')

def on_message(client, userdata, msg):
    global current_job_id
    topic = msg.topic
    payload = msg.payload.decode()
    try:
        data = json.loads(payload)
    except Exception:
        print(f"Invalid JSON: {payload}")
        return
    with lock:
        if topic == CONTROL_TOPIC:
            # Handle job start/stop
            status = data.get('status')
            job_id = data.get('job_id', 'idle')
            if status == 'start':
                current_job_id = job_id
                print(f"Job started: {job_id}")
            elif status == 'end':
                current_job_id = 'idle'
                print(f"Job ended: {job_id}")
        elif topic.startswith('greenpulse/raw/'):
            job_id = data.get('job_id', current_job_id)
            if topic.endswith('power'):
                # Power in watts, 1s sample
                watts = data.get('watts')
                if watts is not None:
                    kwh = watts / 1000.0 / 3600.0  # 1s sample
                    job_metrics[job_id]['cumulative_kwh'] += kwh
                    job_metrics[job_id]['current_watts'] = watts
                    job_metrics[job_id]['cumulative_co2e_kg'] += kwh * CO2E_FACTOR
            elif topic.endswith('flow_temp'):
                # Water in LPM, 1s sample
                flow_lpm = data.get('flow_lpm')
                if flow_lpm is not None:
                    liters = flow_lpm / 60.0  # 1s sample
                    job_metrics[job_id]['cumulative_liters'] += liters
            # Write to InfluxDB
            point = (
                Point('environmental_footprint')
                .tag('job_id', job_id)
                .field('cumulative_kwh', job_metrics[job_id]['cumulative_kwh'])
                .field('cumulative_co2e_kg', job_metrics[job_id]['cumulative_co2e_kg'])
                .field('cumulative_liters', job_metrics[job_id]['cumulative_liters'])
                .field('current_watts', job_metrics[job_id]['current_watts'])
                .time(int(time.time() * 1e9), WritePrecision.NS)
            )
            write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
            print(f"[{job_id}] kWh={job_metrics[job_id]['cumulative_kwh']:.6f}, CO2e={job_metrics[job_id]['cumulative_co2e_kg']:.6f}, Liters={job_metrics[job_id]['cumulative_liters']:.3f}, Watts={job_metrics[job_id]['current_watts']}")

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()

if __name__ == "__main__":
    main()
