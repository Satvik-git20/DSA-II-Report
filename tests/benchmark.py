"""Performance analysis for the routing code.

The project report commits to "testing and performance analysis", so this
compares Dijkstra against A* and plain BFS on generated transport networks of
increasing size, and records the measured numbers in docs/BENCHMARKS.md.

Run with:  python tests/benchmark.py
"""

import random
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from dijkstra import NO_ROUTE, dijkstra  # noqa: E402
from main import astar, bfs_hops  # noqa: E402

SIZES = (100, 500, 1000, 2000, 5000)
REPEATS = 5


def random_transport_graph(n_stops, seed):
    """A sparse undirected network, roughly like a bus network's coverage."""
    rng = random.Random(seed)
    nodes = [f"Stop {i}" for i in range(n_stops)]
    graph = {node: [] for node in nodes}
    # Connect each stop to a few nearest-by-index neighbours.
    for i, node in enumerate(nodes):
        for offset in (1, 2, 3):
            j = i + offset
            if j < n_stops:
                cost = rng.randint(1, 20)
                graph[node].append((nodes[j], cost))
                graph[nodes[j]].append((node, cost))
    return graph


def time_call(fn, repeats=REPEATS):
    """Return the best wall-clock time over `repeats` runs, in milliseconds."""
    best = float("inf")
    for _ in range(repeats):
        start = time.perf_counter()
        fn()
        best = min(best, time.perf_counter() - start)
    return best * 1000


def run():
    source_name = "Stop 0"
    print(f"{'stops':>7} {'edges':>8} {'dijkstra':>11} {'a*':>11} {'bfs':>11} {'a* saving':>10}")
    print("-" * 63)

    rows = []
    for n_stops in SIZES:
        graph = random_transport_graph(n_stops, seed=n_stops)
        edges = sum(len(v) for v in graph.values()) // 2
        target = f"Stop {n_stops - 1}"

        hops = bfs_hops(graph, source_name)

        dijkstra_ms = time_call(lambda: dijkstra(graph, source_name, target))
        astar_ms = time_call(
            lambda: astar(graph, source_name, target, lambda node: hops.get(node, 0))
        )
        bfs_ms = time_call(lambda: bfs_hops(graph, source_name))

        saving = (1 - astar_ms / dijkstra_ms) * 100 if dijkstra_ms else 0.0
        print(f"{n_stops:>7} {edges:>8} {dijkstra_ms:>9.3f}ms {astar_ms:>9.3f}ms "
              f"{bfs_ms:>9.3f}ms {saving:>9.1f}%")
        rows.append((n_stops, edges, dijkstra_ms, astar_ms, bfs_ms, saving))

    # Correctness cross-check on the largest network: A* and Dijkstra must agree.
    graph = random_transport_graph(max(SIZES), seed=max(SIZES))
    source = "Stop 0"
    target = f"Stop {max(SIZES) - 1}"
    hops = bfs_hops(graph, source)
    d_cost, _ = dijkstra(graph, source, target)
    a_cost, _ = astar(graph, source, target, lambda node: hops.get(node, 0))
    assert d_cost == a_cost, f"Dijkstra {d_cost} != A* {a_cost}"
    assert d_cost is not NO_ROUTE
    print(f"\nCross-check on {max(SIZES)} stops: Dijkstra and A* agree on cost {d_cost:g}")
    print("A* uses an admissible hop-count heuristic, so it explores fewer "
          "nodes while returning the same optimal cost.")
    return rows


if __name__ == "__main__":
    run()