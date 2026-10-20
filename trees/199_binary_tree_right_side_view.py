"""
LeetCode 199: Binary Tree Right Side View
Difficulty: Medium
Topic: Trees / BFS

Problem
-------
Given the root of a binary tree, imagine standing on its right side. Return
the values of the nodes you can see, ordered from top to bottom.

Example 1:
  Input:  root = [1, 2, 3, null, 5, null, 4]
  Output: [1, 3, 4]

Example 2:
  Input:  root = [1, 2, 3, 4]
  Output: [1, 3, 4]   (the lone 4 on level 3 hangs off the left side,
                       but nothing blocks it, so it's visible)

Approach (thought process)
--------------------------
1. "Visible from the right" is not "walk down the right children". A deep
   left subtree can poke out below a short right subtree (Example 2), so
   chasing `.right` gives the wrong answer.
2. What we actually see is the LAST node on each depth level. That makes it
   a level-order question: BFS processes the tree one level at a time.
3. Run BFS with a queue. At the start of each level, the queue holds exactly
   that level's nodes, so we know its size. Pop that many, push their
   children left-then-right, and record the value of the final node popped.
4. Alternative: DFS visiting right before left, recording a node the first
   time its depth is reached. Same answer, recursion instead of a queue.

Complexity: O(n) time (every node is visited once), O(w) space for the queue,
where w is the tree's maximum width.
"""

from __future__ import annotations

from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val: int = 0, left: "TreeNode | None" = None,
                 right: "TreeNode | None" = None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        if root is None:
            return []
        view: List[int] = []
        queue = deque([root])
        while queue:
            for _ in range(len(queue)):
                node = queue.popleft()
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            view.append(node.val)  # last node popped on this level
        return view


def _dfs_view(root: Optional[TreeNode]) -> List[int]:
    out: List[int] = []

    def go(node: Optional[TreeNode], depth: int) -> None:
        if node is None:
            return
        if depth == len(out):
            out.append(node.val)
        go(node.right, depth + 1)
        go(node.left, depth + 1)

    go(root, 0)
    return out


def build(values: List[Optional[int]]) -> Optional[TreeNode]:
    """Build a tree from LeetCode's level-order list format."""
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


if __name__ == "__main__":
    s = Solution()
    assert s.rightSideView(build([1, 2, 3, None, 5, None, 4])) == [1, 3, 4]
    assert s.rightSideView(build([1, 2, 3, 4])) == [1, 3, 4]
    assert s.rightSideView(build([1, None, 3])) == [1, 3]
    assert s.rightSideView(build([])) == []

    import random

    for _ in range(500):
        n = random.randint(0, 20)
        vals = [random.choice([None, random.randint(0, 99)]) if i else
                random.randint(0, 99) for i in range(n)]
        root = build(vals)
        assert s.rightSideView(root) == _dfs_view(root), vals
    print("All tests passed.")
