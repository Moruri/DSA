"""
LeetCode 300: Longest Increasing Subsequence
Link: https://leetcode.com/problems/longest-increasing-subsequence/
Difficulty: Medium
Topic: Dynamic Programming / Binary Search

Problem
-------
Given an integer array nums, return the length of the longest strictly
increasing subsequence.

A subsequence is derived from the array by deleting some or no elements
without changing the order of the remaining elements.

Example 1:
  Input:  nums = [10, 9, 2, 5, 3, 7, 101, 18]
  Output: 4
  Explanation: The LIS is [2, 3, 7, 101] (length 4).

Example 2:
  Input:  nums = [0, 1, 0, 3, 2, 3]
  Output: 4

Example 3:
  Input:  nums = [7, 7, 7, 7, 7, 7, 7]
  Output: 1

Approach (thought process)
--------------------------
1. Classic DP: let dp[i] be the LIS length ending at i. Then
     dp[i] = 1 + max({dp[j] | j < i and nums[j] < nums[i]} or {0})
   Answer is max(dp). O(n²) time — fine for small n, slow for n = 2500.
2. Patience sorting / tails array improves to O(n log n). Maintain `tails`
   where tails[k] is the smallest tail of every increasing subsequence of
   length k + 1 seen so far. The array stays strictly increasing.
3. For each num: if it is larger than every tail, append it (LIS grows by 1).
   Otherwise binary-search the first tail >= num and replace it — a smaller
   tail only makes future extensions easier; LIS length does not shrink.
4. After the scan, len(tails) is the LIS length. (Reconstructing the actual
   subsequence needs extra back-pointers; we only need the length here.)
5. Empty input → 0; all equal → 1.

Complexity: O(n log n) time, O(n) space for the tails array.
"""

from __future__ import annotations

from bisect import bisect_left
from typing import List


class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        """Return the length of the longest strictly increasing subsequence."""
        if not nums:
            return 0

        tails: List[int] = []
        for num in nums:
            i = bisect_left(tails, num)
            if i == len(tails):
                tails.append(num)
            else:
                tails[i] = num
        return len(tails)


def _demo() -> None:
    sol = Solution()
    cases = [
        ([10, 9, 2, 5, 3, 7, 101, 18], 4),
        ([0, 1, 0, 3, 2, 3], 4),
        ([7, 7, 7, 7, 7, 7, 7], 1),
        ([1], 1),
        ([], 0),
        ([1, 3, 6, 7, 9, 4, 10, 5, 6], 6),
        ([4, 10, 4, 3, 8, 9], 3),
        ([1, 2, 3, 4, 5], 5),
    ]
    for nums, expected in cases:
        got = sol.lengthOfLIS(nums)
        status = "OK" if got == expected else "FAIL"
        print(f"{status}: nums={nums} -> {got} (expected {expected})")
        assert got == expected, (
            f"300 lengthOfLIS({nums}) returned {got}, expected {expected}"
        )


if __name__ == "__main__":
    _demo()
