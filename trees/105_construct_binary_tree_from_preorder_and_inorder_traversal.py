"""
LeetCode 105: Construct Binary Tree from Preorder and Inorder Traversal
Difficulty: Medium
Topic: Trees

Problem
-------
Given two integer arrays `preorder` and `inorder` where `preorder` is the
preorder traversal of a binary tree and `inorder` is the inorder traversal
of the same tree, construct and return the binary tree. It is guaranteed
that values are unique.

Example 1:
  Input:  preorder = [3, 9, 20, 15, 7], inorder = [9, 3, 15, 20, 7]
  Output: [3, 9, 20, null, null, 15, 7]

Example 2:
  Input:  preorder = [-1], inorder = [-1]
  Output: [-1]

Approach (thought process)
--------------------------
1. Preorder always lists the root first, then the whole left subtree, then
   the right. Inorder lists the left subtree, then the root, then the right.
2. Take `preorder[0]` as the root. Find that value in `inorder`; everything
   left of it belongs to the left subtree, everything right to the right.
3. The left subtree size equals the count of inorder elements before the
   root. Slice both arrays accordingly and recurse.
4. An index map from value → inorder position turns the root lookup into
   O(1). Pass index ranges instead of copying slices to keep the build
   linear in the number of nodes.

Complexity: O(n) time, O(n) space (map + recursion stack).
"""

from __future__ import annotations

from typing import Dict, List, Optional


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
    def buildTree(
        self, preorder: List[int], inorder: List[int]
    ) -> Optional[TreeNode]:
        """Rebuild the unique tree from preorder + inorder traversals."""
        if not preorder or not inorder:
            return None

        index: Dict[int, int] = {val: i for i, val in enumerate(inorder)}

        def build(pre_lo: int, pre_hi: int, in_lo: int, in_hi: int) -> Optional[TreeNode]:
            if pre_lo > pre_hi or in_lo > in_hi:
                return None
            root_val = preorder[pre_lo]
            root = TreeNode(root_val)
            mid = index[root_val]
            left_size = mid - in_lo
            root.left = build(pre_lo + 1, pre_lo + left_size, in_lo, mid - 1)
            root.right = build(pre_lo + left_size + 1, pre_hi, mid + 1, in_hi)
            return root

        n = len(preorder)
        return build(0, n - 1, 0, n - 1)


def _to_list(root: Optional[TreeNode]) -> List[Optional[int]]:
    """Level-order list with trailing Nones trimmed (LeetCode style)."""
    if root is None:
        return []
    out: List[Optional[int]] = []
    queue: List[Optional[TreeNode]] = [root]
    while queue:
        node = queue.pop(0)
        if node is None:
            out.append(None)
            continue
        out.append(node.val)
        queue.append(node.left)
        queue.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


def _demo() -> None:
    sol = Solution()
    cases = [
        ([3, 9, 20, 15, 7], [9, 3, 15, 20, 7], [3, 9, 20, None, None, 15, 7]),
        ([-1], [-1], [-1]),
        ([1, 2], [2, 1], [1, 2]),
        ([1, 2], [1, 2], [1, None, 2]),
        ([1, 2, 3], [2, 1, 3], [1, 2, 3]),
    ]
    for preorder, inorder, expected in cases:
        got = _to_list(sol.buildTree(preorder, inorder))
        status = "OK" if got == expected else "FAIL"
        print(
            f"{status}: buildTree({preorder}, {inorder}) -> {got} (expected {expected})"
        )
        assert got == expected, (
            f"105 buildTree({preorder}, {inorder}) returned {got}, expected {expected}"
        )


if __name__ == "__main__":
    _demo()
