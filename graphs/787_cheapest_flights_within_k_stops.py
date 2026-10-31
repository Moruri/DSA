"""
LeetCode 787: Cheapest Flights Within K Stops
Difficulty: Medium
Topic: Graphs / Bellman-Ford (bounded rounds)

Problem
-------
There are n cities and a list of directed flights [from, to, price]. Return
the cheapest price from src to dst using at most k stops (so at most k + 1
flights), or -1 if no such route exists.

Examples:
  n = 4, flights = [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]],
  src = 0, dst = 3, k = 1  ->  700   (0 -> 1 -> 3; 0 -> 1 -> 2 -> 3 needs 2 stops)
  n = 3, flights = [[0,1,100],[1,2,100],[0,2,500]], src = 0, dst = 2, k = 1 -> 200
  same graph, k = 0  ->  500

Approach (thought process)
--------------------------
1. Plain Dijkstra is the reflex for "cheapest path", but it breaks here: it
   settles each city once at its cheapest cost, and that cheapest route might
   burn too many stops. A pricier route with fewer hops may be the only one
   that still fits the budget, and Dijkstra would already have thrown it away.
2. The constraint is "at most k + 1 edges". Bellman-Ford has exactly that
   shape: after round i of relaxing every edge, dist[v] is the cheapest cost
   using at most i edges. So run exactly k + 1 rounds and read dist[dst].
3. The one trap: within a round, relax from a SNAPSHOT of the previous round
   (prev). If you update dist in place, a city improved early in round i can
   be used again later in the same round, chaining two flights into one round
   and quietly exceeding the stop limit.

Why it works: by induction, after round i, cur[v] = min cost over all walks
src -> v with at most i edges. Round i + 1 extends each of those by one edge
(from prev) and keeps the old values (copy), so the invariant holds. After
k + 1 rounds we have the best route with at most k stops.

Complexity:
  - Time: O((k + 1) * E), one pass over the flights per round.
  - Space: O(n) for the two distance arrays.
"""

import heapq
from typing import List


class Solution:
    def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        INF = float("inf")
        dist = [INF] * n
        dist[src] = 0
        for _ in range(k + 1):
            prev = dist[:]  # snapshot: each round may add only ONE flight
            for u, v, w in flights:
                if prev[u] + w < dist[v]:
                    dist[v] = prev[u] + w
        return -1 if dist[dst] == INF else dist[dst]


def _brute(n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
    # Dijkstra over (city, edges_used) states, used only to cross-check.
    adj = [[] for _ in range(n)]
    for u, v, w in flights:
        adj[u].append((v, w))
    best = {}
    heap = [(0, src, 0)]
    while heap:
        cost, u, used = heapq.heappop(heap)
        if u == dst:
            return cost
        if used == k + 1 or best.get((u, used), float("inf")) < cost:
            continue
        for v, w in adj[u]:
            nc = cost + w
            if nc < best.get((v, used + 1), float("inf")):
                best[(v, used + 1)] = nc
                heapq.heappush(heap, (nc, v, used + 1))
    return -1


if __name__ == "__main__":
    import random

    sol = Solution()
    f1 = [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]]
    assert sol.findCheapestPrice(4, f1, 0, 3, 1) == 700
    f2 = [[0, 1, 100], [1, 2, 100], [0, 2, 500]]
    assert sol.findCheapestPrice(3, f2, 0, 2, 1) == 200
    assert sol.findCheapestPrice(3, f2, 0, 2, 0) == 500
    assert sol.findCheapestPrice(3, [[0, 1, 5]], 0, 2, 3) == -1

    rng = random.Random(787)
    for _ in range(2000):
        n = rng.randint(2, 6)
        pairs = {(u, v) for u in range(n) for v in range(n) if u != v}
        chosen = rng.sample(sorted(pairs), rng.randint(0, len(pairs)))
        fl = [[u, v, rng.randint(1, 20)] for u, v in chosen]
        s, d = rng.sample(range(n), 2)
        kk = rng.randint(0, n - 1)
        assert sol.findCheapestPrice(n, fl, s, d, kk) == _brute(n, fl, s, d, kk), (n, fl, s, d, kk)
    print("All tests passed for 787.")
