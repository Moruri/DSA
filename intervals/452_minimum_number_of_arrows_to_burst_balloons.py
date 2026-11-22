"""
LeetCode 452: Minimum Number of Arrows to Burst Balloons
Difficulty: Medium
Topic: Intervals / Greedy

Problem
-------
Balloons are horizontal intervals [x_start, x_end] on a wall. An arrow shot
straight up at x bursts every balloon with x_start <= x <= x_end. Return the
fewest arrows that burst all balloons.

Approach (thought process)
--------------------------
1. Every balloon needs some arrow inside its interval. The question becomes:
   how few points can "stab" every interval?
2. Look at the balloon that ends first. Some arrow must land at or before its
   end. Shooting exactly at its end is never worse than shooting earlier: it
   still bursts that balloon and reaches as far right as possible, so it hits
   every other balloon that has already started.
3. So sort by end. Shoot at the first end. Skip every balloon whose start is
   <= that arrow (it's already burst). The first balloon that starts after
   the arrow needs a new arrow, placed at its own end. Repeat.
4. Touching counts as overlapping here ([1,2] and [2,3] share x = 2), so the
   new-arrow test is a strict start > arrow.

Why it works: an exchange argument. Any optimal plan's first arrow can be
slid right to the earliest end without losing a balloon, so greedy never
uses more arrows than optimal. (Compare 435 Non-overlapping Intervals: same
sort-by-end greedy, counting the opposite thing.)

Complexity
----------
Time:  O(n log n) for the sort, then one O(n) pass.
Space: O(1) extra beyond the sort.
"""

from typing import List


class Solution:
    def findMinArrowShots(self, points: List[List[int]]) -> int:
        if not points:
            return 0
        points.sort(key=lambda p: p[1])
        arrows = 1
        arrow_x = points[0][1]
        for start, end in points[1:]:
            if start > arrow_x:  # this balloon is out of reach of the last arrow
                arrows += 1
                arrow_x = end
        return arrows


if __name__ == "__main__":
    s = Solution()
    cases = [
        ([[10, 16], [2, 8], [1, 6], [7, 12]], 2),
        ([[1, 2], [3, 4], [5, 6], [7, 8]], 4),
        ([[1, 2], [2, 3], [3, 4], [4, 5]], 2),
        ([[1, 2]], 1),
        ([[-2147483648, 2147483647]], 1),
        ([[1, 10], [2, 3], [4, 5], [6, 7]], 3),
    ]
    for pts, want in cases:
        got = s.findMinArrowShots([p[:] for p in pts])
        assert got == want, (pts, got, want)
        print(f"findMinArrowShots({pts}) = {got}")
    print("All tests passed.")
