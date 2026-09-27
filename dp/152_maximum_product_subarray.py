"""
LeetCode 152: Maximum Product Subarray
Link: https://leetcode.com/problems/maximum-product-subarray/
Difficulty: Medium
Topic: Dynamic Programming

Problem
-------
Given an integer array nums, find a contiguous non-empty subarray within the
array that has the largest product, and return the product.

The test cases are generated so that the answer will fit in a 32-bit integer.

Example 1:
  Input:  nums = [2, 3, -2, 4]
  Output: 6
  Explanation: [2, 3] has the largest product 6.

Example 2:
  Input:  nums = [-2, 0, -1]
  Output: 0
  Explanation: The result cannot be 2, because [-2, -1] is not contiguous.

Approach (thought process)
--------------------------
1. Kadane for sums fails here: a negative factor can flip a large negative
   running product into the new maximum, so we must track both extremes.
2. At each index keep `cur_max` and `cur_min` — the max/min product of any
   subarray ending here. A new value `x` can start fresh, extend the old max,
   or extend the old min (if x is negative, min * x becomes the new max).
3. So for each x: candidates are x, cur_max * x, and cur_min * x. Update
   cur_max / cur_min to the max / min of those three.
4. Track a global answer as the largest cur_max seen. Zeros reset both
   runners to 0 via the `x` candidate, which is correct.
5. Single-pass, constant extra memory — no need for a full DP array.

Complexity: O(n) time, O(1) extra space.
"""

from __future__ import annotations

from typing import List


class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        """Return the largest product of any contiguous non-empty subarray."""
        if not nums:
            return 0

        best = cur_max = cur_min = nums[0]
        for x in nums[1:]:
            # Negatives swap roles of max and min; evaluate all three candidates.
            candidates = (x, cur_max * x, cur_min * x)
            cur_max = max(candidates)
            cur_min = min(candidates)
            if cur_max > best:
                best = cur_max
        return best


def _demo() -> None:
    sol = Solution()
    cases = [
        ([2, 3, -2, 4], 6),
        ([-2, 0, -1], 0),
        ([-2], -2),
        ([0, 2], 2),
        ([-2, 3, -4], 24),
        ([2, -5, -2, -4, 3], 24),  # [-5,-2,-4] or [-2,-4,3]
        ([1, 2, 3, 4], 24),
        ([-1, -2, -3, 0], 6),
        ([0, 0, 0], 0),
        ([-4, -3], 12),
    ]
    for nums, expected in cases:
        got = sol.maxProduct(nums)
        status = "OK" if got == expected else "FAIL"
        print(f"{status}: nums={nums} -> {got} (expected {expected})")
        assert got == expected, (
            f"152 maxProduct({nums}) returned {got}, expected {expected}"
        )


if __name__ == "__main__":
    _demo()
