import random


AIRSPACE_MIN = 0
AIRSPACE_MAX = 100
MAX_SPEED = 3.0
RANDOM_ACCEL = 0.30


def clamp(value, low, high):
    return max(low, min(high, value))


def limit_speed(drone):
    drone["vx"] = clamp(drone["vx"], -MAX_SPEED, MAX_SPEED)
    drone["vy"] = clamp(drone["vy"], -MAX_SPEED, MAX_SPEED)


def bounce_if_needed(drone):
    if drone["x"] <= AIRSPACE_MIN or drone["x"] >= AIRSPACE_MAX:
        drone["vx"] *= -1

    if drone["y"] <= AIRSPACE_MIN or drone["y"] >= AIRSPACE_MAX:
        drone["vy"] *= -1

    drone["x"] = clamp(drone["x"], AIRSPACE_MIN, AIRSPACE_MAX)
    drone["y"] = clamp(drone["y"], AIRSPACE_MIN, AIRSPACE_MAX)


def update_unknown(drone, dt):
    """
    Unknown drone:
    - semi-random motion
    - bounded speed
    - bounded airspace bounce
    - unpredictable but stable
    """

    # random steering
    drone["vx"] += random.uniform(-RANDOM_ACCEL, RANDOM_ACCEL)
    drone["vy"] += random.uniform(-RANDOM_ACCEL, RANDOM_ACCEL)

    # avoid absurd speeds
    limit_speed(drone)

    # move
    drone["x"] += drone["vx"] * dt
    drone["y"] += drone["vy"] * dt

    # keep inside sector
    bounce_if_needed(drone)