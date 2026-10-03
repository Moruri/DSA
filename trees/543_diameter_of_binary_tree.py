"""
LeetCode 543: Diameter of Binary Tree
Difficulty: Easy
Topic: Trees

Problem
-------
Given the root of a binary tree, return the length of the diameter of the
tree. The diameter is the length of the longest path between any two nodes
(number of edges). The path may or may not pass through the root.

Example 1:
  Input:  root = [1, 2, 3, 4, 5]
  Output: 3
  Explanation: paths [4, 2, 1, 3] or [5, 2, 1, 3]

Example 2:
  Input:  root = [1, 2]
  Output: 1

Approach (thought process)
--------------------------
1. For any node, the longest path that *bends* through it is
   (height of left subtree) + (height of right subtree) — edges down left
   plus edges down right.
2. The global diameter is the maximum of that quantity over every node, so
   a single DFS that returns height can also update a running best.
3. Height of None is 0. Height of a node is 1 + max(left_h, right_h). Before
   returning, record `left_h + right_h` against the answer.
4. Post-order ensures both children are known when we score the bend at the
   current node. The answer may live entirely in one subtree (never touch
   the root), which the global max still catches.

Complexity: O(n) time, O(h) recursion space (h = height).
"""

from __future__ import annotations

from typing import List, Optional


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
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        """Return the number of edges on the longest path in the tree."""
        best = 0

        def height(node: Optional[TreeNode]) -> int:
            nonlocal best
            if node is None:
                return 0
            left_h = height(node.left)
            right_h = height(node.right)
            best = max(best, left_h + right_h)
            return 1 + max(left_h, right_h)

        height(root)
        return best


def _from_list(values: List[Optional[int]]) -> Optional[TreeNode]:
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue: List[TreeNode] = [root]
    i = 1
    while queue and i < len(values):
        node = queue.pop(0)
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
        ([1, 2, 3, 4, 5], 3),
        ([1, 2], 1),
        ([1], 0),
        ([1, 2, 3, 4, 5, None, None, 6, 7], 4),
        ([], 0),
    ]
    for values, expected in cases:
        got = sol.diameterOfBinaryTree(_from_list(values))
        status = "OK" if got == expected else "FAIL"
        print(f"{status}: diameterOfBinaryTree({values}) -> {got} (expected {expected})")
        assert got == expected, (
            f"543 diameterOfBinaryTree({values}) returned {got}, expected {expected}"
        )


if __name__ == "__main__":
    _demo()
