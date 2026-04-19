from typing import List, Tuple, Dict

from core.models import Waypoint, Mission
from core.deconflict import predict_conflict
from core.resolution import suggest_resolution


# =====================================================
# INPUT HELPERS
# =====================================================
def get_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid number. Try again.")


def get_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid integer. Try again.")


# =====================================================
# BUILD PRIMARY USER MISSION
# =====================================================
def build_user_mission() -> Mission:
    print("\n--- Enter Primary Mission ---")

    start_time = get_float("Start time: ")
    end_time = get_float("End time: ")
    velocity = get_float("Velocity: ")

    count = get_int("Number of waypoints: ")

    if count < 2:
        raise ValueError("Need at least 2 waypoints.")

    points = []

    for i in range(count):
        x = get_float(f"Waypoint {i+1} X: ")
        y = get_float(f"Waypoint {i+1} Y: ")
        points.append(Waypoint(x, y))

    return Mission(
        start_time,
        end_time,
        velocity,
        tuple(points)
    )


# =====================================================
# PRESET TRAFFIC MISSIONS
# =====================================================
def load_other_missions() -> List[Tuple[str, Mission]]:
    return [
        (
            "Drone_1",
            Mission(
                0, 20, 1,
                (
                    Waypoint(0, 10),
                    Waypoint(10, 0),
                )
            )
        ),
        (
            "Drone_2",
            Mission(
                5, 25, 1,
                (
                    Waypoint(2, 0),
                    Waypoint(8, 10),
                )
            )
        ),
        (
            "Drone_3",
            Mission(
                0, 30, 1,
                (
                    Waypoint(10, 10),
                    Waypoint(15, 15),
                )
            )
        ),
    ]


# =====================================================
# CHECK CONFLICTS
# =====================================================
def check_named_conflicts(
    primary: Mission,
    traffic: List[Tuple[str, Mission]],
    safety_distance: float = 1.5
) -> List[Dict]:

    results = []

    for drone_id, mission in traffic:

        result = predict_conflict(
            primary,
            mission,
            safety_distance
        )

        if result["status"] == "conflict":
            result["drone_id"] = drone_id
            results.append(result)

    return results


# =====================================================
# PRINT RESULTS
# =====================================================
def print_results(results: List[Dict]) -> None:

    if not results:
        print("\nMISSION CLEAR ✅")
        print("No conflicts detected.")
        print("Recommendation: Proceed with mission.")
        return

    print("\nCONFLICTS DETECTED ⚠")

    for i, r in enumerate(results, start=1):

        print(f"\nConflict {i}")
        print(f"Drone      : {r['drone_id']}")
        print(f"Time       : {r['conflict_time']:.2f} sec")
        print(f"Distance   : {r['distance']:.2f}")
        print(f"Severity   : {r['severity']}")
        print(f"Position A : {r['position_a']}")
        print(f"Position B : {r['position_b']}")

        print("Recommended Actions:")

        actions = suggest_resolution(r)

        for act in actions:
            print(f" - {act}")


# =====================================================
# MAIN
# =====================================================
def main() -> None:

    print("UAV Strategic Deconfliction System")

    try:
        primary = build_user_mission()

    except ValueError as err:

        print("\nINVALID MISSION ❌")
        print(err)

        print("\nSuggestions:")
        print("- Increase mission end time")
        print("- Increase velocity")
        print("- Reduce route distance")
        print("- Add fewer waypoints")

        return

    traffic = load_other_missions()

    results = check_named_conflicts(
        primary,
        traffic,
        safety_distance=1.5
    )

    print_results(results)


# =====================================================
# ENTRY
# =====================================================
if __name__ == "__main__":
    main()  