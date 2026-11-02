"""
LeetCode 1004: Max Consecutive Ones III
Difficulty: Medium
Topic: Sliding Window / Budgeted Flips

Problem
-------
Given a binary array nums and an integer k, return the maximum number of
consecutive 1s in the array if you can flip at most k 0s.

Examples:
  nums = [1,1,1,0,0,0,1,1,1,1,0], k = 2              ->  6
  nums = [0,0,1,1,0,0,1,1,1,0,1,1,0,0,0,1,1,1,1], k = 3  ->  10

Approach (thought process)
--------------------------
1. Rephrase: "flip at most k zeros" is the same as "find the longest
   contiguous window that contains at most k zeros". Every zero inside the
   window gets flipped; the window is then all ones.
2. That is a classic variable-size sliding window. Grow the right edge one
   step at a time and count the zeros inside.
3. If the zero count goes over k, the window is invalid, so slide the left
   edge forward (un-counting any zero that leaves) until it is valid again.
4. After each step the window [left, right] is the longest valid window
   ending at right, so record its length.

Why it works: for a fixed right edge, the best left edge only ever moves
forward as right grows (adding elements can only add zeros). So each index
enters and leaves the window at most once, and we never miss the longest
valid window.

Complexity:
  - Time: O(n), each pointer moves at most n steps.
  - Space: O(1).
"""

from typing import List


class Solution:
    def longestOnes(self, nums: List[int], k: int) -> int:
        left = 0
        zeros = 0
        best = 0
        for right, x in enumerate(nums):
            if x == 0:
                zeros += 1
            while zeros > k:
                if nums[left] == 0:
                    zeros -= 1
                left += 1
            best = max(best, right - left + 1)
        return best


if __name__ == "__main__":
    s = Solution()
    cases = [
        ([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2, 6),
        ([0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1], 3, 10),
        ([0, 0, 0], 0, 0),
        ([0, 0, 0], 5, 3),
        ([1, 1, 1], 0, 3),
    ]
    for nums, k, expected in cases:
        got = s.longestOnes(nums, k)
        assert got == expected, (nums, k, got, expected)
        print(f"k={k} {nums} -> {got}")
    print("All tests passed.")
