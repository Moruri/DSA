"""
LeetCode 153: Find Minimum in Rotated Sorted Array
Difficulty: Medium
Topic: Binary Search / Rotation Pivot

Problem
-------
A sorted array of unique values was rotated some number of times
(e.g. [0,1,2,4,5,6,7] -> [4,5,6,7,0,1,2]). Return its minimum in O(log n).

Approach (thought process)
--------------------------
1. A rotated sorted array is two sorted runs: a "high" run followed by a
   "low" run. The minimum is the first element of the low run, the pivot.
2. Compare the middle element with the RIGHT end, nums[hi]:
     - nums[mid] > nums[hi]: mid sits in the high run, so the drop (and the
       minimum) is strictly to the right. Set lo = mid + 1.
     - nums[mid] < nums[hi]: mid..hi is sorted, so mid itself could be the
       minimum but nothing right of it is smaller. Set hi = mid.
3. Stop when lo == hi; that index is the minimum.
4. Why the right end and not the left? nums[hi] always belongs to the low
   run (or the array is unrotated, which behaves the same), so the
   comparison never becomes ambiguous. Comparing with nums[lo] breaks on
   the unrotated case, where you'd wrongly move right.

Why it works: the invariant "the minimum is inside [lo, hi]" holds after each
step, and the range shrinks every iteration, so it converges on the minimum.

Complexity:
  - Time: O(log n).
  - Space: O(1).
"""

from typing import List


class Solution:
    def findMin(self, nums: List[int]) -> int:
        lo, hi = 0, len(nums) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if nums[mid] > nums[hi]:
                lo = mid + 1
            else:
                hi = mid
        return nums[lo]


def _demo() -> None:
    sol = Solution()
    cases = [
        ([3, 4, 5, 1, 2], 1),
        ([4, 5, 6, 7, 0, 1, 2], 0),
        ([11, 13, 15, 17], 11),  # not rotated
        ([2, 1], 1),
        ([7], 7),
    ]
    for nums, expected in cases:
        got = sol.findMin(nums)
        print(f"{'OK' if got == expected else 'FAIL'}: {nums} -> {got} (expected {expected})")
        assert got == expected, f"153 findMin({nums}) returned {got}, expected {expected}"


if __name__ == "__main__":
    _demo()
