"""
LeetCode 128: Longest Consecutive Sequence
Difficulty: Medium
Topic: Hashing

Problem
-------
Given an unsorted array of integers `nums`, return the length of the longest
consecutive elements sequence. Must run in O(n) time.

Example 1:
  Input:  nums = [100, 4, 200, 1, 3, 2]
  Output: 4
  Explanation: [1, 2, 3, 4]

Example 2:
  Input:  nums = [0, 3, 7, 2, 5, 8, 4, 6, 0, 1]
  Output: 9

Approach (thought process)
--------------------------
1. Sorting would give consecutive runs in O(n log n), but the O(n) budget
   rules that out — we need hash-set membership instead of order.
2. Put every number into a set. A consecutive run starting at `x` only exists
   when `x - 1` is *absent*: that marks the true start of a streak.
3. From each start, walk `x, x+1, x+2, ...` while members remain in the set,
   counting the length. Track the global maximum.
4. Each number is visited at most twice (once as a candidate start check, once
   inside a walk), so the nested-looking loop is still O(n). Duplicates are
   collapsed by the set for free.

Complexity: O(n) time, O(n) space for the set.
"""

from __future__ import annotations

from typing import List


class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        """Return length of the longest consecutive sequence in nums."""
        if not nums:
            return 0

        values = set(nums)
        best = 0
        for x in values:
            if x - 1 in values:
                continue
            length = 1
            while x + length in values:
                length += 1
            best = max(best, length)
        return best


def _demo() -> None:
    sol = Solution()
    cases = [
        ([100, 4, 200, 1, 3, 2], 4),
        ([0, 3, 7, 2, 5, 8, 4, 6, 0, 1], 9),
        ([], 0),
        ([1], 1),
        ([1, 2, 0, 1], 3),
        ([9, 1, 4, 7, 3, -1, 0, 5, 8, -1, 6], 7),
    ]
    for nums, expected in cases:
        got = sol.longestConsecutive(nums)
        status = "OK" if got == expected else "FAIL"
        print(f"{status}: longestConsecutive({nums}) -> {got} (expected {expected})")
        assert got == expected, (
            f"128 longestConsecutive({nums}) returned {got}, expected {expected}"
        )


if __name__ == "__main__":
    _demo()
