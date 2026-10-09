"""
LeetCode 684: Redundant Connection
Difficulty: Medium
Topic: Graphs / Union-Find (Disjoint Set Union)

Problem
-------
A tree with n nodes (labelled 1..n) had one extra edge added, so the graph
now has exactly one cycle. Given the edge list in the order the edges were
added, return an edge that can be removed so the result is a tree again. If
several answers exist, return the one that appears last in the input.

Example 1:
  Input:  edges = [[1,2],[1,3],[2,3]]
  Output: [2,3]

Example 2:
  Input:  edges = [[1,2],[2,3],[3,4],[1,4],[1,5]]
  Output: [1,4]

Approach (thought process)
--------------------------
1. A tree on n nodes has n - 1 edges and no cycles. We have n edges, so one
   edge closes a cycle. The question is which one.
2. Replay the edges one at a time while tracking which nodes are already
   connected. An edge (u, v) is harmless if u and v are in different
   components: it just merges them. But if u and v are already connected,
   this edge creates a second path between them, which is the cycle.
3. "Are u and v connected?" plus "merge their groups" is exactly what
   Union-Find does in nearly O(1) per operation.
4. Why the first offending edge is also the "last in input" answer: only one
   edge closes the cycle in the replay order, and every other edge on that
   cycle appeared earlier (they had to be in place for u and v to already be
   connected). So the edge we catch is the latest cycle edge in the input.

Implementation details:
  - find(x) with path compression (point nodes closer to the root as we go).
  - union by size so trees stay shallow.
  - union returns False when both ends share a root; that edge is the answer.

Complexity: O(n * alpha(n)) time, effectively linear; O(n) space.
"""

from __future__ import annotations

from typing import List


class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        n = len(edges)
        parent = list(range(n + 1))
        size = [1] * (n + 1)

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]  # path halving
                x = parent[x]
            return x

        def union(a: int, b: int) -> bool:
            ra, rb = find(a), find(b)
            if ra == rb:
                return False
            if size[ra] < size[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            size[ra] += size[rb]
            return True

        for u, v in edges:
            if not union(u, v):
                return [u, v]
        return []


def _is_tree(n: int, edges: List[List[int]]) -> bool:
    adj = {i: [] for i in range(1, n + 1)}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    seen = {1}
    stack = [1]
    while stack:
        node = stack.pop()
        for nxt in adj[node]:
            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    return len(edges) == n - 1 and len(seen) == n


def _demo() -> None:
    sol = Solution()
    cases = [
        ([[1, 2], [1, 3], [2, 3]], [2, 3]),
        ([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]], [1, 4]),
        ([[1, 2], [2, 3], [3, 1]], [3, 1]),
    ]
    for edges, expected in cases:
        got = sol.findRedundantConnection(edges)
        status = "OK" if got == expected else "FAIL"
        print(f"{status}: findRedundantConnection({edges}) -> {got} (expected {expected})")
        assert got == expected

    # Random trees plus one extra edge: removing the answer must leave a tree,
    # and no later edge in the input may also work.
    import random

    rng = random.Random(684)
    for _ in range(200):
        n = rng.randint(3, 12)
        edges = [[rng.randint(1, i - 1), i] for i in range(2, n + 1)]
        while True:
            u, v = rng.sample(range(1, n + 1), 2)
            if [u, v] not in edges and [v, u] not in edges:
                break
        edges.append([u, v])
        rng.shuffle(edges)
        got = sol.findRedundantConnection(edges)
        idx = edges.index(got)
        assert _is_tree(n, edges[:idx] + edges[idx + 1 :])
        for later in range(idx + 1, len(edges)):
            assert not _is_tree(n, edges[:later] + edges[later + 1 :])
    print("OK: 200 random tree-plus-one-edge graphs verified")


if __name__ == "__main__":
    _demo()
