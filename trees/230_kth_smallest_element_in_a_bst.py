"""
LeetCode 230: Kth Smallest Element in a BST
Difficulty: Medium
Topic: Trees / BST In-order Traversal

Problem
-------
Given the root of a binary search tree and an integer k, return the kth
smallest value (1-indexed) among all the node values in the tree.

Example:
  root = [3, 1, 4, null, 2], k = 1 -> 1
  root = [5, 3, 6, 2, 4, null, null, 1], k = 3 -> 3

Approach (thought process)
--------------------------
1. Brute force: collect every value, sort, index k - 1. O(n log n) and it
   ignores the one thing a BST gives us for free.
2. The BST property (left < node < right) means an in-order walk
   (left, node, right) visits values in ascending order. So the kth node
   popped during an in-order walk *is* the answer. No sorting needed.
3. Do the in-order walk iteratively with an explicit stack so we can stop
   the moment we hit the kth node instead of walking the whole tree:
     - Slide left as far as possible, pushing each node.
     - Pop: that's the next-smallest value. Count it down; if k hits 0,
       return it.
     - Step into the popped node's right subtree and repeat.

Why it works: the stack always holds the "ancestors we still owe a visit",
smallest on top. Popping gives values in sorted order, exactly like reading
the BST left to right.

Follow-up (frequent inserts/deletes and many kth queries): store a subtree
size in each node. At a node, if size(left) >= k go left; if
size(left) + 1 == k it's this node; otherwise go right with
k - size(left) - 1. That makes each query O(h).

Complexity:
  - Time: O(h + k), where h is the tree height. We descend once and pop k
    nodes. Worst case O(n) for a skewed tree.
  - Space: O(h) for the stack.
"""

from typing import List, Optional


class TreeNode:
    def __init__(self, val: int = 0, left: "TreeNode" = None, right: "TreeNode" = None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        stack: List[TreeNode] = []
        node = root
        while stack or node:
            while node:
                stack.append(node)
                node = node.left
            node = stack.pop()
            k -= 1
            if k == 0:
                return node.val
            node = node.right
        raise ValueError("k is larger than the number of nodes")


def _insert(root: Optional[TreeNode], val: int) -> TreeNode:
    if root is None:
        return TreeNode(val)
    if val < root.val:
        root.left = _insert(root.left, val)
    else:
        root.right = _insert(root.right, val)
    return root


def _build(values: List[int]) -> Optional[TreeNode]:
    root = None
    for v in values:
        root = _insert(root, v)
    return root


if __name__ == "__main__":
    s = Solution()

    # [3, 1, 4, null, 2]
    root = TreeNode(3, TreeNode(1, None, TreeNode(2)), TreeNode(4))
    assert s.kthSmallest(root, 1) == 1
    assert s.kthSmallest(root, 3) == 3

    # [5, 3, 6, 2, 4, null, null, 1]
    root = TreeNode(5, TreeNode(3, TreeNode(2, TreeNode(1)), TreeNode(4)), TreeNode(6))
    assert s.kthSmallest(root, 3) == 3
    assert s.kthSmallest(root, 6) == 6

    assert s.kthSmallest(TreeNode(7), 1) == 7

    import random

    for _ in range(500):
        vals = random.sample(range(-50, 50), random.randint(1, 20))
        root = _build(vals)
        ordered = sorted(vals)
        for k in range(1, len(vals) + 1):
            assert s.kthSmallest(root, k) == ordered[k - 1]
    print("All tests passed.")
