"""
LeetCode 57: Insert Interval
Difficulty: Medium
Topic: Intervals / Linear Sweep

Problem
-------
You are given a list of non-overlapping intervals sorted by start, and one
new interval. Insert the new interval so the list stays sorted and
non-overlapping, merging wherever it overlaps. Touching endpoints count as
overlapping here ([1, 5] and [5, 7] become [1, 7]).

Examples:
  intervals = [[1, 3], [6, 9]], newInterval = [2, 5]  ->  [[1, 5], [6, 9]]
  intervals = [[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], newInterval = [4, 8]
      ->  [[1, 2], [3, 10], [12, 16]]

Approach (thought process)
--------------------------
1. The input is already sorted and already clean, so we do not need to sort
   and re-merge everything like in Merge Intervals (56). Only the stretch of
   intervals that touches the new one can change.
2. That means the list splits into three zones relative to new = [s, e]:
     a) intervals that end before s  -> completely to the left, copy as is
     b) intervals that start at or before e (and end at or after s)
        -> they overlap the new one, so absorb them by widening it:
           s = min(s, start), e = max(e, end)
     c) everything after that         -> completely to the right, copy as is
3. Walk once with a single index: drain zone (a), absorb zone (b), append the
   widened interval, then copy zone (c). Each interval is looked at once.

Why it works: because the intervals are sorted and disjoint, the ones that
overlap [s, e] form one contiguous block. Anything before that block ends
before s and anything after starts after e, so neither can be affected, and
merging the block into one interval is exactly the union of what overlaps.

Complexity:
  - Time: O(n), one pass (no sorting needed).
  - Space: O(n) for the output list.
"""

from typing import List


class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        res: List[List[int]] = []
        s, e = newInterval
        i, n = 0, len(intervals)

        # Zone a: strictly to the left of the new interval.
        while i < n and intervals[i][1] < s:
            res.append(intervals[i])
            i += 1

        # Zone b: overlaps (touching counts), so absorb it into [s, e].
        while i < n and intervals[i][0] <= e:
            s = min(s, intervals[i][0])
            e = max(e, intervals[i][1])
            i += 1
        res.append([s, e])

        # Zone c: strictly to the right.
        res.extend(intervals[i:])
        return res


def _brute(intervals: List[List[int]], new: List[int]) -> List[List[int]]:
    items = sorted(intervals + [new])
    merged: List[List[int]] = []
    for a, b in items:
        if merged and a <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    return merged


def _random_clean(rng) -> List[List[int]]:
    out, cur = [], rng.randint(0, 3)
    for _ in range(rng.randint(0, 6)):
        a = cur + rng.randint(1, 3)
        b = a + rng.randint(0, 3)
        out.append([a, b])
        cur = b
    return out


if __name__ == "__main__":
    import random

    sol = Solution()
    assert sol.insert([[1, 3], [6, 9]], [2, 5]) == [[1, 5], [6, 9]]
    assert sol.insert([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]) == [[1, 2], [3, 10], [12, 16]]
    assert sol.insert([], [5, 7]) == [[5, 7]]
    assert sol.insert([[1, 5]], [6, 8]) == [[1, 5], [6, 8]]
    assert sol.insert([[1, 5]], [5, 7]) == [[1, 7]]
    assert sol.insert([[3, 5]], [0, 1]) == [[0, 1], [3, 5]]

    rng = random.Random(57)
    for _ in range(1000):
        ints = _random_clean(rng)
        a = rng.randint(0, 25)
        new = [a, a + rng.randint(0, 8)]
        assert sol.insert([x[:] for x in ints], new[:]) == _brute(ints, new), (ints, new)
    print("All tests passed for 57.")
