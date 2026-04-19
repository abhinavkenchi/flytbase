from core.models import Waypoint, Mission
from core.deconflict import predict_conflict
from core.visualize import plot_two_missions_with_conflict


def main():
    m1 = Mission(0, 20, 1, (Waypoint(0, 0), Waypoint(10, 10)))
    m2 = Mission(0, 20, 1, (Waypoint(0, 10), Waypoint(10, 0)))

    result = predict_conflict(m1, m2, safety_distance=1.5)

    print(result)

    plot_two_missions_with_conflict(
        m1,
        m2,
        result,
        "outputs/conflict_demo.png"
    )


if __name__ == "__main__":
    main()