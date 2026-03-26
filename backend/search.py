import heapq


def dijkstra(graph, start, end, weight="cost", *, avoid_cities=None, travel_time=None, allowed_modes=None):
    """
    Dijkstra shortest-path with optional filters.

    - avoid_cities: iterable of city names to skip (case-insensitive)
    - travel_time: "day" or "night" (filters edges with mismatched travel_time when present)
    - allowed_modes: iterable of transport modes (e.g. {"train","bus"}) to allow
    """
    if not start or not end:
        return float("inf"), []

    start = start.strip()
    end = end.strip()

    avoid_set = {c.strip().lower() for c in (avoid_cities or []) if str(c).strip()}
    if start.lower() in avoid_set or end.lower() in avoid_set:
        return float("inf"), []

    travel_time = travel_time.strip().lower() if isinstance(travel_time, str) and travel_time.strip() else None
    allowed_modes_set = {m.strip().lower() for m in (allowed_modes or []) if str(m).strip()} or None

    pq = [(0.0, start, [])]
    visited = set()

    while pq:
        curr_weight, node, path = heapq.heappop(pq)

        if node in visited:
            continue

        path = path + [node]
        visited.add(node)

        if node == end:
            return curr_weight, path

        for edge in graph.get(node, []):
            next_node = edge.get("to")
            if not next_node:
                continue

            if next_node.strip().lower() in avoid_set:
                continue

            edge_mode = (edge.get("mode") or "").strip().lower()
            if allowed_modes_set is not None and edge_mode not in allowed_modes_set:
                continue

            edge_travel_time = (edge.get("travel_time") or "").strip().lower()
            if travel_time and edge_travel_time and edge_travel_time != travel_time:
                continue

            edge_weight = float(edge.get(weight, 0.0) or 0.0)
            next_weight = curr_weight + edge_weight

            heapq.heappush(pq, (next_weight, next_node, path))

    return float("inf"), []
