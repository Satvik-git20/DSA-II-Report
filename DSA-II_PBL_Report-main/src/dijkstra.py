from heapq import heappush, heappop


def dijkstra(graph, source, destination):
    """Return (minimum_cost, route) from source to destination.

    graph format:
        {
            "Stop A": [("Stop B", cost), ("Stop C", cost)],
            ...
        }

    Costs must be non-negative.
    """
    distances = {node: float("inf") for node in graph}
    previous = {node: None for node in graph}

    if source not in graph or destination not in graph:
        raise ValueError("Source and destination must exist in the graph.")

    distances[source] = 0
    priority_queue = [(0, source)]

    while priority_queue:
        current_cost, current = heappop(priority_queue)

        if current_cost != distances[current]:
            continue

        if current == destination:
            break

        for neighbor, edge_cost in graph[current]:
            if edge_cost < 0:
                raise ValueError("Dijkstra's algorithm requires non-negative costs.")

            new_cost = current_cost + edge_cost

            if new_cost < distances.get(neighbor, float("inf")):
                distances[neighbor] = new_cost
                previous[neighbor] = current
                heappush(priority_queue, (new_cost, neighbor))

    if distances[destination] == float("inf"):
        return float("inf"), []

    route = []
    current = destination
    while current is not None:
        route.append(current)
        current = previous[current]

    route.reverse()
    return distances[destination], route
