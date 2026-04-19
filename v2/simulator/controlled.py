AIRSPACE_MIN = 0
AIRSPACE_MAX = 100


def clamp(value, low, high):
    return max(low, min(high, value))


def bounce_if_needed(drone):
    if drone["x"] <= AIRSPACE_MIN or drone["x"] >= AIRSPACE_MAX:
        drone["vx"] *= -1

    if drone["y"] <= AIRSPACE_MIN or drone["y"] >= AIRSPACE_MAX:
        drone["vy"] *= -1

    drone["x"] = clamp(drone["x"], AIRSPACE_MIN, AIRSPACE_MAX)
    drone["y"] = clamp(drone["y"], AIRSPACE_MIN, AIRSPACE_MAX)


def update_controlled(drone, dt):
    """
    Controlled drone:
    - obeys pause
    - linear motion
    - bounded airspace bounce
    """

    if drone["status"] == "paused":
        return

    drone["x"] += drone["vx"] * dt
    drone["y"] += drone["vy"] * dt

    bounce_if_needed(drone)