"""
LeetCode 662: Maximum Width of Binary Tree
Difficulty: Medium
Topic: Trees / BFS with Positional Indexing

Problem
-------
Return the maximum width over all levels of a binary tree. A level's width is
the distance between its leftmost and rightmost non-null nodes, counting the
null gaps between them as if the tree were complete.

Approach (thought process)
--------------------------
1. Counting nulls literally would explode (a deep skinny tree implies
   exponentially many gaps). Instead, label every node with the index it
   would have in a complete binary tree, heap-style: a node at index i has
   children at 2*i and 2*i + 1.
2. With those labels, a level's width is simply
   (index of last node) - (index of first node) + 1. The gaps are counted
   for free by the arithmetic.
3. Walk the tree level by level with BFS, carrying (node, index) pairs.
4. Indices double every level, so on a deep tree they grow huge. Python ints
   don't overflow, but it's still tidy (and needed in fixed-width languages)
   to re-base each level by subtracting that level's first index. Widths are
   differences, so shifting everything by a constant changes nothing.

Why it works: the heap labeling is exactly the position a node would occupy
if every missing slot were filled in, which is precisely the definition of
width the problem uses.

Complexity:
  - Time: O(n), each node is visited once.
  - Space: O(w), the largest number of nodes on one level in the queue.
"""

from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val: int = 0, left: "Optional[TreeNode]" = None, right: "Optional[TreeNode]" = None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def widthOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        best = 0
        queue = deque([(root, 0)])
        while queue:
            first = queue[0][1]
            last = queue[-1][1]
            best = max(best, last - first + 1)
            for _ in range(len(queue)):
                node, idx = queue.popleft()
                idx -= first  # re-base so numbers stay small
                if node.left:
                    queue.append((node.left, 2 * idx))
                if node.right:
                    queue.append((node.right, 2 * idx + 1))
        return best


def build(values: List[Optional[int]]) -> Optional[TreeNode]:
    """Build a tree from LeetCode-style level-order list."""
    if not values or values[0] is None:
        return None
    it = iter(values)
    root = TreeNode(next(it))
    queue = deque([root])
    while queue:
        node = queue.popleft()
        for side in ("left", "right"):
            try:
                v = next(it)
            except StopIteration:
                return root
            if v is not None:
                child = TreeNode(v)
                setattr(node, side, child)
                queue.append(child)
    return root


def _demo() -> None:
    sol = Solution()
    cases = [
        ([1, 3, 2, 5, 3, None, 9], 4),
        ([1, 3, 2, 5, None, None, 9, 6, None, 7], 7),
        ([1, 3, 2, 5], 2),
        ([1], 1),
        ([], 0),
    ]
    for values, expected in cases:
        got = sol.widthOfBinaryTree(build(values))
        print(f"{'OK' if got == expected else 'FAIL'}: {values} -> {got} (expected {expected})")
        assert got == expected, f"662 width({values}) returned {got}, expected {expected}"


if __name__ == "__main__":
    _demo()
