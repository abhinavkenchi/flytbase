# REQUIREMENTS.md

## FlytBase Robotics Assignment Repository – Complete Requirements

This repository contains **V1**, **V1.1**, and **V2** implementations of the FlytBase Robotics Assignment.

To run, review, test, and evaluate the project properly, use the following setup.

---

# Recommended System

* Ubuntu 22.04 / 24.04 (Recommended)
* Windows 10 / 11
* macOS
* Minimum 8 GB RAM
* Recommended 16 GB RAM
* Dual Core CPU minimum
* Quad Core recommended

---

# Core Software Required

* Python 3.10 or above
* pip
* Git (optional)
* Modern web browser

Check installation:

```bash
python3 --version
pip --version
git --version
```

---

# Complete Python Libraries Used

## External Libraries Required

* streamlit
* plotly
* pandas
* numpy
* pytest
* pyyaml
* matplotlib

Install all dependencies:

```bash
pip install streamlit plotly pandas numpy pytest pyyaml matplotlib
```

Or:

```bash
pip install -r requirements.txt
```

---

## Python Standard Libraries Used

(No installation required)

* sys
* os
* math
* time
* random
* threading
* pathlib
* dataclasses
* collections
* itertools
* statistics
* json
* typing
* copy

---

# Repository Structure

```text
v1/      Strategic Deconfliction System
v1.1/    Improved V1 with enhancements
v2/      Air Traffic Controller Edition
```

Inside V2:

```text
core/        Prediction, planner, controller logic
dashboard/   Streamlit UI modules
simulator/   Drone motion + telemetry simulation
scripts/     Launchers, demos, benchmarks, load tests
tests/       Unit and system tests
docs/        Reports and summaries
```

---

# Run Commands

## Run V1

```bash
python3 main.py
```

## Run V2 Controller

```bash
python3 -m scripts.run_v2
```

## Run Dashboard

```bash
streamlit run dashboard/app.py
```

## Run Tests

```bash
pytest
```

## Run Load Test

```bash
python3 -m scripts.load_test
```

---

# Browser Requirement (Dashboard)

Use any modern browser:

* Google Chrome (Recommended)
* Microsoft Edge
* Firefox

---

# Functional Review Checklist

Reviewer can inspect:

* Live drone simulation
* Controlled vs unknown drones
* Predictive conflict alerts
* Pause / reroute / resume logic
* Dashboard metrics
* Pre-flight mission review
* Replay / event logs
* Health monitoring
* Performance testing

---

# Setup Time

* Basic run: 5–10 minutes
* Full review: 15–20 minutes

---

# Not Required

This project does **NOT** require:

* GPU
* ROS
* Docker
* Database server
* Paid APIs
* Cloud hosting
* External drone hardware

---

# Troubleshooting

## If streamlit not found

```bash
pip install streamlit
```

## If pytest not found

```bash
pip install pytest
```

## If import errors occur

Run commands from repository root folder.

---

# Best Review Workflow

Use two terminals.

## Terminal 1

```bash
python3 -m scripts.run_v2
```

## Terminal 2

```bash
streamlit run dashboard/app.py
```

This runs backend controller + live dashboard together.

---

# Final Note

All dependencies are lightweight and the project can run on a standard laptop without specialized hardware.
