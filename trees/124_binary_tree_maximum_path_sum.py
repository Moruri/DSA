"""
LeetCode 124: Binary Tree Maximum Path Sum
Difficulty: Hard
Topic: Trees / Post-order DFS (return one thing, record another)

Problem
-------
A path is a sequence of nodes where each adjacent pair is joined by an edge,
and no node appears twice. The path does not need to pass through the root.
Return the maximum sum of node values over all non-empty paths.

Example 1: root = [1, 2, 3]                 -> 6   (2 -> 1 -> 3)
Example 2: root = [-10, 9, 20, null, null, 15, 7] -> 42  (15 -> 20 -> 7)

Approach (thought process)
--------------------------
1. Every path has exactly one "highest" node, the peak where it turns. At
   the peak, the path is: best downward chain from the left child + the
   peak's value + best downward chain from the right child.
2. So for each node we want gain(node) = the best sum of a chain that starts
   at node and goes straight down (one side only). That is
       gain(node) = node.val + max(0, gain(left), gain(right))
   The max(0, ...) means "drop a branch that only hurts".
3. Post-order DFS computes gain bottom-up. While at a node we also try it as
   the peak: node.val + max(0, gain(left)) + max(0, gain(right)), and keep
   a running best.
4. The key subtlety: the value we RETURN to the parent can use only one
   branch (a parent can't extend a path that already forks), but the value
   we RECORD as a candidate answer may use both branches.
5. Start best at -infinity, not 0, so an all-negative tree returns its
   largest single node instead of 0.

Why it works: every path is counted exactly at its peak, and at the peak the
best choice of each side is independent, so the two best downward chains
give the best path through that peak.

Complexity: O(n) time, O(h) recursion stack (h = tree height).
"""

from __future__ import annotations

from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val: int = 0, left: "TreeNode | None" = None,
                 right: "TreeNode | None" = None) -> None:
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        best = float("-inf")

        def gain(node: Optional[TreeNode]) -> int:
            nonlocal best
            if node is None:
                return 0
            left = max(gain(node.left), 0)
            right = max(gain(node.right), 0)
            best = max(best, node.val + left + right)  # node as the peak
            return node.val + max(left, right)        # one branch upward

        gain(root)
        return int(best)


def build(values: List[Optional[int]]) -> Optional[TreeNode]:
    """Build a tree from LeetCode-style level-order list."""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue, i = deque([root]), 1
    while queue and i < len(values):
        node = queue.popleft()
        for side in ("left", "right"):
            if i < len(values) and values[i] is not None:
                child = TreeNode(values[i])
                setattr(node, side, child)
                queue.append(child)
            i += 1
    return root


if __name__ == "__main__":
    s = Solution()
    cases = [
        ([1, 2, 3], 6),
        ([-10, 9, 20, None, None, 15, 7], 42),
        ([-3], -3),
        ([-2, -1], -1),
        ([2, -1], 2),
        ([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1], 48),
    ]
    for values, expected in cases:
        got = s.maxPathSum(build(values))
        assert got == expected, (values, got, expected)
        print(f"{values} -> {got}")
    print("All tests passed.")
