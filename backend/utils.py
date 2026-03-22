import csv

def load_graph(file_path):
    graph = {}

    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)

        for row in reader:
            source = row['source']
            destination = row['destination']

            edge = {
                "to": destination,
                "mode": row['mode'],
                "time": int(row['time']),
                "cost": int(row['cost']),
                "distance": int(row['distance'])
            }

            if source not in graph:
                graph[source] = []

            graph[source].append(edge)

            # reverse edge
            if destination not in graph:
                graph[destination] = []

            graph[destination].append({
                "to": source,
                "mode": row['mode'],
                "time": int(row['time']),
                "cost": int(row['cost']),
                "distance": int(row['distance'])
            })

    return graph