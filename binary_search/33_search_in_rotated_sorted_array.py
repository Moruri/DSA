"""
LeetCode 33: Search in Rotated Sorted Array
Difficulty: Medium
Topic: Binary Search

Problem
-------
There is an integer array nums sorted in ascending order with distinct
values. Before being handed to you, nums was possibly rotated at an unknown
pivot index k, so it looks like
  [nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]].

Given the rotated array nums and an integer target, return the index of
target if it is in nums, or -1 if it is not. You must write an algorithm
with O(log n) runtime complexity.

Example 1:
  Input:  nums = [4, 5, 6, 7, 0, 1, 2], target = 0
  Output: 4

Example 2:
  Input:  nums = [4, 5, 6, 7, 0, 1, 2], target = 3
  Output: -1

Example 3:
  Input:  nums = [1], target = 0
  Output: -1

Approach (thought process)
--------------------------
1. A linear scan is O(n) — the problem demands O(log n), which screams
   binary search. But plain binary search needs a fully sorted array.
2. Key observation: whenever you split a rotated sorted array at mid, at
   least one of the two halves [lo..mid] or [mid..hi] is properly sorted.
   Compare nums[lo] <= nums[mid] to tell which one.
3. Once you know a sorted half, you can check in O(1) whether target lies
   inside its value range:
     - left half sorted and nums[lo] <= target < nums[mid]  -> go left
     - right half sorted and nums[mid] < target <= nums[hi] -> go right
   Otherwise, target must be in the other (unsorted) half, so search there.
4. Each step halves the search space, exactly like ordinary binary search.
   Return mid the moment nums[mid] == target; return -1 when lo passes hi.

Complexity: O(log n) time, O(1) extra space.
"""

from __future__ import annotations

from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        """Return the index of target in a rotated sorted array, or -1."""
        lo, hi = 0, len(nums) - 1

        while lo <= hi:
            mid = (lo + hi) // 2
            if nums[mid] == target:
                return mid

            if nums[lo] <= nums[mid]:
                # Left half [lo..mid] is sorted.
                if nums[lo] <= target < nums[mid]:
                    hi = mid - 1
                else:
                    lo = mid + 1
            else:
                # Right half [mid..hi] is sorted.
                if nums[mid] < target <= nums[hi]:
                    lo = mid + 1
                else:
                    hi = mid - 1

        return -1


def _demo() -> None:
    sol = Solution()
    cases = [
        ([4, 5, 6, 7, 0, 1, 2], 0, 4),
        ([4, 5, 6, 7, 0, 1, 2], 3, -1),
        ([1], 0, -1),
        ([1], 1, 0),
        ([], 5, -1),
        ([1, 3], 3, 1),
        ([3, 1], 1, 1),
        ([5, 1, 2, 3, 4], 5, 0),
        ([1, 2, 3, 4, 5], 4, 3),  # not rotated at all
    ]
    for nums, target, expected in cases:
        got = sol.search(nums, target)
        status = "OK" if got == expected else "FAIL"
        print(f"{status}: nums={nums}, target={target} -> {got} (expected {expected})")
        assert got == expected, (
            f"33 search({nums}, {target}) returned {got}, expected {expected}"
        )


if __name__ == "__main__":
    _demo()
