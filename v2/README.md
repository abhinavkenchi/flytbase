# FlytBase Robotics Assignment 2025 — V2  
## Air Traffic Controller Edition

A real-time UAV Traffic Management (UTM) prototype built to manage dense shared airspace with multiple drones, predictive conflict detection, controller intervention, pre-flight mission review, replay analytics, and operational health monitoring.

This project extends the V1 strategic deconfliction system into a live tactical airspace control platform.

---

# Problem Statement

As drone density increases, multiple operators may attempt to use the same airspace simultaneously. Static pre-flight planning alone is insufficient because real-world environments involve:

- dynamic route changes  
- telemetry uncertainty  
- non-cooperative aircraft  
- delayed updates  
- unexpected congestion  
- operator intervention requirements  

The goal of V2 is to simulate an **Air Traffic Controller for drones** capable of managing active traffic safely in real time.

---

# Core Features

## 1. Real-Time Airspace Simulation

- 30+ simultaneous drones
- Controlled cooperative drones
- Unknown / unpredictable drones
- Continuous motion updates

## 2. Predictive Conflict Detection

The system forecasts future trajectory intersections using velocity-based lookahead simulation.

Outputs include:

- ETA to conflict
- Severity levels (HIGH / MEDIUM / LOW)
- Conflict pairs
- Predicted collision zones

## 3. Tactical Deconfliction Controller

Instead of pausing all aircraft, the controller uses cooperative conflict resolution:

- one drone yields
- another reroutes vertically (up/down sidestep)
- automatic resume after safe clearance
- cooldown to avoid oscillations

## 4. Live Dashboard

Streamlit-based ATC dashboard provides:

- live airspace map
- controlled vs unknown traffic
- paused drones
- conflict alerts
- fleet metrics
- system health panels

## 5. Pre-Flight Mission Review

Incoming missions can be assessed before takeoff:

- approve
- reject
- delay
- risk prioritization

## 6. Incident Replay

Replay recent events for controller review:

- paused drones
- reroutes
- cleared conflicts

## 7. Performance / Load Testing

Scripts included for scalability testing under higher drone counts.

---

# Project Structure

```text
core/        -> prediction, controller, planner, replay logic
dashboard/   -> UI modules and operator dashboard
simulator/   -> drone motion models and spawning
scripts/     -> launchers, demos, benchmarks, load tests
tests/       -> validation test cases
docs/        -> architecture and reflections