"""
LeetCode 198: House Robber
Difficulty: Medium
Topic: Dynamic Programming

Problem
-------
You are a professional robber planning to rob houses along a street. Each
house has a certain amount of money stashed. The only constraint is that
adjacent houses have security systems connected: if two adjacent houses are
broken into on the same night, the police are alerted.

Given an integer array nums representing the amount of money in each house,
return the maximum amount you can rob tonight without alerting the police.

Example 1:
  Input:  nums = [1, 2, 3, 1]
  Output: 4
  Explanation: Rob house 1 (money = 1) and house 3 (money = 3). 1 + 3 = 4.

Example 2:
  Input:  nums = [2, 7, 9, 3, 1]
  Output: 12
  Explanation: Rob houses 1, 3 and 5 (2 + 9 + 1 = 12).

Approach (thought process)
--------------------------
1. Brute force: for every subset of non-adjacent houses, sum the money and
   keep the best. That is exponential — far too slow.
2. Notice the choice at house i depends only on what we did at i-1 and i-2.
   Define dp[i] = the most money obtainable from houses 0..i. Two options:
     - skip house i:  dp[i] = dp[i-1]
     - rob  house i:  dp[i] = dp[i-2] + nums[i]  (house i-1 must be skipped)
   So dp[i] = max(dp[i-1], dp[i-2] + nums[i]).
3. Base cases: dp[0] = nums[0]; dp[1] = max(nums[0], nums[1]). Working with a
   virtual dp[-1] = 0 and dp[-2] = 0 handles these uniformly.
4. Only the last two dp values are ever needed, so keep two rolling variables
   (prev2 = dp[i-2], prev1 = dp[i-1]) instead of a full array. The answer is
   prev1 after the scan; an empty street yields 0.

Complexity: O(n) time, O(1) extra space.
"""

from __future__ import annotations

from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        """Return the maximum loot without robbing two adjacent houses."""
        prev2 = 0  # best total up to house i-2
        prev1 = 0  # best total up to house i-1

        for money in nums:
            # Either skip this house (prev1) or rob it on top of prev2.
            current = max(prev1, prev2 + money)
            prev2, prev1 = prev1, current

        return prev1


def _demo() -> None:
    sol = Solution()
    cases = [
        ([1, 2, 3, 1], 4),
        ([2, 7, 9, 3, 1], 12),
        ([], 0),
        ([5], 5),
        ([2, 1], 2),
        ([2, 1, 1, 2], 4),
        ([0, 0, 0], 0),
    ]
    for nums, expected in cases:
        got = sol.rob(nums)
        status = "OK" if got == expected else "FAIL"
        print(f"{status}: nums={nums} -> {got} (expected {expected})")
        assert got == expected, f"198 rob({nums}) returned {got}, expected {expected}"


if __name__ == "__main__":
    _demo()
