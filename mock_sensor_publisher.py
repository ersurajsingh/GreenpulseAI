import time
import math
import json
import random
import paho.mqtt.client as mqtt

BROKER = 'localhost'
PORT = 1883
TOPIC = 'greenpulse/raw/flow_temp'
HOSTNAME = 'gpu-server-01'

# Smoothly fluctuating flow (LPM) using sine wave
FLOW_MIN = 0.1
FLOW_MAX = 2.5
FLOW_PERIOD = 60  # seconds for a full sine cycle

# Temperature ramp: 25.0 to 35.0 over 5 minutes, then back
TEMP_MIN = 25.0
TEMP_MAX = 35.0
TEMP_PERIOD = 300  # 5 minutes up, 5 down


def get_flow_lpm(t):
    # Sine wave between FLOW_MIN and FLOW_MAX
    amplitude = (FLOW_MAX - FLOW_MIN) / 2
    offset = (FLOW_MAX + FLOW_MIN) / 2
    return round(offset + amplitude * math.sin(2 * math.pi * t / FLOW_PERIOD), 3)

def get_temp_c(t):
    # Triangle wave for temperature
    cycle = (t // TEMP_PERIOD) % 2
    pos = (t % TEMP_PERIOD) / TEMP_PERIOD
    if cycle == 0:
        temp = TEMP_MIN + (TEMP_MAX - TEMP_MIN) * pos
    else:
        temp = TEMP_MAX - (TEMP_MAX - TEMP_MIN) * pos
    return round(temp, 2)

def main():
    client = mqtt.Client()
    try:
        client.connect(BROKER, PORT, 60)
    except Exception as e:
        print(f"Failed to connect to MQTT broker: {e}")
        return
    t0 = time.time()
    while True:
        t = time.time() - t0
        flow_lpm = get_flow_lpm(t)
        temp_c = get_temp_c(t)
        payload = {
            'host': HOSTNAME,
            'flow_lpm': flow_lpm,
            'temp_c': temp_c
        }
        try:
            client.publish(TOPIC, json.dumps(payload))
            print(f"Published: {payload}")
        except Exception as e:
            print(f"Publish error: {e}")
        time.sleep(1)

if __name__ == "__main__":
    main()
