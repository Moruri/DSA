"""
LeetCode 547: Number of Provinces
Link: https://leetcode.com/problems/number-of-provinces/
Difficulty: Medium
Topic: Union-Find

Problem
-------
There are n cities numbered from 0 to n - 1. Some are connected directly;
connectivity is transitive, so a city a connected to b and b to c means a, b,
and c form one province.

You are given an n x n matrix isConnected where isConnected[i][j] == 1 means
cities i and j are directly connected (and 0 means they are not). Return the
total number of provinces.

Example 1:
  Input:  isConnected = [[1,1,0],[1,1,0],[0,0,1]]
  Output: 2
  Explanation: cities 0-1 form one province; city 2 alone is another.

Example 2:
  Input:  isConnected = [[1,0,0],[0,1,0],[0,0,1]]
  Output: 3

Approach (thought process)
--------------------------
1. A province is a connected component in an undirected graph whose vertices
   are cities and whose edges are the 1-entries of isConnected (the matrix is
   symmetric and the diagonal is always 1).
2. DFS/BFS from each unvisited city also counts components (same idea as
   Number of Islands). Here we prefer Union-Find because the folder theme is
   disjoint-set and the adjacency matrix is a natural batch of undirected edges.
3. Start with n singleton sets (one per city). For every pair i < j with
   isConnected[i][j] == 1, union(i, j). After all edges are processed, the
   number of distinct roots is the number of provinces.
4. Path compression on find plus union-by-rank keeps nearly O(1) per operation,
   so the whole pass is effectively linear in the number of matrix cells we
   inspect (the upper triangle).

Complexity: O(n² · α(n)) time (scan the matrix; α is inverse Ackermann ≈ 1),
O(n) extra space for parent/rank arrays.
"""

from __future__ import annotations

from typing import List


class _UnionFind:
    """Disjoint-set with path compression and union by rank."""

    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n

    def find(self, x: int) -> int:
        """Return the root of x, compressing the path along the way."""
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]  # path halving
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> None:
        """Merge the sets containing a and b, if they differ."""
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.rank[ra] < self.rank[rb]:
            self.parent[ra] = rb
        elif self.rank[ra] > self.rank[rb]:
            self.parent[rb] = ra
        else:
            self.parent[rb] = ra
            self.rank[ra] += 1
        self.components -= 1


class Solution:
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        """Return the number of provinces (connected components) via Union-Find."""
        n = len(isConnected)
        if n == 0:
            return 0

        uf = _UnionFind(n)
        for i in range(n):
            for j in range(i + 1, n):
                if isConnected[i][j] == 1:
                    uf.union(i, j)
        return uf.components


def _demo() -> None:
    sol = Solution()
    cases = [
        ([[1, 1, 0], [1, 1, 0], [0, 0, 1]], 2),
        ([[1, 0, 0], [0, 1, 0], [0, 0, 1]], 3),
        ([[1]], 1),
        ([[1, 1], [1, 1]], 1),
        # Chain 0-1-2-3: one province despite sparse direct edges.
        (
            [
                [1, 1, 0, 0],
                [1, 1, 1, 0],
                [0, 1, 1, 1],
                [0, 0, 1, 1],
            ],
            1,
        ),
        # Two pairs.
        (
            [
                [1, 1, 0, 0],
                [1, 1, 0, 0],
                [0, 0, 1, 1],
                [0, 0, 1, 1],
            ],
            2,
        ),
    ]
    for matrix, expected in cases:
        got = sol.findCircleNum([row[:] for row in matrix])
        status = "OK" if got == expected else "FAIL"
        print(f"{status}: n={len(matrix)} -> {got} (expected {expected})")
        assert got == expected, (
            f"547 findCircleNum(n={len(matrix)}) returned {got}, expected {expected}"
        )


if __name__ == "__main__":
    _demo()
