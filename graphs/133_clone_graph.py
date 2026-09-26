"""
LeetCode 133: Clone Graph
Link: https://leetcode.com/problems/clone-graph/
Difficulty: Medium
Topic: Graphs / DFS / BFS

Problem
-------
Given a reference of a node in a connected undirected graph, return a deep
copy (clone) of the graph.

Each node contains an integer value and a list of neighbours:

    class Node:
        def __init__(self, val=0, neighbors=None):
            self.val = val
            self.neighbors = neighbors if neighbors is not None else []

The graph is represented as an adjacency list. The given node is always the
first node with val = 1 (when the graph is non-empty). The graph may be empty
(node is None).

Example 1:
  Input:  adjList = [[2, 4], [1, 3], [2, 4], [1, 3]]
  Output: [[2, 4], [1, 3], [2, 4], [1, 3]]
  Explanation: 1 — 2
               |   |
               4 — 3

Example 2:
  Input:  adjList = [[]]
  Output: [[]]
  Explanation: Single node with val = 1 and no neighbours.

Example 3:
  Input:  adjList = []
  Output: []
  Explanation: Empty graph; the given node is None.

Approach (thought process)
--------------------------
1. A shallow copy that reuses the original neighbour objects is wrong — we
   need a brand-new Node for every original node, with edges only among the
   clones.
2. Traverse from the given node (DFS or BFS). Keep a map
   original → clone so each node is created exactly once and cycles do not
   recurse forever.
3. On first visit: allocate `clone = Node(node.val)`, store it in the map,
   then recursively (or iteratively) clone each neighbour and append the
   cloned neighbour to `clone.neighbors`.
4. When a neighbour is already in the map, reuse that clone — that is how
   shared edges and back-edges are wired correctly.
5. Empty input (node is None) returns None; a lone node with no neighbours
   returns a single new Node with an empty neighbour list.

Complexity: O(V + E) time and O(V) space for the map / recursion stack.
"""

from __future__ import annotations

from typing import Dict, List, Optional


class Node:
    def __init__(self, val: int = 0, neighbors: Optional[List["Node"]] = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


class Solution:
    def cloneGraph(self, node: Optional[Node]) -> Optional[Node]:
        """Return a deep copy of the undirected graph rooted at node."""
        if node is None:
            return None

        clones: Dict[Node, Node] = {}

        def dfs(curr: Node) -> Node:
            if curr in clones:
                return clones[curr]
            copy = Node(curr.val)
            clones[curr] = copy
            for neighbor in curr.neighbors:
                copy.neighbors.append(dfs(neighbor))
            return copy

        return dfs(node)


def _build_graph(adj: List[List[int]]) -> Optional[Node]:
    """Build a graph from 1-indexed adjacency lists; return node 1."""
    if not adj:
        return None
    nodes = {i: Node(i) for i in range(1, len(adj) + 1)}
    for i, neighbors in enumerate(adj, start=1):
        nodes[i].neighbors = [nodes[n] for n in neighbors]
    return nodes[1]


def _to_adj(node: Optional[Node]) -> List[List[int]]:
    """Serialise a graph (from node 1) back to sorted adjacency lists."""
    if node is None:
        return []
    seen: Dict[int, List[int]] = {}
    stack = [node]
    while stack:
        curr = stack.pop()
        if curr.val in seen:
            continue
        seen[curr.val] = sorted(n.val for n in curr.neighbors)
        for n in curr.neighbors:
            if n.val not in seen:
                stack.append(n)
    return [seen[i] for i in range(1, max(seen) + 1)]


def _is_deep_copy(original: Optional[Node], clone: Optional[Node]) -> bool:
    """True iff clone mirrors original's structure with distinct Node objects."""
    if original is None and clone is None:
        return True
    if original is None or clone is None:
        return False
    visited_o: Dict[int, Node] = {}
    visited_c: Dict[int, Node] = {}
    stack = [(original, clone)]
    while stack:
        o, c = stack.pop()
        if o is c:
            return False  # shared object — not a deep copy
        if o.val != c.val:
            return False
        if o.val in visited_o:
            if visited_o[o.val] is not o or visited_c[c.val] is not c:
                return False
            continue
        visited_o[o.val] = o
        visited_c[c.val] = c
        if len(o.neighbors) != len(c.neighbors):
            return False
        o_vals = sorted(n.val for n in o.neighbors)
        c_vals = sorted(n.val for n in c.neighbors)
        if o_vals != c_vals:
            return False
        o_by_val = {n.val: n for n in o.neighbors}
        c_by_val = {n.val: n for n in c.neighbors}
        for v in o_vals:
            stack.append((o_by_val[v], c_by_val[v]))
    return True


def _demo() -> None:
    sol = Solution()
    cases = [
        [[2, 4], [1, 3], [2, 4], [1, 3]],
        [[]],
        [],
        [[2], [1]],
        [[2, 3], [1], [1]],
    ]
    for adj in cases:
        original = _build_graph(adj)
        clone = sol.cloneGraph(original)
        got = _to_adj(clone)
        deep = _is_deep_copy(original, clone)
        status = "OK" if got == adj and deep else "FAIL"
        print(f"{status}: adj={adj} -> {got} (deep_copy={deep})")
        assert got == adj, f"133 cloneGraph adj mismatch: {got} != {adj}"
        assert deep, f"133 cloneGraph did not produce a deep copy for {adj}"


if __name__ == "__main__":
    _demo()
