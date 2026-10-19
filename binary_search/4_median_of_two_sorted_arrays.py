"""
LeetCode 4: Median of Two Sorted Arrays
Difficulty: Hard
Topic: Binary Search / Partition Search

Problem
-------
Given two sorted arrays nums1 (size m) and nums2 (size n), return the median
of the two arrays combined. The overall run time must be O(log(m + n)).

Examples:
  nums1 = [1, 3],    nums2 = [2]      ->  2.0
  nums1 = [1, 2],    nums2 = [3, 4]   ->  2.5

Approach (thought process)
--------------------------
1. Merging both arrays and picking the middle is O(m + n). That works, but
   the problem asks for a logarithmic bound, so we must avoid touching every
   element.
2. Reframe the median: it splits the combined sorted list into a LEFT half
   and a RIGHT half of equal size (left gets the extra element when the total
   is odd), with every left value <= every right value.
3. If we take i elements from nums1 for the left half, the left half needs
   half = (m + n + 1) // 2 elements in total, so we must take j = half - i
   from nums2. Choosing i fixes j. The whole problem becomes "find the right
   i", a single number in the range 0..m.
4. A cut is valid when the borders cross correctly:
       nums1[i-1] <= nums2[j]   and   nums2[j-1] <= nums1[i]
   (Inside each array order is already guaranteed; only the cross-pairs need
   checking.) Missing neighbours at the edges count as -inf / +inf.
5. If nums1[i-1] > nums2[j], we took too many from nums1, so move i left.
   Otherwise if nums2[j-1] > nums1[i], we took too few, so move i right.
   That monotonic "too many / too few" signal is exactly what binary search
   needs.
6. Once valid: odd total -> median is max(left borders); even total ->
   average of max(left borders) and min(right borders).
7. Binary search over the SHORTER array so j never goes negative and the
   cost is O(log(min(m, n))).

Why it works: as i grows, nums1[i-1] grows and nums2[j] shrinks (j falls),
so the condition "nums1[i-1] <= nums2[j]" is true for small i and false past
some point. Binary search finds the boundary, and at that boundary the other
condition holds as well.

Complexity:
  - Time: O(log(min(m, n))).
  - Space: O(1).
"""

from typing import List


class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        a, b = nums1, nums2
        if len(a) > len(b):
            a, b = b, a                    # search over the shorter array
        m, n = len(a), len(b)
        half = (m + n + 1) // 2
        lo, hi = 0, m
        NEG, POS = float("-inf"), float("inf")

        while lo <= hi:
            i = (lo + hi) // 2             # elements taken from a
            j = half - i                   # elements taken from b
            a_left = a[i - 1] if i > 0 else NEG
            a_right = a[i] if i < m else POS
            b_left = b[j - 1] if j > 0 else NEG
            b_right = b[j] if j < n else POS

            if a_left > b_right:
                hi = i - 1                 # too many from a
            elif b_left > a_right:
                lo = i + 1                 # too few from a
            else:
                left_max = max(a_left, b_left)
                if (m + n) % 2:
                    return float(left_max)
                return (left_max + min(a_right, b_right)) / 2

        raise ValueError("inputs must be sorted")


if __name__ == "__main__":
    import random
    import statistics

    sol = Solution()
    assert sol.findMedianSortedArrays([1, 3], [2]) == 2.0
    assert sol.findMedianSortedArrays([1, 2], [3, 4]) == 2.5
    assert sol.findMedianSortedArrays([], [1]) == 1.0
    assert sol.findMedianSortedArrays([2], []) == 2.0
    assert sol.findMedianSortedArrays([1, 1, 1], [1, 1]) == 1.0

    for _ in range(2000):
        x = sorted(random.randint(-50, 50) for _ in range(random.randint(0, 8)))
        y = sorted(random.randint(-50, 50) for _ in range(random.randint(0, 8)))
        if not x and not y:
            continue
        assert sol.findMedianSortedArrays(x, y) == statistics.median(x + y), (x, y)
    print("All tests passed for 4. Median of Two Sorted Arrays")
