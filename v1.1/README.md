# UAV Strategic Deconfliction in Shared Airspace (V1.1)

## Overview

V1.1 is a modular prototype system designed to verify whether a drone mission is safe to execute in shared airspace before takeoff.

The system analyzes waypoint-based drone missions, predicts drone trajectories over time, detects spatial-temporal conflicts with other drones, and provides recommended resolution actions.

It also includes an interactive dashboard for live simulation, conflict monitoring, predictive alerts, and benchmarking tools.

---

# Core Objectives

- Validate a primary drone mission before execution
- Detect conflicts in both space and time
- Simulate multiple drones operating simultaneously
- Provide conflict explanations and mitigation suggestions
- Visualize drone movement and risk zones
- Demonstrate scalability with benchmark testing

---

# Key Features

## Strategic Deconfliction Engine

- Waypoint mission support
- Constant velocity trajectory modeling
- Mission time window validation
- Conflict detection using safety distance thresholds
- Severity classification:
  - Low
  - Medium
  - High

## Real-Time Dashboard

- Live drone playback simulation
- Animated airspace visualization
- Drone trails
- Conflict alerts
- Incident history log
- CSV report export
- Predictive alerts (future conflicts)

## Testing & Reliability

- Automated pytest suite
- Edge-case validation
- Runtime benchmarking

---

# Project Structure

```text
v1.1/
├── core/
│   ├── models.py
│   ├── trajectory.py
│   ├── deconflict.py
│   ├── resolution.py
│   ├── dashboard_engine.py
│   └── predictive.py
│
├── dashboard/
│   └── app.py
│
├── scripts/
│   └── benchmark.py
│
├── simulator/
│   └── telemetry.py
│
├── tests/
│
└── README.md
