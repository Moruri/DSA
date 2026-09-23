"""
LeetCode 11: Container With Most Water
Link: https://leetcode.com/problems/container-with-most-water/
Difficulty: Medium
Topic: Two Pointers

Problem
-------
You are given an integer array height of length n. There are n vertical lines
drawn such that the two endpoints of the ith line are (i, 0) and (i, height[i]).

Find two lines that together with the x-axis form a container, such that the
container contains the most water.

Return the maximum amount of water a container can store.

Notice that you may not slant the container.

Example 1:
  Input:  height = [1, 8, 6, 2, 5, 4, 8, 3, 7]
  Output: 49
  Explanation: The lines at indices 1 and 8 form a container of area
               min(8, 7) * (8 - 1) = 49.

Example 2:
  Input:  height = [1, 1]
  Output: 1

Approach (thought process)
--------------------------
1. Brute force tries every pair (i, j) and takes max of min(height[i],
   height[j]) * (j - i) — O(n²), too slow for n up to 10^5.
2. The area is limited by the shorter line and by the width between indices.
   Starting at the widest span (lo = 0, hi = n - 1) maximises width first.
3. At each step the current area is a candidate. To beat it we must move a
   pointer: shrinking the width means we need a taller limiting height. The
   only move that can help is advancing the shorter side — the taller side
   alone cannot raise the min.
4. Keep a running max while lo < hi; when heights are equal either pointer
   may advance (both sides are limiting). Each index is visited at most once.
5. Correctness: every potentially optimal pair is considered because any
   discarded shorter pillar could never form a larger area with anything
   remaining inside the current window.

Complexity: O(n) time, O(1) extra space.
"""

from __future__ import annotations

from typing import List


class Solution:
    def maxArea(self, height: List[int]) -> int:
        """Return the maximum water area between two vertical lines."""
        lo, hi = 0, len(height) - 1
        best = 0

        while lo < hi:
            h_lo, h_hi = height[lo], height[hi]
            width = hi - lo
            if h_lo < h_hi:
                area = h_lo * width
                lo += 1
            else:
                area = h_hi * width
                hi -= 1
            if area > best:
                best = area

        return best


def _demo() -> None:
    sol = Solution()
    cases = [
        ([1, 8, 6, 2, 5, 4, 8, 3, 7], 49),
        ([1, 1], 1),
        ([4, 3, 2, 1, 4], 16),
        ([1, 2, 1], 2),
        ([2, 3, 4, 5, 18, 17, 6], 17),
        ([1, 2, 4, 3], 4),
        ([1], 0),
        ([], 0),
    ]
    for height, expected in cases:
        got = sol.maxArea(height)
        status = "OK" if got == expected else "FAIL"
        print(f"{status}: height={height} -> {got} (expected {expected})")
        assert got == expected, (
            f"11 maxArea({height}) returned {got}, expected {expected}"
        )


if __name__ == "__main__":
    _demo()