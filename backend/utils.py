import csv


def _to_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return float(default)


def load_graph(file_path):
    """
    Load routes CSV into an adjacency-list graph.

    Each edge contains:
      - to, mode, time, cost, distance, travel_time
    """
    graph = {}

    with open(str(file_path), "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            source = (row.get("source") or "").strip()
            destination = (row.get("destination") or "").strip()
            if not source or not destination:
                continue

            mode = (row.get("mode") or "").strip().lower()
            travel_time = (row.get("travel_time") or "").strip().lower()

            edge = {
                "to": destination,
                "mode": mode,
                "time": _to_float(row.get("time")),
                "cost": _to_float(row.get("cost")),
                "distance": _to_float(row.get("distance")),
                "travel_time": travel_time,
            }

            graph.setdefault(source, []).append(edge)

            # Add reverse edge (treat routes as bidirectional)
            graph.setdefault(destination, []).append(
                {
                    "to": source,
                    "mode": mode,
                    "time": edge["time"],
                    "cost": edge["cost"],
                    "distance": edge["distance"],
                    "travel_time": travel_time,
                }
            )

    return graph
