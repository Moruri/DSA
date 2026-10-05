"""
LeetCode 435: Non-overlapping Intervals
Difficulty: Medium
Topic: Intervals / Greedy

Problem
-------
Given an array of `intervals` where intervals[i] = [start, end], return the
minimum number of intervals you need to remove so the rest don't overlap.
Intervals that only touch at a point (like [1, 2] and [2, 3]) do NOT
overlap.

Example 1:
  Input:  intervals = [[1, 2], [2, 3], [3, 4], [1, 3]]
  Output: 1   (remove [1, 3])

Example 2:
  Input:  intervals = [[1, 2], [1, 2], [1, 2]]
  Output: 2

Approach (thought process)
--------------------------
1. "Remove the fewest" is the same as "keep the most". Keeping the maximum
   number of non-overlapping intervals is the classic activity-selection
   problem, so answer = len(intervals) - kept.
2. Greedy choice: sort by END time. Always keep the interval that finishes
   earliest, because it leaves the most room for everything after it.
3. Walk the sorted list with `prev_end`. If the next interval starts at or
   after `prev_end`, it fits: keep it and move `prev_end` to its end.
   Otherwise it overlaps something we already kept, so count it as removed.

Why it works (exchange argument): take any optimal set of kept intervals.
Its first interval ends no earlier than the one with the smallest end, so
swapping that one in never causes a new overlap. Repeating the argument on
the rest shows the greedy keeps at least as many as any optimal answer.

Why not sort by start? Then one long interval that starts early would be
kept and block many short ones; sorting by end avoids that trap.

Complexity: O(n log n) time for the sort, O(1) extra space beyond it.
"""

from __future__ import annotations

from itertools import combinations
from typing import List


class Solution:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        """Return the minimum removals so no two intervals overlap."""
        if not intervals:
            return 0
        intervals = sorted(intervals, key=lambda iv: iv[1])
        removed = 0
        prev_end = intervals[0][1]
        for start, end in intervals[1:]:
            if start >= prev_end:
                prev_end = end  # fits after the last kept interval
            else:
                removed += 1  # overlaps; drop it (it ends later, so it's worse)
        return removed


def _brute(intervals: List[List[int]]) -> int:
    n = len(intervals)
    for keep in range(n, 0, -1):
        for combo in combinations(sorted(intervals), keep):
            if all(combo[i][1] <= combo[i + 1][0] for i in range(keep - 1)):
                return n - keep
    return n


def _demo() -> None:
    sol = Solution()
    cases = [
        ([[1, 2], [2, 3], [3, 4], [1, 3]], 1),
        ([[1, 2], [1, 2], [1, 2]], 2),
        ([[1, 2], [2, 3]], 0),
        ([[1, 100], [11, 22], [1, 11], [2, 12]], 2),
        ([[0, 2], [1, 3], [2, 4], [3, 5], [4, 6]], 2),
        ([[-52, 31], [-73, -26], [82, 97], [-65, -11], [-62, -49], [95, 99], [58, 95], [-31, 49], [66, 98], [-63, 2], [30, 47], [-40, -26]], 7),
    ]
    for intervals, expected in cases:
        got = sol.eraseOverlapIntervals(intervals)
        status = "OK" if got == expected else "FAIL"
        print(f"{status}: eraseOverlapIntervals({intervals}) -> {got} (expected {expected})")
        assert got == expected, f"435 returned {got} for {intervals}, expected {expected}"

    import random

    rng = random.Random(435)
    for _ in range(200):
        ivs = []
        for _ in range(rng.randint(1, 8)):
            a = rng.randint(0, 15)
            ivs.append([a, a + rng.randint(1, 6)])
        assert sol.eraseOverlapIntervals(ivs) == _brute(ivs), ivs
    print("OK: 200 random cases match brute force")


if __name__ == "__main__":
    _demo()
