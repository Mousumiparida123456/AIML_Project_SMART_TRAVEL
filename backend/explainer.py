def explain_plan(plan, preference):
    """
    Generate human-like explanation for selected route
    """

    explanation = ""

    if preference.lower() == "cheap":
        explanation = f"This route is chosen because it has the lowest cost ({plan['total_cost']})."

    elif preference.lower() == "fast":
        explanation = f"This route is selected as it takes the least time ({plan['total_time']} hours)."

    elif preference.lower() == "comfortable":
        explanation = f"This route is more comfortable with only {plan['mode_switches']} transport switches."

    elif preference.lower() == "balanced":
        explanation = f"This route provides a balance between cost ({plan['total_cost']}) and time ({plan['total_time']} hours)."

    else:
        explanation = f"This route is optimal based on selected preference."

    # Add extra reasoning about stops and modes
    explanation += f" It includes {len(plan['path']) - 1} stops and uses {', '.join(plan['modes'])} transport."

    return explanation