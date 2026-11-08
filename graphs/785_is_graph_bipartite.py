"""
LeetCode 785: Is Graph Bipartite?
Difficulty: Medium
Topic: Graphs / BFS Two-Coloring

Problem
-------
An undirected graph with n nodes (0..n-1) is given as an adjacency list
`graph`, where graph[u] lists the neighbors of u. The graph may be
disconnected. Return True if the nodes can be split into two sets A and B
so that every edge connects a node in A with a node in B.

Approach (thought process)
--------------------------
1. "Split into two sets with every edge crossing" is the same as "color
   every node with one of two colors so no edge joins two same-colored
   nodes".
2. Once you color one node, its neighbors are forced to the other color,
   their neighbors are forced back, and so on. There is no choice to
   make inside a connected component except the very first color, and by
   symmetry that choice does not matter.
3. So BFS from every uncolored node (to cover disconnected pieces):
     - give the start color 0
     - for each neighbor: if uncolored, give it the opposite color and
       enqueue it; if it already has the SAME color as the current node,
       we found an edge we cannot satisfy, so return False.
4. If every component colors cleanly, return True.

Why it works: the coloring is forced, so a conflict means no valid
2-coloring exists for that component. In graph terms, the conflict is
exactly an odd-length cycle, and a graph is bipartite iff it has no odd
cycle.

Complexity:
  - Time: O(V + E), each node and edge is handled a constant number of
    times.
  - Space: O(V) for the colors and the queue.
"""

from collections import deque
from typing import List


class Solution:
    def isBipartite(self, graph: List[List[int]]) -> bool:
        color = [-1] * len(graph)
        for start in range(len(graph)):
            if color[start] != -1:
                continue
            color[start] = 0
            queue = deque([start])
            while queue:
                u = queue.popleft()
                for v in graph[u]:
                    if color[v] == -1:
                        color[v] = 1 - color[u]
                        queue.append(v)
                    elif color[v] == color[u]:
                        return False
        return True


if __name__ == "__main__":
    s = Solution()
    # Example 1: square with a diagonal-ish extra edge -> triangle exists.
    assert s.isBipartite([[1, 2, 3], [0, 2], [0, 1, 3], [0, 2]]) is False
    # Example 2: 4-cycle -> bipartite.
    assert s.isBipartite([[1, 3], [0, 2], [1, 3], [0, 2]]) is True
    # Disconnected: an even edge plus an isolated triangle.
    assert s.isBipartite([[1], [0], [3, 4], [2, 4], [2, 3]]) is False
    # Disconnected and all fine: two separate edges plus an isolated node.
    assert s.isBipartite([[1], [0], [3], [2], []]) is True
    # Single node, empty graph.
    assert s.isBipartite([[]]) is True
    assert s.isBipartite([]) is True
    # Odd cycle of length 5.
    five = [[1, 4], [0, 2], [1, 3], [2, 4], [3, 0]]
    assert s.isBipartite(five) is False
    # Even cycle of length 6.
    six = [[(i - 1) % 6, (i + 1) % 6] for i in range(6)]
    assert s.isBipartite(six) is True
    print("all tests passed")
