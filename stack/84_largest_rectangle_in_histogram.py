"""
LeetCode 84: Largest Rectangle in Histogram
Difficulty: Hard
Topic: Monotonic Stack

Problem
-------
Given an array `heights` where each bar has width 1, return the area of the
largest rectangle that fits entirely inside the histogram.

Example 1:
  Input:  heights = [2, 1, 5, 6, 2, 3]
  Output: 10   (bars 5 and 6, height 5, width 2)

Example 2:
  Input:  heights = [2, 4]
  Output: 4

Approach (thought process)
--------------------------
1. Brute force: for every pair (i, j), the rectangle's height is the
   minimum bar in between. That's O(n^2) at best, too slow for n = 10^5.
2. Flip the question: for each bar, ask "what is the widest rectangle that
   uses THIS bar as its shortest bar?" It stretches left and right until it
   hits a bar strictly shorter than itself. So we need, for every bar, the
   nearest shorter bar on each side.
3. A stack of indices with increasing heights gives both at once. Walk left
   to right. When the current bar is shorter than the bar on top of the
   stack, the top bar has just found its right boundary (the current
   index). Its left boundary is whatever is under it on the stack, because
   everything between was popped earlier for being taller. Pop it, compute
   height * (right - left - 1), and keep popping while the current bar is
   still shorter.
4. Append a sentinel bar of height 0 at the end so every remaining bar gets
   popped and measured. Use -1 as the "left wall" when the stack is empty.

Why it works: each bar is popped exactly when its first shorter bar to the
right shows up, and at that moment the element beneath it is its first
shorter bar to the left. So every bar is measured at its maximal width, and
the best rectangle must use some bar as its minimum.

Complexity: O(n) time (each index is pushed and popped once), O(n) space.
"""

from __future__ import annotations

from typing import List


class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        """Return the area of the largest rectangle in the histogram."""
        stack: List[int] = []  # indices, heights strictly increasing upward
        best = 0
        for i, h in enumerate(heights + [0]):  # 0 sentinel flushes the stack
            while stack and heights[stack[-1]] >= h:
                height = heights[stack.pop()]
                left = stack[-1] if stack else -1
                best = max(best, height * (i - left - 1))
            stack.append(i)
        return best


def _brute(heights: List[int]) -> int:
    best = 0
    for i in range(len(heights)):
        low = heights[i]
        for j in range(i, len(heights)):
            low = min(low, heights[j])
            best = max(best, low * (j - i + 1))
    return best


def _demo() -> None:
    sol = Solution()
    cases = [
        ([2, 1, 5, 6, 2, 3], 10),
        ([2, 4], 4),
        ([1], 1),
        ([0], 0),
        ([2, 2, 2, 2], 8),
        ([6, 2, 5, 4, 5, 1, 6], 12),
        ([1, 2, 3, 4, 5], 9),
        ([5, 4, 3, 2, 1], 9),
    ]
    for heights, expected in cases:
        got = sol.largestRectangleArea(heights)
        status = "OK" if got == expected else "FAIL"
        print(f"{status}: largestRectangleArea({heights}) -> {got} (expected {expected})")
        assert got == expected, f"84 returned {got} for {heights}, expected {expected}"

    import random

    rng = random.Random(84)
    for _ in range(300):
        arr = [rng.randint(0, 10) for _ in range(rng.randint(1, 12))]
        assert sol.largestRectangleArea(arr) == _brute(arr), arr
    print("OK: 300 random cases match brute force")


if __name__ == "__main__":
    _demo()
