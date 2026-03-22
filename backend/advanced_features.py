import random


# ---------------- SWITCHING PENALTY ---------------- #
def apply_switching_penalty(plan, penalty=50):
    """
    Add cost penalty when switching transport modes
    """

    extra_cost = plan["mode_switches"] * penalty
    plan["total_cost"] += extra_cost
    plan["switch_penalty"] = extra_cost

    return plan


# ---------------- DELAY SIMULATION ---------------- #
def apply_delay(plan):
    """
    Simulate random delays in travel time
    """

    delay = random.randint(0, 2)  # delay in hours
    plan["total_time"] += delay
    plan["delay_added"] = delay

    return plan


# ---------------- ROUND TRIP ---------------- #
def round_trip(graph, start, end):
    """
    Generate round trip plan
    """

    from search import dijkstra
    from planner import build_plan

    cost1, path1 = dijkstra(graph, start, end, "cost")
    cost2, path2 = dijkstra(graph, end, start, "cost")

    plan1 = build_plan(graph, path1)
    plan2 = build_plan(graph, path2)

    return {
        "forward": plan1,
        "return": plan2
    }


# ---------------- TOP 3 ROUTES ---------------- #
def get_top_routes(graph, start, end):
    """
    Get cheapest, fastest, shortest routes
    """

    from search import dijkstra
    from planner import build_plan

    routes = []

    # Cheapest
    cost, path = dijkstra(graph, start, end, "cost")
    routes.append(("cheapest", build_plan(graph, path)))

    # Fastest
    time, path = dijkstra(graph, start, end, "time")
    routes.append(("fastest", build_plan(graph, path)))

    # Shortest
    dist, path = dijkstra(graph, start, end, "distance")
    routes.append(("shortest", build_plan(graph, path)))

    return routes