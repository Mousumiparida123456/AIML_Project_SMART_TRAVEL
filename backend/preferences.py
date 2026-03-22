def choose_best_plan(plans, preference="cheap", top_n=3):

    if not plans:
        return None, []

    # ✅ REMOVE DUPLICATES (based on path)
    unique = []
    seen_paths = set()

    for plan in plans:
        path_tuple = tuple(plan["path"])
        if path_tuple not in seen_paths:
            seen_paths.add(path_tuple)
            unique.append(plan)

    # 🔽 SELECT SORT KEY
    if preference == "cheap":
        key_func = lambda x: x["total_cost"]

    elif preference == "fast":
        key_func = lambda x: x["total_time"]

    elif preference == "short":
        key_func = lambda x: x["total_distance"]

    elif preference == "comfortable":
        key_func = lambda x: x["mode_switches"]

    elif preference == "balanced":
        key_func = lambda x: x["total_cost"] + x["total_time"]

    else:
        key_func = lambda x: x["total_cost"]

    # 🔽 SORT UNIQUE PLANS
    ranked_plans = sorted(unique, key=key_func)

    best_plan = ranked_plans[0]
    top_plans = ranked_plans[:top_n]

    return best_plan, top_plans