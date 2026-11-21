"""
LeetCode 1631: Path With Minimum Effort
Difficulty: Medium
Topic: Graphs / Dijkstra (Minimax Path)

Problem
-------
You are a hiker on a rows x cols grid of heights. Start at the top-left,
finish at the bottom-right, moving up/down/left/right. A route's "effort"
is the LARGEST absolute height difference between two consecutive cells on
it. Return the minimum effort over all routes.

Approach (thought process)
--------------------------
1. See the grid as a graph: each cell is a node, each pair of neighbours
   is an edge weighted by |height difference|.
2. The cost of a path is not a sum, it's a MAX of edge weights (a
   "minimax" or bottleneck path). Dijkstra still works, because extending a
   path can never make its cost go down: max(cost, w) >= cost. That
   monotonic property is all Dijkstra really needs.
3. So run Dijkstra with a min-heap keyed by "effort so far". Pop the cell
   with the smallest effort; for each neighbour, the candidate effort is
   max(current effort, |h[cell] - h[nbr]|). If that beats the neighbour's
   best known effort, record it and push.
4. The first time the bottom-right cell is popped, its effort is final:
   every other route still in the heap is already at least that hard.

Why it works: the heap always expands the easiest frontier cell first, and
since efforts never decrease along a path, nothing popped later can offer a
cheaper way back to a cell already settled.

Alternatives: binary search on the answer E + BFS using only edges <= E,
or Kruskal-style union-find adding edges by weight until start and end
connect. Both are fine; Dijkstra is the most direct.

Complexity
----------
Time:  O(R*C * log(R*C)) - each cell pushed a few times, heap operations log.
Space: O(R*C) for the best-effort table and the heap.
"""

import heapq
from typing import List


class Solution:
    def minimumEffortPath(self, heights: List[List[int]]) -> int:
        rows, cols = len(heights), len(heights[0])
        best = [[float("inf")] * cols for _ in range(rows)]
        best[0][0] = 0
        heap = [(0, 0, 0)]  # (effort so far, row, col)

        while heap:
            effort, r, c = heapq.heappop(heap)
            if (r, c) == (rows - 1, cols - 1):
                return effort
            if effort > best[r][c]:
                continue  # stale heap entry
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    step = abs(heights[nr][nc] - heights[r][c])
                    cand = max(effort, step)
                    if cand < best[nr][nc]:
                        best[nr][nc] = cand
                        heapq.heappush(heap, (cand, nr, nc))
        return 0


if __name__ == "__main__":
    s = Solution()
    cases = [
        ([[1, 2, 2], [3, 8, 2], [5, 3, 5]], 2),
        ([[1, 2, 3], [3, 8, 4], [5, 3, 5]], 1),
        ([[1, 2, 1, 1, 1], [1, 2, 1, 2, 1], [1, 2, 1, 2, 1], [1, 2, 1, 2, 1], [1, 1, 1, 2, 1]], 0),
        ([[7]], 0),
        ([[1, 10, 6, 7, 9, 10, 4, 9]], 9),
    ]
    for grid, want in cases:
        got = s.minimumEffortPath(grid)
        assert got == want, (grid, got, want)
        print(f"effort={got}  (expected {want})")
    print("All 1631 tests passed.")
