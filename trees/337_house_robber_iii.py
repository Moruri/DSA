"""
LeetCode 337: House Robber III
Difficulty: Medium
Topic: Trees / Tree DP (post-order)

Problem
-------
Houses form a binary tree. Robbing two directly linked houses (parent and
child) sets off the alarm. Return the most money you can rob.

Approach (thought process)
--------------------------
1. This is House Robber (198) on a tree: at each node you choose rob or
   skip, and robbing forbids robbing its children.
2. Plain recursion "best(node)" that tries both choices recomputes the
   grandchildren again and again (exponential). Instead, have every node
   return TWO numbers about its subtree:
     rob  = best total if this node IS robbed
     skip = best total if this node is NOT robbed
3. Post-order (children first), with (lr, ls) and (rr, rs) from the kids:
     rob  = node.val + ls + rs           # kids must be skipped
     skip = max(lr, ls) + max(rr, rs)    # each kid picks its own best
4. Answer = max of the root's pair. An empty subtree returns (0, 0).

Why it works: the pair is exactly what a parent needs to know about a
child, so each subtree is solved once and the choices combine locally.

Complexity
----------
Time:  O(n), one visit per node.
Space: O(h) recursion stack, h = tree height.
"""

from typing import List, Optional, Tuple


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def rob(self, root: Optional[TreeNode]) -> int:
        def dfs(node: Optional[TreeNode]) -> Tuple[int, int]:
            if not node:
                return 0, 0
            lr, ls = dfs(node.left)
            rr, rs = dfs(node.right)
            rob = node.val + ls + rs
            skip = max(lr, ls) + max(rr, rs)
            return rob, skip

        return max(dfs(root))


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
    cases = [
        ([3, 2, 3, None, 3, None, 1], 7),
        ([3, 4, 5, 1, 3, None, 1], 9),
        ([], 0),
        ([4, 1, None, 2, None, 3], 7),
    ]
    for values, want in cases:
        got = s.rob(build(values))
        assert got == want, (values, got, want)
        print(f"rob({values}) = {got}")
    print("All tests passed.")
