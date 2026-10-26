"""
LeetCode 213: House Robber II
Difficulty: Medium
Topic: Dynamic Programming (circular array)

Problem
-------
Houses sit in a circle, each holding nums[i] money. Robbing two adjacent
houses trips the alarm, and because the street is a circle the first and
last houses are neighbours too. Return the most money you can rob.

Example:
  [2, 3, 2]    -> 3   (can't take both 2s, they touch around the circle)
  [1, 2, 3, 1] -> 4   (1 + 3)

Approach (thought process)
--------------------------
1. Without the circle this is plain House Robber (198): walk the street
   keeping two numbers, the best total up to the previous house and up to
   the one before it. At each house: best = max(skip it, rob it + best two
   back).
2. The circle adds exactly one extra conflict: house 0 vs house n-1. In any
   valid plan at least one of them is left alone.
3. So split into two linear problems: rob houses 0..n-2 (last one excluded)
   or houses 1..n-1 (first one excluded). Every valid circular plan lives in
   at least one of these, and every plan in either one is valid on the
   circle. Answer = max of the two.
4. Edge case: a single house has no neighbour conflict with itself, so the
   answer is nums[0] (both slices would be empty otherwise).

Why it works: breaking the circle at the one edge that differs from the
linear case turns a cyclic constraint into two acyclic ones whose union
covers all legal choices.

Complexity:
  - Time: O(n), two linear passes.
  - Space: O(1), just two rolling variables per pass.
"""

from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        if len(nums) == 1:
            return nums[0]

        def rob_line(houses: List[int]) -> int:
            prev2 = prev1 = 0  # best up to i-2, best up to i-1
            for money in houses:
                prev2, prev1 = prev1, max(prev1, prev2 + money)
            return prev1

        return max(rob_line(nums[:-1]), rob_line(nums[1:]))


if __name__ == "__main__":
    s = Solution()
    cases = [
        ([2, 3, 2], 3),
        ([1, 2, 3, 1], 4),
        ([1, 2, 3], 3),
        ([5], 5),
        ([200, 3, 140, 20, 10], 340),
    ]
    for nums, expected in cases:
        got = s.rob(nums)
        assert got == expected, (nums, got, expected)
        print(f"{nums} -> {got}")
    print("All tests passed.")
