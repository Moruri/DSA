"""
LeetCode 103: Binary Tree Zigzag Level Order Traversal
Difficulty: Medium
Topic: Trees / BFS (alternating direction)

Problem
-------
Given the root of a binary tree, return the level order traversal of its
values, but zigzag: left-to-right on level 0, right-to-left on level 1, and
so on, alternating.

Approach (thought process)
--------------------------
1. Strip away the zigzag and this is plain level-order traversal (102):
   BFS with a queue, processing one whole level per outer-loop iteration
   (snapshot len(queue) so you know where the level ends).
2. The zigzag only changes the *order we write values*, not the order we
   *visit nodes*. Tempting trick: alternate which child you enqueue first.
   That breaks on the next level because the queue order gets scrambled.
   Keep the traversal boring and fix the output instead.
3. For each level, allocate a row of size k (the level width). Visiting the
   i-th node of the level, write it to row[i] on left-to-right levels and to
   row[k - 1 - i] on right-to-left levels. A deque with appendleft works
   too; reversing the row on odd levels is the simplest version of all.
4. Flip a boolean after every level.

Why it works: BFS visits every level left to right exactly once, so the
i-th visited node of a level is the i-th node from the left. Placing it at
index i or its mirror k-1-i produces exactly the required order, and the
child ordering for the next level is never disturbed.

Complexity
----------
Time:  O(n) -- every node is enqueued and dequeued once.
Space: O(w) for the queue, w = max level width (up to ~n/2), plus O(n) output.
"""

from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []
        out: List[List[int]] = []
        q = deque([root])
        left_to_right = True
        while q:
            k = len(q)
            row = [0] * k
            for i in range(k):
                node = q.popleft()
                row[i if left_to_right else k - 1 - i] = node.val
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
            out.append(row)
            left_to_right = not left_to_right
        return out


def build(values):
    """Build a tree from LeetCode-style level-order list (None = missing)."""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    q = deque([root])
    i = 1
    while q and i < len(values):
        node = q.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            q.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            q.append(node.right)
        i += 1
    return root


if __name__ == "__main__":
    s = Solution()
    cases = [
        ([3, 9, 20, None, None, 15, 7], [[3], [20, 9], [15, 7]]),
        ([1], [[1]]),
        ([], []),
        ([1, 2, 3, 4, None, None, 5], [[1], [3, 2], [4, 5]]),
        ([1, 2, 3, 4, 5, 6, 7, 8, 9], [[1], [3, 2], [4, 5, 6, 7], [9, 8]]),
    ]
    for values, want in cases:
        got = s.zigzagLevelOrder(build(values))
        assert got == want, (values, got, want)
        print(f"zigzagLevelOrder({values}) = {got}")
    print("All tests passed.")
