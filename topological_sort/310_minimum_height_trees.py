"""
LeetCode 310: Minimum Height Trees
Difficulty: Medium
Topic: Graphs / Topological Sort (Leaf Peeling)

Problem
-------
A tree has n nodes labeled 0..n-1 and n-1 undirected edges. Picking any
node as the root gives a rooted tree with some height. Return every root
label that gives the minimum possible height.

Approach (thought process)
--------------------------
1. Brute force (BFS from every node) is O(n^2). We want the "center" of the
   tree instead: the node(s) that sit in the middle of the longest path.
2. Intuition: leaves are the worst possible roots, since they are at the
   ends of paths. If we strip off every current leaf at once, the center of
   the tree does not move, because every longest path loses one node at
   each end.
3. So peel the tree layer by layer like an onion, Kahn-style: start with all
   degree-1 nodes, remove them, decrease their neighbors' degrees, and the
   neighbors that drop to degree 1 form the next layer.
4. Stop when 2 or fewer nodes remain. A longest path has either one middle
   node (odd length) or two (even length), so the answer has 1 or 2 nodes.
5. Edge case: n == 1 means the only node is the answer.

Why it works: the height from root r equals the distance to the farthest
leaf, and that is minimized at the middle of a diameter path. Peeling all
leaves simultaneously shortens every diameter equally from both ends, so
the survivors are exactly the middle node(s).

Complexity
----------
Time:  O(n), every node and edge is processed once.
Space: O(n) for the adjacency lists and the queue.
"""

from typing import List


class Solution:
    def findMinHeightTrees(self, n: int, edges: List[List[int]]) -> List[int]:
        if n <= 2:
            return list(range(n))

        adj = [set() for _ in range(n)]
        for a, b in edges:
            adj[a].add(b)
            adj[b].add(a)

        leaves = [i for i in range(n) if len(adj[i]) == 1]
        remaining = n
        while remaining > 2:
            remaining -= len(leaves)
            next_leaves = []
            for leaf in leaves:
                neighbor = adj[leaf].pop()
                adj[neighbor].remove(leaf)
                if len(adj[neighbor]) == 1:
                    next_leaves.append(neighbor)
            leaves = next_leaves
        return sorted(leaves)


if __name__ == "__main__":
    sol = Solution()
    assert sol.findMinHeightTrees(4, [[1, 0], [1, 2], [1, 3]]) == [1]
    assert sol.findMinHeightTrees(6, [[3, 0], [3, 1], [3, 2], [3, 4], [5, 4]]) == [3, 4]
    assert sol.findMinHeightTrees(1, []) == [0]
    assert sol.findMinHeightTrees(2, [[0, 1]]) == [0, 1]
    # A straight line 0-1-2-3-4: the middle node is 2.
    assert sol.findMinHeightTrees(5, [[0, 1], [1, 2], [2, 3], [3, 4]]) == [2]
    print("All tests passed.")
