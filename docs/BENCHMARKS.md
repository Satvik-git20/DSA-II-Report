# Performance Analysis

The project report (§14) commits to "testing and performance analysis". These
are measured results from `tests/benchmark.py`, run on generated transport
networks of increasing size.

## Method

Each network is a sparse undirected graph where every stop links to its next
three neighbours by index, which approximates the irregular coverage of a real
bus network better than a regular grid. Costs are drawn from 1–20. The source is
`Stop 0` and the destination is the last stop, so the search cannot finish early.

Each measurement is the **best of 5 runs** in milliseconds, which reduces
scheduler noise. A cross-check asserts that Dijkstra and A\* return the same
optimal cost on the largest network, so the comparison is like-for-like.

Reproduce with:

```bash
python tests/benchmark.py
```

## Results

| Stops | Edges | Dijkstra | A\* | BFS | A\* saving |
|------:|------:|---------:|----:|----:|-----------:|
| 100 | 294 | 0.285 ms | 0.244 ms | 0.047 ms | 14.5% |
| 500 | 1,494 | 1.513 ms | 1.282 ms | 0.239 ms | 15.2% |
| 1,000 | 2,994 | 3.041 ms | 2.609 ms | 0.478 ms | 14.2% |
| 2,000 | 5,994 | 6.117 ms | 5.192 ms | 0.972 ms | 15.1% |
| 5,000 | 14,994 | 17.592 ms | 15.213 ms | 2.686 ms | 13.5% |

## Observations

**Dijkstra scales linearly with edges.** Doubling the edge count roughly doubles
the runtime (1,494 → 2,994 edges gives 1.513 ms → 3.041 ms), consistent with the
O((V + E) log V) bound for a binary-heap implementation.

**A\* is consistently but modestly faster.** It saves 13–15% at every size. The
heuristic is hop count, which is weakly informed: edge costs range 1–20, so one
hop can cost anywhere from 1 to 20 units and hop count barely constrains the true
remaining cost. A better heuristic — great-circle distance, or a lower bound
derived from the cheapest edge in the graph — would widen this gap. The result
reported here is honest about the current heuristic rather than flattering.

**BFS is much faster because it solves an easier problem.** It ignores weights
entirely, so it does no cost arithmetic and visits each node once. It is not
doing the same job: on the sample network BFS reaches the Airport in 2 hops
(cost 15) while the optimal route is 3 hops (cost 13). The `test_fewest_hops_is_
not_cheapest` test locks this distinction in.

**At 5,000 stops the whole search takes under 18 ms**, which is well inside an
interactive budget. For a real system the bottleneck would be network I/O, not
the algorithm.

## Limitations

- Single-threaded CPython on one machine; no comparison against the C
  implementations in `transport.c` / `graphs.c`, which would be the meaningful
  test of what compiled code buys.
- The heuristic is hop count, so the A\* saving understates what an informed
  heuristic could achieve.
- Costs are uniformly random, which is easier to search than real clustered
  demand patterns.