"""
LeetCode 236: Lowest Common Ancestor of a Binary Tree
Link: https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/
Difficulty: Medium
Topic: Trees

Problem
-------
Given a binary tree, find the lowest common ancestor (LCA) of two given nodes
p and q in the tree.

The lowest common ancestor is defined as the lowest node in T that has both
p and q as descendants (where we allow a node to be a descendant of itself).

Example 1:
  Input:  root = [3, 5, 1, 6, 2, 0, 8, null, null, 7, 4], p = 5, q = 1
  Output: 3
  Explanation: The LCA of nodes 5 and 1 is 3.

Example 2:
  Input:  root = [3, 5, 1, 6, 2, 0, 8, null, null, 7, 4], p = 5, q = 4
  Output: 5
  Explanation: The LCA of nodes 5 and 4 is 5 (a node may be a descendant of
  itself).

Approach (thought process)
--------------------------
1. Unlike a BST, there is no value-order shortcut — we must search the
   structure. A post-order DFS that reports whether each subtree contains
   p and/or q is enough.
2. Recurse on left and right. If the current root is p or q, return root
   immediately (it is an ancestor of itself and may sit above the other).
3. If both left and right recursive calls return non-null, p and q lie in
   different subtrees — the current root is their LCA.
4. Otherwise bubble up whichever side is non-null (both targets are deeper
   on that side, or only one was found so far). A null root yields null.
5. Each node is visited once; the call stack is O(h).

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
    def lowestCommonAncestor(
        self, root: Optional[TreeNode], p: TreeNode, q: TreeNode
    ) -> Optional[TreeNode]:
        """Return the LCA of nodes p and q in the binary tree rooted at root."""
        if root is None or root is p or root is q:
            return root

        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)

        if left is not None and right is not None:
            return root
        return left if left is not None else right


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


def _find(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    """Return the first node with the given value (DFS)."""
    if root is None:
        return None
    if root.val == val:
        return root
    return _find(root.left, val) or _find(root.right, val)


def _demo() -> None:
    sol = Solution()
    cases = [
        # Classic LC example: LCA(5, 1) = 3
        ([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], 5, 1, 3),
        # LCA(5, 4) = 5 (node is ancestor of itself)
        ([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], 5, 4, 5),
        # LCA(6, 4) = 5
        ([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], 6, 4, 5),
        # Two-node tree
        ([1, 2], 1, 2, 1),
        # Skewed left: LCA is root
        ([1, 2, None, 3], 2, 3, 2),
        # LCA of siblings under right child
        ([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], 7, 4, 2),
        # Same node twice
        ([1, 2, 3], 2, 2, 2),
        # Deep right vs left
        ([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], 2, 8, 6),
        ([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], 3, 5, 4),
    ]
    for values, p_val, q_val, expected in cases:
        root = _build_tree(values)
        p = _find(root, p_val)
        q = _find(root, q_val)
        assert p is not None and q is not None
        got_node = sol.lowestCommonAncestor(root, p, q)
        got = got_node.val if got_node is not None else None
        status = "OK" if got == expected else "FAIL"
        print(
            f"{status}: root={values}, p={p_val}, q={q_val} -> {got} "
            f"(expected {expected})"
        )
        assert got == expected, (
            f"236 lowestCommonAncestor(p={p_val}, q={q_val}) returned {got}, "
            f"expected {expected}"
        )


if __name__ == "__main__":
    _demo()
