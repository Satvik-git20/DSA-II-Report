"""Build a transport network and compare shortest-path techniques."""

import argparse
import csv
import sys
from collections import deque
from heapq import heappop, heappush
from pathlib import Path

# Allow `python src/main.py` as well as `python -m src.main`.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dijkstra import NO_ROUTE, dijkstra  # noqa: E402

DEFAULT_DATA = Path(__file__).resolve().parent.parent / "data" / "sample_routes.csv"
HEADER_NAMES = {"source", "from", "origin", "stop"}


def load_transport_graph(csv_path):
    """Read an undirected weighted graph from a source,destination,cost CSV.

    An optional `source,destination,cost` header row is skipped. Every other
    row becomes two directed edges, since a route can be travelled in either
    direction.
    """
    graph = {}
    with open(csv_path, newline="", encoding="utf-8") as handle:
        for row_number, row in enumerate(csv.reader(handle), start=1):
            if not row or not row[0].strip() or row[0].strip().startswith("#"):
                continue
            source, destination, raw_cost = (field.strip() for field in row)
            if source.lower() in HEADER_NAMES and not raw_cost.lstrip("-").replace(
                    ".", "", 1).isdigit():
                continue  # header row
            if len(row) != 3:
                raise ValueError(
                    f"{csv_path}:{row_number} needs 3 fields "
                    f"(source, destination, cost), got {len(row)}."
                )
            try:
                cost = float(raw_cost)
            except ValueError:
                raise ValueError(
                    f"{csv_path}:{row_number} has a non-numeric cost {raw_cost!r}."
                ) from None
            graph.setdefault(source, []).append((destination, cost))
            graph.setdefault(destination, []).append((source, cost))
    if not graph:
        raise ValueError(f"{csv_path} contains no routes.")
    return graph


def build_transport_graph():
    # Example route costs. These are sample values for demonstration only.
    return {
        "Central Station": [
            ("City Mall", 4),
            ("University", 6),
        ],
        "City Mall": [
            ("Central Station", 4),
            ("Bus Depot", 5),
            ("Market", 3),
        ],
        "University": [
            ("Central Station", 6),
            ("Market", 2),
            ("Airport", 9),
        ],
        "Bus Depot": [
            ("City Mall", 5),
            ("Airport", 7),
        ],
        "Market": [
            ("City Mall", 3),
            ("University", 2),
            ("Airport", 6),
        ],
        "Airport": [
            ("University", 9),
            ("Bus Depot", 7),
            ("Market", 6),
        ],
    }


def astar(graph, source, destination, heuristic):
    """Return (total_cost, route) using A* with the supplied admissible heuristic.

    heuristic(node) estimates the remaining cost from node to destination and
    must never overestimate it, or the returned route may be suboptimal.
    """
    nodes = set(graph)
    for neighbours in graph.values():
        for neighbour, _ in neighbours:
            nodes.add(neighbour)
    if source not in nodes or destination not in nodes:
        raise ValueError("Source and destination must exist in the graph.")

    distances = {node: float("inf") for node in nodes}
    previous = {node: None for node in nodes}
    distances[source] = 0
    # Queue on the f-score: cost so far plus the heuristic estimate.
    queue = [(heuristic(source), 0, source)]

    while queue:
        _, current_cost, current = heappop(queue)

        if current_cost > distances[current]:
            continue
        if current == destination:
            break

        for neighbour, edge_cost in graph.get(current, ()):
            new_cost = current_cost + edge_cost
            if new_cost < distances.get(neighbour, float("inf")):
                distances[neighbour] = new_cost
                previous[neighbour] = current
                heappush(queue, (new_cost + heuristic(neighbour), new_cost, neighbour))

    if distances[destination] == float("inf"):
        return NO_ROUTE, []

    route = []
    current = destination
    while current is not None:
        route.append(current)
        current = previous[current]
    route.reverse()
    return distances[destination], route


def bfs_hops(graph, source):
    """Return hop counts from source to every reachable stop (unweighted BFS)."""
    hops = {source: 0}
    queue = deque([source])
    while queue:
        current = queue.popleft()
        for neighbour, _ in graph.get(current, ()):
            if neighbour not in hops:
                hops[neighbour] = hops[current] + 1
                queue.append(neighbour)
    return hops


def report(label, result):
    cost, route = result
    if route:
        print(f"{label:<10}: {' -> '.join(route)}  (cost {cost:g})")
    else:
        print(f"{label:<10}: no route found")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(DEFAULT_DATA),
                        help="CSV of source,destination,cost rows")
    parser.add_argument("--source", default="Central Station")
    parser.add_argument("--destination", default="Airport")
    args = parser.parse_args(argv)

    csv_path = Path(args.data)
    if csv_path.is_file():
        graph = load_transport_graph(csv_path)
        origin = f"{csv_path.name} ({len(graph)} stops with outbound routes)"
    else:
        graph = build_transport_graph()
        origin = f"built-in sample graph ({len(graph)} stops)"

    print("Public Transport Route Scheduling System")
    print("-" * 60)
    print(f"Graph       : {origin}")
    print(f"Source      : {args.source}")
    print(f"Destination : {args.destination}")
    print()

    report("Dijkstra", dijkstra(graph, args.source, args.destination))

    # A hop-count heuristic underestimates the true remaining cost, so A* must
    # agree with Dijkstra on the optimal cost while expanding fewer nodes.
    hops = bfs_hops(graph, args.source)
    report("A*", astar(graph, args.source, args.destination,
                       lambda node: hops.get(node, 0)))

    print(f"{'BFS hops':<10}: "
          + (f"{hops[args.destination]} stop(s) from source"
             if args.destination in hops else "unreachable"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())