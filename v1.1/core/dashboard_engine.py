from __future__ import annotations
import math
from typing import List, Dict, Tuple


def detect_live_conflicts(df, tick: int) -> Tuple[List[str], set, List[Dict]]:
    alerts = []
    risk_ids = set()
    conflicts = []

    for i in range(len(df)):
        for j in range(i + 1, len(df)):
            r1 = df.iloc[i]
            r2 = df.iloc[j]

            x1, y1 = float(r1["x"]), float(r1["y"])
            x2, y2 = float(r2["x"]), float(r2["y"])

            id1 = str(r1["id"])
            id2 = str(r2["id"])

            dist = math.dist((x1, y1), (x2, y2))

            if dist < 1.5:

                if dist < 0.6:
                    severity = "high"
                elif dist < 1.0:
                    severity = "medium"
                else:
                    severity = "low"

                alerts.append(
                    f"⚠ {id1} near {id2} | Distance {dist:.2f}"
                )

                risk_ids.add(id1)
                risk_ids.add(id2)

                conflicts.append({
                    "severity": severity,
                    "conflict_time": tick,
                    "drone_a": id1,
                    "drone_b": id2,
                    "distance": dist,
                })

    return alerts, risk_ids, conflicts