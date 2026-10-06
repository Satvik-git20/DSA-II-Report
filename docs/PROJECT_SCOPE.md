# Project Scope

This project is based on the Month 1 PBL Progress Report. The report identifies
graphs, queues, priority queues/heaps, arrays, linked lists, BFS, DFS, and A*
Search as relevant concepts, and plans Dijkstra's Algorithm for the next review.

## Status

Implemented and tested:

- Dijkstra's shortest path (`src/dijkstra.py`)
- A* search and unweighted BFS for comparison (`src/main.py`)
- CSV-backed transport network loading (`src/main.py`)
- DFS, BFS, connected components, Kruskal, Prim, Dijkstra, Bellman-Ford and
  Floyd-Warshall in C (`graphs.c`)
- An 8-stop transport case study covering the above plus resource allocation
  DP, 0/1 knapsack and LCS (`transport.c`)
- Knapsack, LCS, matrix chain multiplication and resource allocation (`dp.c`)
- Unit tests (`tests/test_routing.py`) and measured performance analysis
  (`tests/benchmark.py`, results in `BENCHMARKS.md`)

Not implemented:

- The route scheduling module. The system selects a shortest path; it does not
  build timetables or allocate vehicles over time.
- Informed A* heuristics beyond hop count.

The code in `src/` provides the Dijkstra prototype and uses sample transport
data. It is intentionally an academic starter implementation, not a claim of a
completed real-time transport platform.