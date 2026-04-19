from __future__ import annotations

import pandas as pd
from simulator.telemetry import generate_drones
from core.dashboard_engine import detect_live_conflicts


def predict_future_conflicts(current_tick: int, horizon: int = 5):
    future_alerts = []

    for step in range(1, horizon + 1):
        tick = current_tick + step

        drones = generate_drones(tick)
        df = pd.DataFrame(drones)

        alerts, _, conflicts = detect_live_conflicts(df, tick)

        if alerts:
            future_alerts.append({
                "tick": tick,
                "count": len(alerts),
                "details": alerts[0]
            })

    return future_alerts