def check_constraints(plan, constraints):
    """
    Check if a plan satisfies given constraints
    """

    # Budget constraint
    if "max_cost" in constraints:
        if plan["total_cost"] > constraints["max_cost"]:
            return False

    # Time constraint
    if "max_time" in constraints:
        if plan["total_time"] > constraints["max_time"]:
            return False

    # Transfers constraint
    if "max_transfers" in constraints:
        if plan["transfers"] > constraints["max_transfers"]:
            return False

    # Preferred transport mode
    if "preferred_mode" in constraints:
        if constraints["preferred_mode"] not in plan["modes"]:
            return False

    # 🚨 Emergency rerouting
    if "avoid_cities" in constraints:
        for city in plan["path"]:
            if city in constraints["avoid_cities"]:
                return False

    # 🌙 Time-of-day constraint
    if "travel_time" in constraints:
        if constraints["travel_time"] == "night":
            if "bus" in plan["modes"]:
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