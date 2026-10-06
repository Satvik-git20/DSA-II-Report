# Public Transport Route Scheduling System

A Data Structures and Algorithms II project modelling public transport networks
as weighted graphs and finding efficient routes with shortest-path techniques.

## Project Information

- Course: Data Structure and Algorithms II
- Course Code: CCSE0301
- Program: B.Tech CSE-A
- Assignment: Individual
- Student: Adityaraj Singh
- Project: Public Transport Route Scheduling System
- SDGs: SDG 9 and SDG 11

## Problem

Public transport systems can suffer from inefficient route planning, delays,
longer passenger waiting times, traffic congestion, and poor vehicle
utilization.

## Objectives

- Model transport networks using graphs.
- Apply shortest-path algorithms.
- Reduce route-selection cost.
- Demonstrate practical DSA concepts.
- Prepare the foundation for a route scheduling module.

## Repository Structure

```text
.
├── src/
│   ├── dijkstra.py          # Dijkstra's shortest-path algorithm
│   └── main.py              # CSV loading, CLI, A* and BFS comparison
├── tests/
│   ├── test_routing.py      # 20 unit tests
│   └── benchmark.py         # performance comparison
├── data/
│   └── sample_routes.csv    # source,destination,cost
├── docs/
│   ├── Descriptive_Project_Report.docx
│   ├── PROJECT_SCOPE.md
│   └── BENCHMARKS.md        # measured performance results
├── graphs.c                 # adjacency lists, DFS/BFS, Kruskal, Prim,
│                            #   Dijkstra, Bellman-Ford, Floyd-Warshall
├── transport.c              # transport case study: DFS/BFS/MST/Dijkstra/
│                            #   Floyd-Warshall + resource allocation, knapsack, LCS
├── dp.c                     # knapsack, LCS, matrix chain, resource allocation
├── requirements.txt
└── README.md
```

## Python Implementation

Python 3.10+ is recommended. No external packages are required.

```bash
python src/main.py
```

Options:

```bash
python src/main.py --source "City Mall" --destination "Airport"
python src/main.py --data data/sample_routes.csv
```

Reads `data/sample_routes.csv` by default, treating every row as a route
travellable in both directions. It compares three techniques on the same network:

```text
Dijkstra  : Central Station -> City Mall -> Market -> Airport  (cost 13)
A*        : Central Station -> City Mall -> Market -> Airport  (cost 13)
BFS hops  : 2 stop(s) from source
```

Dijkstra and A\* return the same optimal cost, as they must — A\* adds a
heuristic that guides the search without changing the answer. BFS is faster
because it answers a different question: fewest stops, not lowest cost. On this
network that distinction matters, since the 2-hop path costs 15 while the 3-hop
path costs 13.

Run the tests and benchmarks:

```bash
python -m unittest discover -s tests -v
python tests/benchmark.py
```

## C Implementation

The C files are self-contained demonstrations of the algorithms on small
networks. Compile and run any of them:

```bash
gcc -Wall -Wextra -o graphs graphs.c && ./graphs
gcc -Wall -Wextra -o transport transport.c && ./transport
gcc -Wall -Wextra -o dp dp.c && ./dp
```

| File | Algorithms |
|------|-----------|
| `graphs.c` | DFS, BFS, connected components, Kruskal, Prim, Dijkstra, Bellman-Ford, Floyd-Warshall |
| `transport.c` | DFS components, BFS hops, Kruskal MST, Dijkstra, Floyd-Warshall, resource allocation DP, 0/1 knapsack, LCS — on an 8-stop transit network |
| `dp.c` | 0/1 knapsack, LCS, matrix chain multiplication, resource allocation |

`graphs.c` includes a directed graph with a negative edge to show why
Bellman-Ford is needed when weights can be negative. Dijkstra cannot handle
those, which is why the Python implementation validates and rejects them up
front.

## Data Format

`data/sample_routes.csv`:

```csv
source,destination,cost
Central Station,City Mall,4
Central Station,University,6
```

The header is optional and comments (`#`) are skipped. Costs must be
non-negative. Malformed rows raise an error naming the file and line rather than
failing silently.

## Known Limitations

- The route scheduling module described in the report is **not** implemented —
  the project stops at shortest-path selection.
- No A\* heuristics beyond hop count, so the benchmark shows only a 13–15%
  improvement over Dijkstra rather than the larger gap an informed heuristic
  would give.
- The C demos use fixed-size arrays sized to their sample networks
  (`MAX_EDGES`, `MAXV`, `MAX_STR`). They report an error rather than overrun when
  given a larger input, but they are teaching programs, not production code.
- The CSV and the `build_transport_graph()` fallback in `main.py` describe the
  same network in two places; the CSV is the source of truth when present.

## Future Work

- Route scheduling module
- Queue and priority-queue integration
- Realistic transport datasets
- Informed A\* heuristics
- Optional GUI/web interface

## Academic Note

This repository represents the project direction and the implementation
completed so far. It should be extended with the student's own tested results,
datasets, screenshots, and analysis as development progresses.