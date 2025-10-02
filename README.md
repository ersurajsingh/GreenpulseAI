# GreenPulseAI Proof of Concept

## Overview
GreenPulseAI is a prototype for real-time environmental impact monitoring of AI workloads. It simulates sensor data, job control, and power usage, and visualizes cumulative environmental metrics using MQTT, InfluxDB, and Grafana.

## Architecture
- **MQTT Broker (Mosquitto):** Message bus for all sensor and control data.
- **InfluxDB:** Time-series database for storing environmental metrics.
- **Grafana:** Dashboard for visualization.
- **Python Scripts:** Simulate sensors, jobs, host agent, and data processing.

## Setup Instructions

### 1. Prerequisites
- Docker & Docker Compose
- Python 3.8+
- Install Python dependencies:
  ```sh
  pip install paho-mqtt influxdb-client
  ```

### 2. Start Infrastructure
```
docker-compose up -d
```
This launches Mosquitto (MQTT), InfluxDB (with org `GreenPulseOrg`, user `suraj`, bucket `greenpulse_metrics`), and Grafana.

### 3. Run the Simulation Scripts
Open separate terminals for each script:

```sh
python mock_sensor_publisher.py
python host_agent.py
python data_processor.py
```

### 4. Run the Demo
In a new terminal:
```sh
python demo_run.py
```
This will simulate two jobs with idle periods, triggering the full data pipeline.

### 5. View the Dashboard
- Access Grafana at: http://localhost:3000
- Default login: `admin` / `admin`
- Add InfluxDB as a data source (URL: `http://influxdb:8086`, org: `GreenPulseOrg`, bucket: `greenpulse_metrics`, token: `my-super-secret-token`).
- Create dashboards to visualize `environmental_footprint` measurement.

## File Descriptions
- `docker-compose.yml` — Infrastructure setup
- `mock_sensor_publisher.py` — Simulates water/temperature sensor
- `mock_power_reader.py` — Power simulation logic
- `greenpulse_job.py` — Job context manager for control
- `host_agent.py` — Publishes simulated power readings
- `data_processor.py` — Aggregates and stores metrics
- `demo_run.py` — Runs demo jobs and prints progress

## Methodology & Impact
- **Approach:** Modular simulation of sensors, jobs, and host agent, with real-time data aggregation and visualization.
- **Impact:** Enables rapid prototyping and demonstration of environmental monitoring for AI workloads, without hardware.

## Notes
- All scripts use `localhost` for MQTT/InfluxDB. If running in Docker, use the container names as hostnames inside other containers.
- Ensure all Python dependencies are installed in your environment.

## License
MIT
