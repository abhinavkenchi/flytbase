import os

from core.models import Waypoint, Mission
from core.deconflict import predict_conflict, batch_check
from core.visualize import plot_two_missions_with_conflict, plot_mission_paths


os.makedirs("outputs", exist_ok=True)


def case_clear():
    m1 = Mission(
        0, 20, 1,
        (Waypoint(0, 0), Waypoint(10, 10))
    )

    m2 = Mission(
        15, 35, 1,
        (Waypoint(0, 10), Waypoint(10, 0))
    )

    result = predict_conflict(m1, m2, 1.5)

    plot_two_missions_with_conflict(
        m1, m2, result,
        "outputs/clear_case.png",
        show_plot=False
    )

    print("clear_case:", result)


def case_conflict():
    m1 = Mission(
        0, 20, 1,
        (Waypoint(0, 0), Waypoint(10, 10))
    )

    m2 = Mission(
        0, 20, 1,
        (Waypoint(0, 10), Waypoint(10, 0))
    )

    result = predict_conflict(m1, m2, 1.5)

    plot_two_missions_with_conflict(
        m1, m2, result,
        "outputs/conflict_case.png",
        show_plot=False
    )

    print("conflict_case:", result)


def case_near_miss():
    m1 = Mission(
        0, 20, 1,
        (Waypoint(0, 0), Waypoint(10, 10))
    )

    m2 = Mission(
        0, 20, 1,
        (Waypoint(0, 12), Waypoint(10, 2))
    )

    result = predict_conflict(m1, m2, 1.5)

    plot_two_missions_with_conflict(
        m1, m2, result,
        "outputs/near_collision_case.png",
        show_plot=False
    )

    print("near_collision_case:", result)


def case_multi_drone():
    primary = Mission(
        0, 20, 1,
        (Waypoint(0, 0), Waypoint(10, 10))
    )

    others = [
        Mission(0, 20, 1, (Waypoint(0, 10), Waypoint(10, 0))),
        Mission(10, 30, 1, (Waypoint(2, 0), Waypoint(2, 10))),
        Mission(0, 20, 1, (Waypoint(10, 2), Waypoint(0, 2))),
    ]

    labels = ["Primary", "Drone B", "Drone C", "Drone D"]

    plot_mission_paths(
        [primary] + others,
        labels=labels,
        title="Multiple Drone Airspace",
        save_path="outputs/multi_drone_case.png",
        show_plot=False
    )

    conflicts = batch_check(primary, others, 1.5)

    print("multi_drone_conflicts:", conflicts)


if __name__ == "__main__":
    case_clear()
    case_conflict()
    case_near_miss()
    case_multi_drone()

    print("\nAll scenario images generated in outputs/")
