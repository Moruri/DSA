"""
LeetCode 98: Validate Binary Search Tree
Link: https://leetcode.com/problems/validate-binary-search-tree/
Difficulty: Medium
Topic: Trees / BST

Problem
-------
Given the root of a binary tree, determine if it is a valid binary search
tree (BST).

A valid BST is defined as follows:
  - The left subtree of a node contains only nodes with keys strictly less
    than the node's key.
  - The right subtree of a node contains only nodes with keys strictly
    greater than the node's key.
  - Both the left and right subtrees must also be binary search trees.

Example 1:
  Input:  root = [2, 1, 3]
  Output: true

Example 2:
  Input:  root = [5, 1, 4, null, null, 3, 6]
  Output: false
  Explanation: The root's right child is 4, which is less than 5, so invalid.
  Also 3 sits in the right subtree but is less than the root.

Approach (thought process)
--------------------------
1. Checking only "left < node < right" against immediate children is not
   enough: a node deep in the left subtree could still be ≥ some ancestor.
2. Every node must lie in an open interval (lo, hi) inherited from its
   ancestors. The root starts with (-∞, +∞).
3. Recurse: for node with value v, verify lo < v < hi. Then the left child
   must satisfy (lo, v) and the right child (v, hi).
4. An empty subtree is vacuously valid. Use None sentinels for unbounded
   ends so we never invent fake min/max integers that collide with node
   values at the extremes of the 32-bit range.
5. Alternatively, an inorder walk of a BST is strictly increasing — but the
   range-propagation DFS above makes the BST invariant explicit and visits
   each node once.

Complexity: O(n) time, O(h) space for the recursion stack (h = tree height).
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
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        """Return True iff the tree is a valid BST (strict inequalities)."""

        def valid(
            node: Optional[TreeNode],
            lo: Optional[int],
            hi: Optional[int],
        ) -> bool:
            if node is None:
                return True
            if lo is not None and node.val <= lo:
                return False
            if hi is not None and node.val >= hi:
                return False
            return valid(node.left, lo, node.val) and valid(
                node.right, node.val, hi
            )

        return valid(root, None, None)


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
        ([2, 1, 3], True),
        ([5, 1, 4, None, None, 3, 6], False),
        ([1], True),
        ([], True),
        ([5, 4, 6, None, None, 3, 7], False),  # 3 is in right subtree but < 5
        ([2, 2, 2], False),  # equal keys break strict BST
        ([3, 1, 5, 0, 2, 4, 6], True),
        ([10, 5, 15, None, None, 6, 20], False),  # 6 < 10 but in right subtree
        ([1, None, 1], False),
        ([2147483647], True),
        ([-2147483648, None, 2147483647], True),
    ]
    for values, expected in cases:
        root = _build_tree(values)
        got = sol.isValidBST(root)
        status = "OK" if got == expected else "FAIL"
        print(f"{status}: root={values} -> {got} (expected {expected})")
        assert got == expected, (
            f"98 isValidBST({values}) returned {got}, expected {expected}"
        )


if __name__ == "__main__":
    _demo()
