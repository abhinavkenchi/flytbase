# UAV Strategic Deconfliction System (V1)

A Python-based simulation and monitoring system for detecting and managing airspace conflicts between multiple UAVs (drones) operating in shared airspace.

This project models drone missions using waypoints, predicts trajectories over time, detects separation conflicts, classifies severity, visualizes drone movement, and provides recommended resolution actions through both CLI and live dashboard interfaces.

---

# Project Objective

To build a strategic deconfliction system that helps prevent mid-air conflicts between UAVs by forecasting trajectory intersections before collisions occur.

This simulates a simplified UAV Traffic Management (UTM) workflow.

---

# Key Features

## Core Engine

- Mission creation using waypoint-based routes
- Time-based trajectory prediction
- Multi-drone conflict detection
- Conflict severity classification:
  - Low
  - Medium
  - High
- Resolution recommendations

## Interfaces

- Command Line Interface (`main.py`)
- Live Streamlit Dashboard (`dashboard/app.py`)

## Dashboard Features

- Real-time drone simulation
- Playback timeline controls
- Start / Pause / Step controls
- Conflict alerts
- Recommended actions
- Drone status table
- Animated movement trails

## Testing

- Unit tests for models
- Conflict detection tests
- System-level tests

---

# Project Structure

```text
flytbase/
├── core/               # Core logic modules
│   ├── models.py
│   ├── trajectory.py
│   ├── deconflict.py
│   ├── resolution.py
│   └── visualize.py
│
├── dashboard/
│   └── app.py          # Streamlit dashboard
│
├── simulator/
│   ├── telemetry.py
│   └── scenarios.py
│
├── scripts/
│   ├── generate_scenarios.py
│   └── run_visual.py
│
├── tests/
│   ├── test_models.py
│   ├── test_deconflict.py
│   └── test_system.py
│
├── outputs/            # Generated images
├── main.py             # CLI application
├── pyproject.toml
└── README.md