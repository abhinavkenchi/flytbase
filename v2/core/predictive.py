import math


SAFE_DISTANCE = 8.0
LOOKAHEAD_SECONDS = 15


def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def predict_pair(d1, d2):
    """
    Predict future conflict between two drones.

    Resume-support improvements:
    1. Paused drones use zero velocity.
    2. If both drones are paused, skip prediction.
    3. Helps paused drones gain safe_cycles and resume.
    """

    # both paused = no active future conflict worth alerting
    if d1["status"] == "paused" and d2["status"] == "paused":
        return None

    for t in range(1, LOOKAHEAD_SECONDS + 1):

        # paused drones do not move
        vx1 = 0 if d1["status"] == "paused" else d1["vx"]
        vy1 = 0 if d1["status"] == "paused" else d1["vy"]

        vx2 = 0 if d2["status"] == "paused" else d2["vx"]
        vy2 = 0 if d2["status"] == "paused" else d2["vy"]

        x1 = d1["x"] + vx1 * t
        y1 = d1["y"] + vy1 * t

        x2 = d2["x"] + vx2 * t
        y2 = d2["y"] + vy2 * t

        dist = distance(x1, y1, x2, y2)

        if dist < SAFE_DISTANCE:

            # if one drone paused, downgrade severity slightly
            paused_involved = (
                d1["status"] == "paused" or
                d2["status"] == "paused"
            )

            if t <= 3:
                severity = "HIGH"
            elif t <= 7:
                severity = "MEDIUM"
            else:
                severity = "LOW"

            # downgrade one level if paused drone involved
            if paused_involved:
                if severity == "HIGH":
                    severity = "MEDIUM"
                elif severity == "MEDIUM":
                    severity = "LOW"

            return {
                "a": d1["id"],
                "b": d2["id"],
                "eta": t,
                "severity": severity,
                "point": (
                    round((x1 + x2) / 2, 1),
                    round((y1 + y2) / 2, 1)
                ),
                "distance": round(dist, 2),
            }

    return None


def run_predictions(drones):
    alerts = []

    ids = list(drones.keys())

    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):

            d1 = drones[ids[i]]
            d2 = drones[ids[j]]

            alert = predict_pair(d1, d2)

            if alert:
                alerts.append(alert)

    return alerts