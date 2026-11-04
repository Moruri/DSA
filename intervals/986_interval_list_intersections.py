"""
LeetCode 986: Interval List Intersections
Difficulty: Medium
Topic: Intervals / Two Pointers

Problem
-------
Given two lists of closed intervals, each pairwise disjoint and sorted, return
the intersection of the two lists.

Approach (thought process)
--------------------------
1. Both lists are already sorted, so this is a merge-style walk, like merging
   two sorted arrays: one pointer i into A, one pointer j into B.
2. Two intervals [a1, a2] and [b1, b2] overlap on
       lo = max(a1, b1), hi = min(a2, b2)
   and that overlap is real whenever lo <= hi (closed intervals, so a single
   shared point like [5, 5] counts).
3. Which pointer advances? The interval that ends first. It can't overlap
   anything later in the other list, because everything later there starts
   after the current one, which already reaches at least as far. The
   interval that ends later might still overlap the next one, so keep it.
4. Stop when either list runs out; nothing more can intersect.

Why it works: each step either records the only possible overlap between
the two current intervals or proves one of them is finished, so no overlap is
missed and none is counted twice.

Complexity:
  - Time: O(m + n), each pointer only moves forward.
  - Space: O(1) extra beyond the output.
"""

from typing import List


class Solution:
    def intervalIntersection(self, A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
        i = j = 0
        out: List[List[int]] = []
        while i < len(A) and j < len(B):
            lo = max(A[i][0], B[j][0])
            hi = min(A[i][1], B[j][1])
            if lo <= hi:
                out.append([lo, hi])
            if A[i][1] < B[j][1]:
                i += 1
            else:
                j += 1
        return out


def _demo() -> None:
    sol = Solution()
    cases = [
        (
            [[0, 2], [5, 10], [13, 23], [24, 25]],
            [[1, 5], [8, 12], [15, 24], [25, 26]],
            [[1, 2], [5, 5], [8, 10], [15, 23], [24, 24], [25, 25]],
        ),
        ([[1, 3], [5, 9]], [], []),
        ([[1, 7]], [[3, 10]], [[3, 7]]),
        ([[1, 2]], [[3, 4]], []),
    ]
    for A, B, expected in cases:
        got = sol.intervalIntersection(A, B)
        print(f"{'OK' if got == expected else 'FAIL'}: {A} & {B} -> {got}")
        assert got == expected, f"986 returned {got}, expected {expected}"


if __name__ == "__main__":
    _demo()
