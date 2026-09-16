"""
LeetCode 215: Kth Largest Element in an Array
Link: https://leetcode.com/problems/kth-largest-element-in-an-array/
Difficulty: Medium
Topic: Heaps / Quickselect

Problem
-------
Given an integer array nums and an integer k, return the k-th largest element
in the array. Note that it is the k-th largest element in sorted order, not
the k-th distinct element. Can you solve it without sorting?

Example 1:
  Input:  nums = [3, 2, 1, 5, 6, 4], k = 2
  Output: 5

Example 2:
  Input:  nums = [3, 2, 3, 1, 2, 4, 5, 5, 6], k = 4
  Output: 4

Approach (thought process)
--------------------------
1. Simplest: sort descending and index k-1. O(n log n) time. Correct, but the
   prompt asks for something better than a full sort — we only need one order
   statistic, not the whole ordering.
2. Min-heap of size k. Push each element; whenever the heap grows past k
   elements, pop the smallest. After the pass the heap holds exactly the k
   largest values, and its root (the smallest of those) is the k-th largest.
   Each push/pop is O(log k), so the total is O(n log k) with O(k) extra space
   — a big win when k is much smaller than n, and it streams (works on data
   that does not fit in memory).
3. Small optimisation: seed the heap with the first k elements via heapify
   (O(k)), then for the remaining elements use heapq.heappushpop, which only
   does the push if the new value beats the current root. Equivalent result,
   fewer heap operations.
4. Alternative — Quickselect: pick a pivot, partition into (> pivot, == pivot,
   < pivot), and recurse only into the part that contains the k-th largest.
   Expected O(n) time (O(n^2) worst case, avoided in practice by a random
   pivot), O(1) extra space if done in place. It is the asymptotically best
   answer, but the heap version is shorter, deterministic, and what most
   interviewers expect first; mention quickselect as the follow-up.
5. Python's heapq.nlargest(k, nums)[-1] is the same min-heap idea in one line.

Complexity (heap): O(n log k) time, O(k) extra space.
Complexity (quickselect): O(n) expected time, O(1) extra space (in place).
"""

from __future__ import annotations

import heapq
import random
from typing import List


class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        """Return the k-th largest element using a min-heap of size k."""
        # The heap always holds the k largest values seen so far; its root is
        # the smallest of them, i.e. the current k-th largest.
        heap = nums[:k]
        heapq.heapify(heap)
        for num in nums[k:]:
            if num > heap[0]:
                heapq.heapreplace(heap, num)
        return heap[0]

    def findKthLargestQuickselect(self, nums: List[int], k: int) -> int:
        """Alternative: expected-O(n) quickselect with three-way partitioning."""
        target = k  # rank counted from the largest (1 = maximum)
        candidates = nums
        while True:
            pivot = random.choice(candidates)
            greater = [x for x in candidates if x > pivot]
            equal = [x for x in candidates if x == pivot]
            if target <= len(greater):
                candidates = greater
            elif target <= len(greater) + len(equal):
                return pivot
            else:
                target -= len(greater) + len(equal)
                candidates = [x for x in candidates if x < pivot]


def _reference(nums: List[int], k: int) -> int:
    """O(n log n) full-sort reference used to cross-check in the demo."""
    return sorted(nums, reverse=True)[k - 1]


def _demo() -> None:
    sol = Solution()
    cases = [
        ([3, 2, 1, 5, 6, 4], 2, 5),
        ([3, 2, 3, 1, 2, 4, 5, 5, 6], 4, 4),
        # k = 1 is the maximum; k = n is the minimum.
        ([7], 1, 7),
        ([2, 1], 1, 2),
        ([2, 1], 2, 1),
        # Duplicates count separately (k-th largest, not k-th distinct).
        ([5, 5, 5, 5], 3, 5),
        ([1, 1, 2, 2, 3, 3], 3, 2),
        # Negatives.
        ([-1, -5, -3, -2], 2, -2),
    ]
    for nums, k, expected in cases:
        got = sol.findKthLargest(list(nums), k)
        got_qs = sol.findKthLargestQuickselect(list(nums), k)
        status = "OK" if got == expected == got_qs else "FAIL"
        print(f"{status}: nums={nums}, k={k} -> heap={got}, quickselect={got_qs} (expected {expected})")
        assert got == expected, f"215 findKthLargest({nums}, {k}) returned {got}, expected {expected}"
        assert got_qs == expected, f"215 quickselect({nums}, {k}) returned {got_qs}, expected {expected}"

    # Randomised cross-check of both methods against a full sort.
    rng = random.Random(215)
    for _ in range(300):
        n = rng.randint(1, 40)
        nums = [rng.randint(-20, 20) for _ in range(n)]
        k = rng.randint(1, n)
        expected = _reference(nums, k)
        assert sol.findKthLargest(list(nums), k) == expected, f"heap mismatch on {nums}, k={k}"
        assert sol.findKthLargestQuickselect(list(nums), k) == expected, f"quickselect mismatch on {nums}, k={k}"
        assert heapq.nlargest(k, nums)[-1] == expected
    print("OK: 300 random cases match the full-sort reference (heap, quickselect, nlargest)")


if __name__ == "__main__":
    _demo()
