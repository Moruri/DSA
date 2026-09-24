"""
LeetCode 42: Trapping Rain Water
Link: https://leetcode.com/problems/trapping-rain-water/
Difficulty: Hard
Topic: Two Pointers

Problem
-------
Given n non-negative integers representing an elevation map where the width
of each bar is 1, compute how much water it can trap after raining.

Example 1:
  Input:  height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
  Output: 6
  Explanation: Water fills the valleys between the bars for a total of 6 units.

Example 2:
  Input:  height = [4, 2, 0, 3, 2, 5]
  Output: 9

Approach (thought process)
--------------------------
1. Water above index i is limited by the shorter of the tallest bars to its
   left and to its right: trapped[i] = max(0, min(left_max[i], right_max[i])
   - height[i]). Precomputing both max arrays is O(n) time and O(n) space.
2. A monotonic decreasing stack of indices works too: when a taller bar
   arrives, pop and add the water trapped between the new bar and the new
   stack top. Also O(n) time / O(n) space.
3. Two pointers give the same answer in O(1) extra space. Maintain lo/hi and
   left_max/right_max. The side with the smaller running max is the limiting
   wall for that index, so we can safely accumulate water there and advance
   that pointer.
4. Invariant: water under the shorter wall cannot be blocked by anything on
   the other side (the other side's max is at least as tall). Advance until
   lo and hi meet; sum is the answer.
5. Empty or single-bar maps trap nothing.

Complexity: O(n) time, O(1) extra space.
"""

from __future__ import annotations

from typing import List


class Solution:
    def trap(self, height: List[int]) -> int:
        """Return how many units of rain water the elevation map can trap."""
        n = len(height)
        if n < 3:
            return 0

        lo, hi = 0, n - 1
        left_max = right_max = 0
        water = 0

        while lo < hi:
            h_lo, h_hi = height[lo], height[hi]
            if h_lo <= h_hi:
                if h_lo >= left_max:
                    left_max = h_lo
                else:
                    water += left_max - h_lo
                lo += 1
            else:
                if h_hi >= right_max:
                    right_max = h_hi
                else:
                    water += right_max - h_hi
                hi -= 1

        return water


def _demo() -> None:
    sol = Solution()
    cases = [
        ([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], 6),
        ([4, 2, 0, 3, 2, 5], 9),
        ([0], 0),
        ([], 0),
        ([1, 2], 0),
        ([2, 0, 2], 2),
        ([5, 4, 1, 2], 1),
        ([4, 2, 3], 1),
    ]
    for height, expected in cases:
        got = sol.trap(height)
        status = "OK" if got == expected else "FAIL"
        print(f"{status}: height={height} -> {got} (expected {expected})")
        assert got == expected, (
            f"42 trap({height}) returned {got}, expected {expected}"
        )


if __name__ == "__main__":
    _demo()
