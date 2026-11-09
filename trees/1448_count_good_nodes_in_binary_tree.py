"""
LeetCode 1448: Count Good Nodes in Binary Tree
Difficulty: Medium
Topic: Trees / DFS with Path State

Problem
-------
A node X is "good" if no node on the path from the root to X has a value
greater than X. Return the number of good nodes in the tree.

Approach (thought process)
--------------------------
1. Whether a node is good depends only on its ancestors, and only on the
   single largest of them. So we don't need the whole path, just the
   running maximum along it.
2. DFS from the root, carrying max_so_far. At each node:
     - it is good if node.val >= max_so_far (count it),
     - then pass max(max_so_far, node.val) down to both children.
3. The root is always good, which falls out naturally if we start with
   max_so_far = root.val (or -infinity).
4. Use an explicit stack to avoid Python's recursion limit on skewed trees.

Why it works: each node sees exactly the maximum of its root-to-node path
(excluding itself), which is the only fact the definition of "good" needs.

Complexity:
  - Time: O(n), each node visited once.
  - Space: O(h) for the stack, where h is the tree height (O(n) worst case).
"""

from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def goodNodes(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        good = 0
        stack = [(root, root.val)]
        while stack:
            node, max_so_far = stack.pop()
            if node.val >= max_so_far:
                good += 1
            new_max = max(max_so_far, node.val)
            if node.left:
                stack.append((node.left, new_max))
            if node.right:
                stack.append((node.right, new_max))
        return good


def build(values: List[Optional[int]]) -> Optional[TreeNode]:
    """Build a tree from LeetCode-style level-order list."""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue, i = [root], 1
    while queue and i < len(values):
        node = queue.pop(0)
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    return root


if __name__ == "__main__":
    s = Solution()
    assert s.goodNodes(build([3, 1, 4, 3, None, 1, 5])) == 4
    assert s.goodNodes(build([3, 3, None, 4, 2])) == 3
    assert s.goodNodes(build([1])) == 1
    # Deep skewed tree (increasing): every node is good, no recursion limit issue.
    root = cur = TreeNode(0)
    for v in range(1, 5000):
        cur.right = TreeNode(v)
        cur = cur.right
    assert s.goodNodes(root) == 5000
    print("All tests passed for 1448 Count Good Nodes in Binary Tree.")
