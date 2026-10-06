"""Dijkstra's shortest-path algorithm for weighted transport networks."""

from heapq import heappush, heappop

# Sentinel returned when no route exists, so callers never have to
# handle a bare float('inf') leaking out of the algorithm.
NO_ROUTE = None


def graph_nodes(graph):
    """Return every node in the graph: dict keys plus edge targets.

    A node only ever reached as an edge target has no adjacency entry of its
    own, so it is absent from the keys. Both are legitimate nodes.
    """
    nodes = set(graph)
    for neighbours in graph.values():
        for neighbour, _ in neighbours:
            nodes.add(neighbour)
    return nodes


def validate_graph(graph):
    """Raise ValueError if the graph cannot be used by Dijkstra's algorithm."""
    for node, neighbours in graph.items():
        for neighbour, edge_cost in neighbours:
            if edge_cost is None or not isinstance(edge_cost, (int, float)):
                raise ValueError(
                    f"Edge {node!r} -> {neighbour!r} needs a numeric cost, "
                    f"got {edge_cost!r}."
                )
            if edge_cost < 0:
                raise ValueError(
                    f"Dijkstra's algorithm requires non-negative costs, but "
                    f"edge {node!r} -> {neighbour!r} has cost {edge_cost}."
                )


def dijkstra(graph, source, destination):
    """Return (total_cost, route) for the cheapest path from source to destination.

    graph format:
        {
            "Stop A": [("Stop B", cost), ("Stop C", cost)],
            ...
        }

    A stop only ever mentioned as an edge target does not need its own
    adjacency entry. Edge costs must be non-negative.

    Returns (cost, route) where route is the list of stops from source to
    destination inclusive. When no route exists, returns (NO_ROUTE, []).
    """
    nodes = graph_nodes(graph)
    if source not in nodes:
        raise ValueError(f"Source {source!r} is not a stop in the graph.")
    if destination not in nodes:
        raise ValueError(f"Destination {destination!r} is not a stop in the graph.")

    # Validate every edge up front, including edges on branches this
    # particular search never visits.
    validate_graph(graph)

    distances = {node: float("inf") for node in nodes}
    previous = {node: None for node in nodes}

    distances[source] = 0
    priority_queue = [(0, source)]

    while priority_queue:
        current_cost, current = heappop(priority_queue)

        if current_cost > distances[current]:
            continue

        if current == destination:
            break

        for neighbour, edge_cost in graph.get(current, ()):
            new_cost = current_cost + edge_cost

            if new_cost < distances.get(neighbour, float("inf")):
                distances[neighbour] = new_cost
                previous[neighbour] = current
                heappush(priority_queue, (new_cost, neighbour))

    if distances[destination] == float("inf"):
        return NO_ROUTE, []

    route = []
    current = destination
    while current is not None:
        route.append(current)
        current = previous[current]

    route.reverse()
    return distances[destination], route