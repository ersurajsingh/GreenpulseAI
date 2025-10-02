import time
from greenpulse_job import Job

"""
Demo Run Script for GreenPulse PoC

Instructions:
1. Start the following scripts in separate terminals:
   - mock_sensor_publisher.py
   - host_agent.py
   - data_processor.py
2. Ensure your docker-compose services (MQTT, InfluxDB, Grafana) are running.
3. Run this script to simulate two jobs with idle periods.
4. View results in InfluxDB or Grafana dashboard.
"""

def main():
    print("Starting Job 1: Initial_Model_Train (10s)")
    with Job('Initial_Model_Train') as run_id:
        for i in range(10):
            print(f"Job 1 step {i+1}/10, run_id={run_id}")
            time.sleep(1)
    print("Idle for 5 seconds...")
    time.sleep(5)
    print("Starting Job 2: Hyperparameter_Tuning (15s)")
    with Job('Hyperparameter_Tuning') as run_id:
        for i in range(15):
            print(f"Job 2 step {i+1}/15, run_id={run_id}")
            time.sleep(1)
    print("Final idle for 5 seconds...")
    time.sleep(5)
    print("Demo complete.")

if __name__ == "__main__":
    main()
