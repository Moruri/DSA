"""
LeetCode 238: Product of Array Except Self
Link: https://leetcode.com/problems/product-of-array-except-self/
Difficulty: Medium
Topic: Arrays / Prefix Products

Problem
-------
Given an integer array nums, return an array answer such that answer[i] is
equal to the product of all the elements of nums except nums[i].

The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit
integer. You must write an algorithm that runs in O(n) time and without using
the division operation.

Example 1:
  Input:  nums = [1, 2, 3, 4]
  Output: [24, 12, 8, 6]

Example 2:
  Input:  nums = [-1, 1, 0, -3, 3]
  Output: [0, 0, 9, 0, 0]

Approach (thought process)
--------------------------
1. Division is banned, so we cannot compute the full product and divide by
   nums[i]. Brute force multiplying everything except i is O(n²).
2. For index i the answer is (product of everything left of i) times
   (product of everything right of i). Those two sides are independent.
3. First pass left → right: build answer[i] = product of nums[0..i-1]
   (the left product). Seed with 1 so answer[0]'s left product is empty = 1.
4. Second pass right → left: keep a running right product. Multiply
   answer[i] by that right product, then fold nums[i] into the running right.
5. One output array plus a scalar for the right product meets the O(1) extra
   space follow-up (the output itself does not count as extra).

Complexity: O(n) time, O(1) extra space beyond the output array.
"""

from __future__ import annotations

from typing import List


class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        """Return products of all elements except the one at each index."""
        n = len(nums)
        answer = [1] * n

        left = 1
        for i in range(n):
            answer[i] = left
            left *= nums[i]

        right = 1
        for i in range(n - 1, -1, -1):
            answer[i] *= right
            right *= nums[i]

        return answer


def _demo() -> None:
    sol = Solution()
    cases = [
        ([1, 2, 3, 4], [24, 12, 8, 6]),
        ([-1, 1, 0, -3, 3], [0, 0, 9, 0, 0]),
        ([2, 3], [3, 2]),
        ([5], [1]),
        ([0, 0], [0, 0]),
        ([1, 0, 2], [0, 2, 0]),
    ]
    for nums, expected in cases:
        got = sol.productExceptSelf(nums)
        status = "OK" if got == expected else "FAIL"
        print(f"{status}: nums={nums} -> {got} (expected {expected})")
        assert got == expected, (
            f"238 productExceptSelf({nums}) returned {got}, expected {expected}"
        )


if __name__ == "__main__":
    _demo()
