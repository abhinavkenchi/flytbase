import time
import random

from core.predictive import run_predictions

# =====================================================
# SETTINGS
# =====================================================
MONITOR_INTERVAL = 1
SAFE_RESUME_CYCLES = 4
YIELD_SECONDS = 4
COOLDOWN_SECONDS = 4
SIDE_STEP_SPEED = 2.2
MAX_ACTIVE_YIELDS = 6


# =====================================================
# HELPERS
# =====================================================
def in_cooldown(drone_id, state):
    if drone_id not in state.cooldown:
        return False

    elapsed = time.time() - state.cooldown[drone_id]

    if elapsed >= COOLDOWN_SECONDS:
        state.cooldown.pop(drone_id, None)
        return False

    return True


def choose_yielder(a, b, drones):
    da = drones[a]
    db = drones[b]

    if da["type"] == "controlled" and db["type"] == "unknown":
        return a, b

    if da["type"] == "unknown" and db["type"] == "controlled":
        return b, a

    return random.choice([(a, b), (b, a)])


def apply_side_step(drone):
    direction = random.choice([-1, 1])

    drone["original_vx"] = drone["vx"]
    drone["original_vy"] = drone["vy"]

    drone["vy"] = SIDE_STEP_SPEED * direction


def restore_path(drone):
    if "original_vx" in drone:
        drone["vx"] = drone["original_vx"]
        drone["vy"] = drone["original_vy"]

        drone.pop("original_vx", None)
        drone.pop("original_vy", None)


# =====================================================
# MAIN CONTROLLER
# =====================================================
def resolve_conflicts(raw_alerts, state):
    used = set()

    for alert in raw_alerts:

        if len(state.paused) >= MAX_ACTIVE_YIELDS:
            break

        if alert["severity"] != "HIGH":
            continue

        if alert["eta"] > 2:
            continue

        d1 = alert["a"]
        d2 = alert["b"]

        if d1 in used or d2 in used:
            continue

        if d1 not in state.drones or d2 not in state.drones:
            continue

        yielder, mover = choose_yielder(d1, d2, state.drones)

        if in_cooldown(yielder, state):
            continue

        if yielder.startswith("C"):

            if yielder not in state.paused:
                state.pause_drone(yielder)

        mover_drone = state.drones[mover]

        if mover_drone["status"] != "paused":
            apply_side_step(mover_drone)

        used.add(d1)
        used.add(d2)


def auto_resume(state, raw_alerts):
    risky = set()

    for a in raw_alerts:
        if a["severity"] == "HIGH":
            risky.add(a["a"])
            risky.add(a["b"])

    for drone_id in list(state.paused.keys()):

        held = time.time() - state.pause_since.get(
            drone_id,
            time.time()
        )

        if drone_id in risky:
            state.safe_cycles[drone_id] = 0
            continue

        state.safe_cycles[drone_id] = (
            state.safe_cycles.get(drone_id, 0) + 1
        )

        if (
            state.safe_cycles[drone_id] >= SAFE_RESUME_CYCLES
            and held >= YIELD_SECONDS
        ):
            state.resume_drone(drone_id)
            state.cooldown[drone_id] = time.time()

    for drone_id, d in state.drones.items():
        if drone_id not in risky:
            restore_path(d)


def controller_step(state, raw_alerts):
    resolve_conflicts(raw_alerts, state)
    auto_resume(state, raw_alerts)


# =====================================================
# DEBUG CONSOLE
# =====================================================
def print_console(state, raw_alerts):
    print("\n=== LIVE AIRSPACE ===")
    print(f"Total drones : {len(state.drones)}")
    print(f"Paused       : {len(state.paused)}")
    print(f"Conflicts    : {len(raw_alerts)}")

    count = 0

    for drone_id, d in state.drones.items():
        print(
            f'{drone_id:<4} | '
            f'{d["type"]:<10} | '
            f'{d["status"]:<7} | '
            f'({d["x"]:>6.1f}, {d["y"]:>6.1f})'
        )

        count += 1
        if count >= 8:
            break