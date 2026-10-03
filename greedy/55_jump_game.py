"""
LeetCode 55: Jump Game
Difficulty: Medium
Topic: Greedy

Problem
-------
You are given an integer array `nums`. You are initially positioned at the
first index, and each element `nums[i]` represents the maximum jump length
from that index. Return `true` if you can reach the last index, or `false`
otherwise.

Example 1:
  Input:  nums = [2, 3, 1, 1, 4]
  Output: true
  Explanation: jump 1 step to index 1, then 3 steps to the end

Example 2:
  Input:  nums = [3, 2, 1, 0, 4]
  Output: false
  Explanation: always land at index 3 where the jump length is 0

Approach (thought process)
--------------------------
1. Tracking every reachable index (BFS / DP boolean array) works but is
   heavier than needed — we only care whether the *farthest* reachable
   position ever covers the last index.
2. Scan left to right. While the current index `i` is still within the
   farthest reach so far, update `farthest = max(farthest, i + nums[i])`.
3. If `farthest` ever reaches or passes the last index, return True. If the
   loop ends with `i` stuck beyond `farthest`, a gap of zeros blocks the path.
4. Only one pass and a few scalars — no queue or DP table required.

Complexity: O(n) time, O(1) extra space.
"""

from __future__ import annotations

from typing import List


class Solution:
    def canJump(self, nums: List[int]) -> bool:
        """Return True iff the last index is reachable from index 0."""
        farthest = 0
        last = len(nums) - 1
        i = 0
        while i <= farthest:
            farthest = max(farthest, i + nums[i])
            if farthest >= last:
                return True
            i += 1
        return False


def _demo() -> None:
    sol = Solution()
    cases = [
        ([2, 3, 1, 1, 4], True),
        ([3, 2, 1, 0, 4], False),
        ([0], True),
        ([1, 0], True),
        ([0, 1], False),
        ([2, 0, 0], True),
        ([1, 1, 1, 0], True),
        ([1, 1, 0, 1], False),
    ]
    for nums, expected in cases:
        got = sol.canJump(nums)
        status = "OK" if got == expected else "FAIL"
        print(f"{status}: canJump({nums}) -> {got} (expected {expected})")
        assert got == expected, (
            f"55 canJump({nums}) returned {got}, expected {expected}"
        )


if __name__ == "__main__":
    _demo()
