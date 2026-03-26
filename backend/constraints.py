def check_constraints(plan, constraints):
    """
    Check if a plan satisfies given constraints
    """

    # Budget constraint
    if "max_cost" in constraints:
        try:
            max_cost = float(constraints["max_cost"])
        except (TypeError, ValueError):
            max_cost = None
        if max_cost is not None and plan["total_cost"] > max_cost:
            return False

    # Time constraint
    if "max_time" in constraints:
        try:
            max_time = float(constraints["max_time"])
        except (TypeError, ValueError):
            max_time = None
        if max_time is not None and plan["total_time"] > max_time:
            return False

    # Transfers constraint
    if "max_transfers" in constraints:
        try:
            max_transfers = int(constraints["max_transfers"])
        except (TypeError, ValueError):
            max_transfers = None
        if max_transfers is not None and plan["transfers"] > max_transfers:
            return False

    # Preferred transport mode(s) (allow-list for all segments)
    if "preferred_mode" in constraints and constraints["preferred_mode"]:
        preferred = constraints["preferred_mode"]
        if isinstance(preferred, str):
            allowed_modes = {preferred.strip().lower()}
        else:
            allowed_modes = {str(m).strip().lower() for m in preferred if str(m).strip()}

        if allowed_modes and any((m or "").strip().lower() not in allowed_modes for m in plan.get("modes", [])):
            return False

    # Emergency rerouting
    if "avoid_cities" in constraints:
        avoid = constraints["avoid_cities"]
        if isinstance(avoid, str):
            avoid_set = {c.strip().lower() for c in avoid.split(",") if c.strip()}
        else:
            avoid_set = {str(c).strip().lower() for c in (avoid or []) if str(c).strip()}

        for city in plan["path"]:
            if str(city).strip().lower() in avoid_set:
                return False

    # Time-of-day constraint (day/night)
    if "travel_time" in constraints and constraints["travel_time"]:
        desired = str(constraints["travel_time"]).strip().lower()
        if desired in {"day", "night"}:
            plan_times = [str(t).strip().lower() for t in plan.get("travel_times", []) if str(t).strip()]
            if plan_times and any(t != desired for t in plan_times):
                return False

    return True


def filter_plans(plans, constraints):
    """
    Filter valid plans based on constraints
    """
    valid_plans = []

    for plan in plans:
        if check_constraints(plan, constraints):
            valid_plans.append(plan)

    return valid_plans
