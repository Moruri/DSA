"""LeetCode 1584 — Min Cost to Connect All Points (Medium).

Connect every point so any two are linked by some path, where an edge costs
the Manhattan distance |x1 - x2| + |y1 - y2|. Return the minimum total cost.

Approach: Prim's algorithm on the implicit complete graph, dense-graph form.
Keep, for every point not yet in the tree, the cheapest edge that reaches it
from the tree. Each round, pull in the closest outside point and let it lower
the other points' best costs. O(n^2) time, O(n) space, no heap needed.
"""
from typing import List


class Solution:
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        n = len(points)
        if n <= 1:
            return 0
        INF = float("inf")
        best = [INF] * n          # cheapest known edge into the tree
        in_tree = [False] * n
        best[0] = 0
        total = 0
        for _ in range(n):
            # pick the outside point with the cheapest connection
            u = -1
            for v in range(n):
                if not in_tree[v] and (u == -1 or best[v] < best[u]):
                    u = v
            in_tree[u] = True
            total += best[u]
            ux, uy = points[u]
            # u may offer a cheaper road to everyone still outside
            for v in range(n):
                if not in_tree[v]:
                    d = abs(ux - points[v][0]) + abs(uy - points[v][1])
                    if d < best[v]:
                        best[v] = d
        return total


if __name__ == "__main__":
    s = Solution()
    assert s.minCostConnectPoints([[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]) == 20
    assert s.minCostConnectPoints([[3, 12], [-2, 5], [-4, 1]]) == 18
    assert s.minCostConnectPoints([[0, 0]]) == 0
    assert s.minCostConnectPoints([[0, 0], [1, 1], [1, 0], [-1, 1]]) == 4
    print("1584 Min Cost to Connect All Points: all tests passed")
