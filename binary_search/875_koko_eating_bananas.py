"""
LeetCode 875: Koko Eating Bananas
Difficulty: Medium
Topic: Binary Search on the Answer

Problem
-------
Koko has `piles` of bananas and `h` hours before the guards return. Each hour
she picks one pile and eats up to `k` bananas from it (if the pile has fewer
than `k`, she finishes it and waits out the rest of that hour). Return the
minimum integer eating speed `k` that lets her finish every pile within `h`
hours.

Example 1:
  Input:  piles = [3, 6, 7, 11], h = 8
  Output: 4

Example 2:
  Input:  piles = [30, 11, 23, 4, 20], h = 5
  Output: 30

Approach (thought process)
--------------------------
1. We are not searching inside the array; we are searching for a *speed*.
   The answer lives in the range [1, max(piles)]: speed max(piles) always
   works (one hour per pile, and h >= len(piles) is guaranteed), and going
   faster than that never helps.
2. Key observation: feasibility is monotonic. If speed k finishes in time,
   any speed > k also does. So the speeds look like
   [too slow, too slow, ..., OK, OK, OK] and we want the first OK.
3. That shape is exactly what binary search finds. For a candidate k the
   hours needed are sum(ceil(p / k)) over all piles, computed in O(n) with
   the integer trick (p + k - 1) // k.
4. If hours <= h, k works, so the answer is k or smaller: hi = k.
   Otherwise k is too slow: lo = k + 1. Stop when lo == hi.

Why it works: the loop keeps the invariant "the answer is in [lo, hi]";
each step halves that range without ever discarding the first feasible
speed.

Complexity: O(n · log M) time where M = max(piles), O(1) extra space.
"""

from __future__ import annotations

from typing import List


class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        """Return the slowest integer speed that finishes all piles in h hours."""

        def hours_needed(k: int) -> int:
            return sum((p + k - 1) // k for p in piles)

        lo, hi = 1, max(piles)
        while lo < hi:
            mid = (lo + hi) // 2
            if hours_needed(mid) <= h:
                hi = mid  # mid works; maybe something slower works too
            else:
                lo = mid + 1  # mid is too slow
        return lo


def _demo() -> None:
    sol = Solution()
    cases = [
        ([3, 6, 7, 11], 8, 4),
        ([30, 11, 23, 4, 20], 5, 30),
        ([30, 11, 23, 4, 20], 6, 23),
        ([1], 1, 1),
        ([1000000000], 2, 500000000),
        ([312884470], 968709470, 1),
    ]
    for piles, h, expected in cases:
        got = sol.minEatingSpeed(piles, h)
        status = "OK" if got == expected else "FAIL"
        print(f"{status}: minEatingSpeed({piles}, {h}) -> {got} (expected {expected})")
        assert got == expected, f"875 minEatingSpeed({piles}, {h}) returned {got}, expected {expected}"


if __name__ == "__main__":
    _demo()
