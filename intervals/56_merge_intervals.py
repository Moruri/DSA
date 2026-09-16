"""
LeetCode 56: Merge Intervals
Link: https://leetcode.com/problems/merge-intervals/
Difficulty: Medium
Topic: Intervals / Sorting

Problem
-------
Given an array of intervals where intervals[i] = [start_i, end_i], merge all
overlapping intervals and return an array of the non-overlapping intervals
that cover all the intervals in the input.

Example 1:
  Input:  intervals = [[1, 3], [2, 6], [8, 10], [15, 18]]
  Output: [[1, 6], [8, 10], [15, 18]]
  Explanation: [1, 3] and [2, 6] overlap, so they merge into [1, 6].

Example 2:
  Input:  intervals = [[1, 4], [4, 5]]
  Output: [[1, 5]]
  Explanation: Intervals that merely touch ([1, 4] and [4, 5]) are considered
  overlapping.

Approach (thought process)
--------------------------
1. Brute force: repeatedly scan for any pair of overlapping intervals and
   merge them until no pair overlaps. That is O(n^2) per pass and up to n
   passes — far too slow for n up to 10^4.
2. Key observation: if the intervals are sorted by start, then an interval can
   only overlap with the *last* merged interval. Anything earlier already
   ended before the last merged interval started (otherwise it would have been
   merged into it), so there is nothing to look back at.
3. Sort by start. Keep an output list `merged`. For each interval [s, e]:
   - if `merged` is empty or the last merged interval ends before `s`
     (strictly: last_end < s), there is a gap — append [s, e] as a new block;
   - otherwise they overlap or touch — extend the last block's end to
     max(last_end, e). Taking the max matters because the current interval
     may be fully contained (e.g. [1, 10] followed by [2, 3]).
4. Touching intervals like [1, 4] and [4, 5] must merge, so the gap test uses
   `<` rather than `<=`.
5. A single left-to-right pass after sorting handles everything, and the
   output is naturally sorted and non-overlapping.

Complexity: O(n log n) time (dominated by the sort), O(n) space for the output
(O(1) extra beyond that if the sort is in place).
"""

from __future__ import annotations

from typing import List


class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        """Merge overlapping/touching intervals; returns them sorted by start."""
        if not intervals:
            return []

        intervals.sort(key=lambda iv: iv[0])
        merged: List[List[int]] = [list(intervals[0])]

        for start, end in intervals[1:]:
            last = merged[-1]
            if start > last[1]:
                # Gap between the last merged block and this interval: start a new block.
                merged.append([start, end])
            else:
                # Overlap or touch: absorb into the last block (max guards containment).
                last[1] = max(last[1], end)

        return merged


def _brute_force(intervals: List[List[int]]) -> List[List[int]]:
    """O(n^2)-per-pass reference: keep merging any overlapping pair until stable."""
    result = [list(iv) for iv in intervals]
    changed = True
    while changed:
        changed = False
        for i in range(len(result)):
            for j in range(i + 1, len(result)):
                a, b = result[i], result[j]
                if a[0] <= b[1] and b[0] <= a[1]:
                    result[i] = [min(a[0], b[0]), max(a[1], b[1])]
                    result.pop(j)
                    changed = True
                    break
            if changed:
                break
    return sorted(result)


def _demo() -> None:
    sol = Solution()
    cases = [
        ([[1, 3], [2, 6], [8, 10], [15, 18]], [[1, 6], [8, 10], [15, 18]]),
        # Touching intervals must merge.
        ([[1, 4], [4, 5]], [[1, 5]]),
        ([], []),
        ([[1, 4]], [[1, 4]]),
        # Unsorted input.
        ([[4, 7], [1, 4]], [[1, 7]]),
        # Fully contained interval: end must not shrink.
        ([[1, 10], [2, 3], [4, 5]], [[1, 10]]),
        # Everything collapses into one block.
        ([[1, 4], [0, 4]], [[0, 4]]),
        ([[1, 4], [0, 0]], [[0, 0], [1, 4]]),
        # Nothing overlaps.
        ([[1, 2], [3, 4], [5, 6]], [[1, 2], [3, 4], [5, 6]]),
        # Duplicates.
        ([[1, 3], [1, 3], [1, 3]], [[1, 3]]),
    ]
    for intervals, expected in cases:
        got = sol.merge([list(iv) for iv in intervals])
        status = "OK" if got == expected else "FAIL"
        print(f"{status}: intervals={intervals} -> {got} (expected {expected})")
        assert got == expected, f"56 merge({intervals}) returned {got}, expected {expected}"

    # Randomised cross-check against the brute-force reference.
    import random

    rng = random.Random(56)
    for _ in range(200):
        n = rng.randint(0, 12)
        intervals = []
        for _ in range(n):
            s = rng.randint(0, 30)
            intervals.append([s, s + rng.randint(0, 8)])
        got = sol.merge([list(iv) for iv in intervals])
        assert got == _brute_force(intervals), f"mismatch on {intervals}"
        # Output invariants: sorted and strictly separated.
        for a, b in zip(got, got[1:]):
            assert a[1] < b[0], f"output not disjoint for {intervals}: {got}"
    print("OK: 200 random cases match the brute-force reference")


if __name__ == "__main__":
    _demo()
