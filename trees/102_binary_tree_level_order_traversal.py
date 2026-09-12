"""
LeetCode 102: Binary Tree Level Order Traversal
Difficulty: Medium
Topic: Trees / BFS

Problem
-------
Given the root of a binary tree, return the level order traversal of its
nodes' values (i.e., from left to right, level by level).

Example 1:
  Input:  root = [3, 9, 20, null, null, 15, 7]
  Output: [[3], [9, 20], [15, 7]]

Example 2:
  Input:  root = [1]
  Output: [[1]]

Example 3:
  Input:  root = []
  Output: []

Approach (thought process)
--------------------------
1. Level order means visiting nodes breadth-first: finish one depth before
   the next. DFS alone does not naturally group by depth.
2. Use a queue (BFS). Start with the root. While the queue is non-empty,
   process exactly the nodes currently in it — that is one level.
3. For each level, collect values into a list and enqueue each node's left
   and right children for the next round.
4. Append each level's list to the answer. An empty root yields [].

Complexity: O(n) time, O(n) space for the queue / output (n = number of nodes).
"""

from __future__ import annotations

from collections import deque
from typing import Deque, List, Optional


class TreeNode:
    def __init__(
        self,
        val: int = 0,
        left: Optional["TreeNode"] = None,
        right: Optional["TreeNode"] = None,
    ) -> None:
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        """Return node values level by level, left to right."""
        if root is None:
            return []

        result: List[List[int]] = []
        queue: Deque[TreeNode] = deque([root])

        while queue:
            level_size = len(queue)
            level: List[int] = []
            for _ in range(level_size):
                node = queue.popleft()
                level.append(node.val)
                if node.left is not None:
                    queue.append(node.left)
                if node.right is not None:
                    queue.append(node.right)
            result.append(level)

        return result


def _build_tree(values: List[Optional[int]]) -> Optional[TreeNode]:
    """Build a binary tree from level-order list (None = missing child)."""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue: Deque[TreeNode] = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])  # type: ignore[arg-type]
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])  # type: ignore[arg-type]
            queue.append(node.right)
        i += 1
    return root


def _demo() -> None:
    sol = Solution()
    cases = [
        ([3, 9, 20, None, None, 15, 7], [[3], [9, 20], [15, 7]]),
        ([1], [[1]]),
        ([], []),
        ([1, 2, 3, 4, None, None, 5], [[1], [2, 3], [4, 5]]),
    ]
    for values, expected in cases:
        root = _build_tree(values)
        got = sol.levelOrder(root)
        status = "OK" if got == expected else "FAIL"
        print(f"{status}: root={values} -> {got} (expected {expected})")


if __name__ == "__main__":
    _demo()
