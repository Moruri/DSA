"""
LeetCode 239: Sliding Window Maximum
Difficulty: Hard
Topic: Sliding Window / Monotonic Deque

Problem
-------
You are given an array of integers `nums` and an integer `k` representing
a sliding window of size `k` moving from left to right across the array.
Return an array of the maximum value in each window.

Example 1:
  Input:  nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3
  Output: [3, 3, 5, 5, 6, 7]

Example 2:
  Input:  nums = [1], k = 1
  Output: [1]

Approach (thought process)
--------------------------
1. Recomputing `max` over every window is O(n·k). We need each index to
   contribute work that does not grow with `k`.
2. Inside a window only candidates that could still be the max matter.
   Keep a deque of indices in *decreasing* value order: the front is always
   the current window's maximum.
3. For each new index `i`:
   - Drop indices from the front that fell out of `[i - k + 1, i]`.
   - Drop from the back while `nums[back] <= nums[i]` — they can never beat
     `i` in any future window that still contains them.
   - Append `i`. When `i >= k - 1`, record `nums[front]` as the answer.
4. Each index is pushed and popped at most once, so the whole scan is linear.

Complexity: O(n) time, O(k) extra space for the deque.
"""

from __future__ import annotations

from collections import deque
from typing import List


class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        """Return the max of every contiguous window of length k."""
        if not nums or k <= 0:
            return []
        n = len(nums)
        if k == 1:
            return list(nums)

        dq: deque[int] = deque()  # indices, values decreasing front → back
        out: List[int] = []

        for i, val in enumerate(nums):
            while dq and dq[0] <= i - k:
                dq.popleft()
            while dq and nums[dq[-1]] <= val:
                dq.pop()
            dq.append(i)
            if i >= k - 1:
                out.append(nums[dq[0]])

        # Silence unused-n warning if static checkers care; n is for clarity.
        assert len(out) == n - k + 1
        return out


def _demo() -> None:
    sol = Solution()
    cases = [
        ([1, 3, -1, -3, 5, 3, 6, 7], 3, [3, 3, 5, 5, 6, 7]),
        ([1], 1, [1]),
        ([1, -1], 1, [1, -1]),
        ([9, 11], 2, [11]),
        ([4, -2], 2, [4]),
        ([7, 2, 4], 2, [7, 4]),
        ([1, 3, 1, 2, 0, 5], 3, [3, 3, 2, 5]),
    ]
    for nums, k, expected in cases:
        got = sol.maxSlidingWindow(nums, k)
        status = "OK" if got == expected else "FAIL"
        print(f"{status}: maxSlidingWindow({nums}, {k}) -> {got} (expected {expected})")
        assert got == expected, (
            f"239 maxSlidingWindow({nums}, {k}) returned {got}, expected {expected}"
        )


if __name__ == "__main__":
    _demo()
