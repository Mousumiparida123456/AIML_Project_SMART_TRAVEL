import heapq

def dijkstra(graph, start, end, weight="cost"):
    pq = [(0, start, [])]
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
            next_node = edge["to"]
            next_weight = curr_weight + edge[weight]

            heapq.heappush(pq, (next_weight, next_node, path))

    return float("inf"), []