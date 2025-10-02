# GreenPulseAI Proof of Concept

## Overview
GreenPulseAI is a prototype for real-time environmental impact monitoring of AI workloads. It simulates sensor data, job control, and power usage, and visualizes cumulative environmental metrics using MQTT, InfluxDB, and Grafana.


## Architecture

```
┌──────────────────────┐      MQTT      ┌───────────────┐      HTTP      ┌───────────────┐
│ mock_sensor_         │ ─────────────> │  Mosquitto    │ ─────────────> │   InfluxDB    │
│ publisher.py         │                │ (MQTT Broker) │                │ (Time Series  │
+──────────────────────+                +───────────────+                │   Database)   │
  │                                 ▲   ▲                          +───────────────+
  │                                 │   │                                 ▲
  ▼                                 │   │                                 │
+──────────────────────+      MQTT      ┌─┴───┴───┐      HTTP      +───────────────+
│   host_agent.py      │ ─────────────> │ data_    │ ─────────────>│   Grafana     │
+──────────────────────+                │ processor│                │ (Dashboard)   │
  │                                 +────────+                +───────────────+
  │                                 ▲
  ▼                                 │
+──────────────────────+      MQTT      ┌─┴────────┐
│   demo_run.py        │ ─────────────> │ green-   │
+──────────────────────+                │ pulse_job│
          +──────────+
+──────────────────────+
│ mock_power_reader.py │ (imported by host_agent, greenpulse_job)
+──────────────────────+
```

**Key Components:**
- `mock_sensor_publisher.py`: Simulates water flow and temperature sensors, publishing to MQTT.
- `host_agent.py`: Simulates host power readings, publishing to MQTT.
- `demo_run.py`: Simulates job execution, sending control signals via MQTT.
- `greenpulse_job.py`: Context manager for job lifecycle, publishing start/stop events.
- `data_processor.py`: Subscribes to all MQTT data/control topics, aggregates and writes cumulative metrics to InfluxDB.
- `InfluxDB`: Stores all time-series environmental data.
- `Grafana`: Visualizes metrics from InfluxDB.

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


## Approach, Methodology, and Impact

### Approach
- Modular simulation of sensors, jobs, and host agent using Python scripts.
- Real-time data aggregation and enrichment (CO2e, kWh, liters) in a central processor.
- All communication via MQTT for realistic, decoupled IoT-style architecture.
- Time-series storage and dashboarding for historical and live analysis.

### Methodology
- **Sensor Simulation**: Water flow and temperature are generated with smooth, realistic patterns.
- **Power Simulation**: Host power draw fluctuates based on job status.
- **Job Control**: Context manager triggers job start/stop, propagating state to all agents.
- **Data Processing**: Cumulative metrics are calculated per job and written to InfluxDB every second.
- **Visualization**: Grafana dashboards can be built to show job-level and system-level environmental impact.

### Impact
- Enables rapid prototyping and demonstration of environmental monitoring for AI workloads, without hardware.
- Provides a template for integrating real sensors and production workloads in the future.
- Supports data-driven sustainability decisions for compute infrastructure.

---

## Dashboard Example
You can create a Grafana dashboard with panels for:
- Cumulative kWh per job
- Cumulative CO2e per job
- Cumulative liters per job
- Current power draw
- Job status timeline

---

## Challenge Submission Deliverables

This repository contains all required deliverables for the GreenPulseAI PoC challenge:

- **A working prototype**: All scripts and infrastructure files are included and tested.
- **A detailed report**: See the Approach, Methodology, and Impact sections above.
- **Code and documentation**: All code is in this repository, with this README as documentation.
- **Dashboard/Visualization**: Grafana dashboard setup instructions are provided. Example panels: cumulative kWh, CO2e, liters, power draw, job status timeline.

---

## Notes
- All scripts use `localhost` for MQTT/InfluxDB. If running in Docker, use the container names as hostnames inside other containers.
- Ensure all Python dependencies are installed in your environment.

## License
MIT
