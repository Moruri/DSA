"""
LeetCode 743: Network Delay Time
Difficulty: Medium
Topic: Graphs / Dijkstra (shortest paths with a min-heap)

Problem
-------
There are n network nodes labelled 1..n and a list of directed, weighted edges
times[i] = (u, v, w): a signal sent from u reaches v after w time units.
A signal starts at node k. Return how long it takes for ALL nodes to receive
it, or -1 if some node can never be reached.

Example:
  Input:  times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2
  Output: 2

Approach (thought process)
--------------------------
1. Every node hears the signal at the moment of its *shortest* path from k,
   so the answer is the largest shortest-path distance (or -1 if any node is
   unreachable). The problem reduces to single-source shortest paths.
2. Weights are non-negative, which is exactly when Dijkstra applies. Keep a
   min-heap of (distance, node). Pop the closest unsettled node; its distance
   is now final, because any other route would go through a node that is
   already at least as far away and weights can't make it shorter.
3. Relax its outgoing edges: push (d + w, neighbour) for each one. Stale heap
   entries (a node popped again with a worse distance) are simply skipped.
4. When the heap empties, if we settled all n nodes the answer is the max
   settled distance; otherwise -1.

Why it works: the heap always hands us the globally nearest frontier node,
so nodes are settled in non-decreasing distance order, and the last node
settled is the last one to hear the signal.

Complexity: O(E log E) time for heap operations, O(V + E) space.
"""

import heapq
from collections import defaultdict
from typing import List


class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        graph = defaultdict(list)
        for u, v, w in times:
            graph[u].append((v, w))

        dist = {}
        heap = [(0, k)]
        while heap:
            d, node = heapq.heappop(heap)
            if node in dist:  # already settled with a shorter distance
                continue
            dist[node] = d
            for nxt, w in graph[node]:
                if nxt not in dist:
                    heapq.heappush(heap, (d + w, nxt))

        return max(dist.values()) if len(dist) == n else -1


if __name__ == "__main__":
    s = Solution()
    assert s.networkDelayTime([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2) == 2
    assert s.networkDelayTime([[1, 2, 1]], 2, 1) == 1
    assert s.networkDelayTime([[1, 2, 1]], 2, 2) == -1
    # A longer direct edge loses to a cheaper detour.
    assert s.networkDelayTime([[1, 2, 10], [1, 3, 1], [3, 2, 2]], 3, 1) == 3
    print("743 Network Delay Time: all tests passed")
