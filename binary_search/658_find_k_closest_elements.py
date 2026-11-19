"""
LeetCode 658: Find K Closest Elements
Difficulty: Medium
Topic: Binary Search (on the window's left edge)

Problem
-------
Given a sorted array arr, an integer k and a target x, return the k
integers closest to x, sorted ascending. Closeness is |a - x|; on a tie
the smaller number wins.

Approach (thought process)
--------------------------
1. The answer is always a contiguous window of length k in the sorted
   array (if you take a far element while skipping a nearer one on the
   same side, swapping them is never worse). So the real question is:
   where does the window start? Call that left edge `lo`, in [0, n - k].
2. Compare two neighbouring candidate windows: start at `mid` vs start at
   `mid + 1`. They share everything except arr[mid] (only in the first)
   and arr[mid + k] (only in the second).
   - If x - arr[mid] > arr[mid + k] - x, then arr[mid] is farther than
     arr[mid + k], so the window should slide right: lo = mid + 1.
   - Otherwise (arr[mid] is closer, or tied and smaller) the window
     should start at mid or earlier: hi = mid.
3. This "should I slide right?" answer is monotone (False...False,
   True...True flipped), which is exactly what binary search needs.
   Using signed differences (not abs) matters: it handles the case where
   x lies outside the window, and ties fall to the left automatically.
4. Return arr[lo : lo + k], already sorted.

Complexity
----------
Time:  O(log(n - k) + k), the search plus copying the answer.
Space: O(1) extra besides the output.
"""

from typing import List


class Solution:
    def findClosestElements(self, arr: List[int], k: int, x: int) -> List[int]:
        lo, hi = 0, len(arr) - k
        while lo < hi:
            mid = (lo + hi) // 2
            if x - arr[mid] > arr[mid + k] - x:
                lo = mid + 1
            else:
                hi = mid
        return arr[lo:lo + k]


def brute(arr: List[int], k: int, x: int) -> List[int]:
    return sorted(sorted(arr, key=lambda a: (abs(a - x), a))[:k])


if __name__ == "__main__":
    import random

    sol = Solution()
    assert sol.findClosestElements([1, 2, 3, 4, 5], 4, 3) == [1, 2, 3, 4]
    assert sol.findClosestElements([1, 1, 2, 3, 4, 5], 4, -1) == [1, 1, 2, 3]
    assert sol.findClosestElements([1, 2, 3, 4, 5], 4, 10) == [2, 3, 4, 5]
    assert sol.findClosestElements([1, 3], 1, 2) == [1]  # tie -> smaller
    random.seed(658)
    for _ in range(500):
        arr = sorted(random.randint(-10, 10) for _ in range(random.randint(1, 12)))
        k = random.randint(1, len(arr))
        x = random.randint(-15, 15)
        assert sol.findClosestElements(arr, k, x) == brute(arr, k, x)
    print("All tests passed.")
