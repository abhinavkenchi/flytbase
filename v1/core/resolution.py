from typing import Dict, List


def suggest_resolution(conflict: Dict) -> List[str]:
    """
    Generate practical conflict-resolution actions
    based on severity, time, and spacing.

    Expected keys in conflict:
        severity
        conflict_time
        distance
        drone_id (optional)
    """

    severity = str(conflict.get("severity", "low")).lower()
    conflict_time = float(conflict.get("conflict_time", 0))
    distance = float(conflict.get("distance", 999))
    drone_id = conflict.get("drone_id", "conflicting drone")

    actions: List[str] = []

    # =====================================================
    # SEVERITY LOGIC
    # =====================================================
    if severity == "low":
        actions.append(
            f"Delay {drone_id} by 2 seconds."
        )
        actions.append(
            "Maintain route and continue monitoring spacing."
        )

    elif severity == "medium":
        actions.append(
            f"Delay {drone_id} by 5 seconds."
        )
        actions.append(
            "Reduce speed by 20% in conflict zone."
        )
        actions.append(
            "Temporary hold position until path clears."
        )

    elif severity == "high":
        actions.append(
            "Immediate reroute required."
        )
        actions.append(
            "Increase altitude separation by +5 m."
        )
        actions.append(
            f"Hold {drone_id} until safe corridor available."
        )
        actions.append(
            "Re-sequence crossing priority."
        )

    else:
        actions.append(
            "Unknown severity: switch to manual review."
        )

    # =====================================================
    # TIME BASED MODIFIER
    # =====================================================
    if conflict_time < 5:
        actions.append(
            "Conflict occurs early: hold takeoff clearance."
        )

    elif conflict_time > 20:
        actions.append(
            "Conflict occurs later: scheduled correction possible."
        )

    # =====================================================
    # DISTANCE MODIFIER
    # =====================================================
    if distance < 0.5:
        actions.append(
            "Critical spacing breach: emergency separation maneuver."
        )

    elif distance < 1.0:
        actions.append(
            "Very close proximity: apply immediate caution."
        )

    # =====================================================
    # REMOVE DUPLICATES
    # =====================================================
    unique_actions = []
    for action in actions:
        if action not in unique_actions:
            unique_actions.append(action)

    return unique_actions   