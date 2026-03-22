def build_plan(graph, path):
    total_time = 0
    total_cost = 0
    total_distance = 0
    modes = []

    for i in range(len(path) - 1):
        current = path[i]
        nxt = path[i + 1]

        for edge in graph.get(current, []):
            if edge["to"] == nxt:
                total_time += edge["time"]
                total_cost += edge["cost"]
                total_distance += edge["distance"]
                modes.append(edge["mode"])
                break

    # Count mode switches
    switches = 0
    for i in range(len(modes) - 1):
        if modes[i] != modes[i + 1]:
            switches += 1

    plan = {
        "path": path,
        "total_time": total_time,
        "total_cost": total_cost,
        "total_distance": total_distance,
        "modes": modes,
        "transfers": len(path) - 1,
        "mode_switches": switches
    }

    return plan