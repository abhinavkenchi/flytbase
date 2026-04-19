import threading
import time

from core.runtime_state import RuntimeState
from core.controller import controller_step, MONITOR_INTERVAL, print_console
from core.predictive import run_predictions
from simulator.spawner import spawn_drones
from simulator.engine import SimEngine

# =====================================================
# MONITOR LOOP
# =====================================================
def monitor(state):
    while True:
        time.sleep(MONITOR_INTERVAL)

        raw_alerts = run_predictions(state.drones)

        controller_step(state, raw_alerts)

        print_console(state, raw_alerts)

# =====================================================
# MAIN
# =====================================================
def main():
    state = RuntimeState()

    drones = spawn_drones(30)

    engine = SimEngine(drones, state)

    sim_thread = threading.Thread(
        target=engine.run,
        daemon=True
    )
    sim_thread.start()

    print("V2.7 Cooperative ATC Started...")

    monitor(state)

if __name__ == "__main__":
    main()
