"""Regression tests for the Python routing code.

Run with:  python -m unittest discover -s tests -v
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from dijkstra import NO_ROUTE, dijkstra, graph_nodes, validate_graph  # noqa: E402
from main import astar, bfs_hops, build_transport_graph, load_transport_graph  # noqa: E402


class TestNodeDiscovery(unittest.TestCase):
    def test_target_only_node_is_a_node(self):
        """A stop reachable only as an edge target is still part of the graph."""
        graph = {"A": [("B", 1)]}
        self.assertEqual(graph_nodes(graph), {"A", "B"})
        self.assertEqual(dijkstra(graph, "A", "B"), (1, ["A", "B"]))

    def test_unknown_source_raises(self):
        with self.assertRaises(ValueError):
            dijkstra({"A": [("B", 1)], "B": []}, "Z", "B")

    def test_unknown_destination_raises(self):
        with self.assertRaises(ValueError):
            dijkstra({"A": [("B", 1)], "B": []}, "A", "Z")


class TestValidation(unittest.TestCase):
    def test_negative_edge_on_untraversed_branch_is_rejected(self):
        """Regression: the check used to sit inside the traversal loop, so a
        negative edge on an unvisited branch was silently ignored."""
        graph = {"A": [("B", 5)], "B": [("A", 5)], "Z": [("Y", -100)]}
        with self.assertRaises(ValueError):
            dijkstra(graph, "A", "B")

    def test_negative_edge_on_traversed_path_is_rejected(self):
        with self.assertRaises(ValueError):
            dijkstra({"A": [("B", -1)], "B": []}, "A", "B")

    def test_non_numeric_cost_is_rejected(self):
        with self.assertRaises(ValueError):
            dijkstra({"A": [("B", "four")]}, "A", "B")

    def test_zero_cost_edges_are_allowed(self):
        self.assertEqual(dijkstra({"A": [("B", 0)], "B": []}, "A", "B"),
                         (0, ["A", "B"]))


class TestNoRoute(unittest.TestCase):
    def test_unreachable_returns_sentinel_not_inf(self):
        """Regression: this used to return a bare float('inf') to the caller."""
        cost, route = dijkstra({"A": [("B", 1)], "B": [], "Q": []}, "A", "Q")
        self.assertIs(cost, NO_ROUTE)
        self.assertEqual(route, [])

    def test_source_equals_destination(self):
        self.assertEqual(dijkstra({"A": [("B", 3)], "B": []}, "A", "A"),
                         (0, ["A"]))


class TestCorrectness(unittest.TestCase):
    def test_sample_network_optimum(self):
        graph = build_transport_graph()
        cost, route = dijkstra(graph, "Central Station", "Airport")
        self.assertEqual(cost, 13)
        self.assertEqual(route[0], "Central Station")
        self.assertEqual(route[-1], "Airport")

    def test_route_cost_equals_sum_of_edge_costs(self):
        """Any returned route must actually cost what the algorithm claims."""
        graph = build_transport_graph()
        cost, route = dijkstra(graph, "Central Station", "Airport")
        walked = 0.0
        for a, b in zip(route, route[1:]):
            edges = dict(graph[a])
            walked += edges[b]
        self.assertEqual(walked, cost)

    def test_dijkstra_agrees_with_astar_zero_heuristic(self):
        graph = build_transport_graph()
        self.assertEqual(
            dijkstra(graph, "Central Station", "Airport"),
            astar(graph, "Central Station", "Airport", lambda node: 0),
        )

    def test_dijkstra_agrees_with_astar_hop_heuristic(self):
        """An admissible heuristic must not change the optimal cost."""
        graph = build_transport_graph()
        hops = bfs_hops(graph, "Central Station")
        dijkstra_result = dijkstra(graph, "Central Station", "Airport")
        astar_result = astar(graph, "Central Station", "Airport",
                             lambda node: hops.get(node, 0))
        self.assertEqual(dijkstra_result[0], astar_result[0])

    def test_bfs_hop_counts(self):
        graph = build_transport_graph()
        hops = bfs_hops(graph, "Central Station")
        self.assertEqual(hops["City Mall"], 1)
        # Fewest stops is not the same as cheapest: BFS reaches Airport in 2
        # hops via University (cost 15), while the optimal route is 3 hops
        # via City Mall and Market (cost 13).
        self.assertEqual(hops["Airport"], 2)
        self.assertEqual(hops["Market"], 2)

    def test_fewest_hops_is_not_cheapest(self):
        """Documents why unweighted BFS cannot replace Dijkstra here."""
        graph = build_transport_graph()
        cost, route = dijkstra(graph, "Central Station", "Airport")
        self.assertEqual(len(route) - 1, 3)
        self.assertEqual(cost, 13)


class TestCsvLoading(unittest.TestCase):
    def setUp(self):
        self.path = ROOT / "data" / "sample_routes.csv"

    def test_loads_expected_routes(self):
        graph = load_transport_graph(self.path)
        self.assertEqual(dijkstra(graph, "Central Station", "Airport"),
                         (13.0, ["Central Station", "City Mall", "Market", "Airport"]))

    def test_routes_are_undirected(self):
        graph = load_transport_graph(self.path)
        # Airport -> Central Station must reverse cleanly.
        cost, route = dijkstra(graph, "Airport", "Central Station")
        self.assertEqual(cost, 13.0)
        self.assertEqual(route[-1], "Central Station")

    def test_header_row_is_skipped(self):
        graph = load_transport_graph(self.path)
        self.assertNotIn("source", graph)

    def test_malformed_row_raises(self):
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False) as fh:
            fh.write("A,B,1\nC,D\n")
            name = fh.name
        with self.assertRaises(ValueError):
            load_transport_graph(name)

    def test_non_numeric_cost_raises(self):
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False) as fh:
            fh.write("A,B,cheap\n")
            name = fh.name
        with self.assertRaises(ValueError):
            load_transport_graph(name)


if __name__ == "__main__":
    unittest.main(verbosity=2)