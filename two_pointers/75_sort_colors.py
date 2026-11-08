"""
LeetCode 75: Sort Colors
Difficulty: Medium
Topic: Two Pointers / Dutch National Flag

Problem
-------
Given an array nums with n objects colored red, white, or blue (encoded as
0, 1, 2), sort them in-place so objects of the same color are adjacent, in
the order red, white, blue. Do not use the library sort. Follow-up: one
pass, O(1) extra space.

Approach (thought process)
--------------------------
1. Counting sort works (count 0s, 1s, 2s, then overwrite) but takes two
   passes. The follow-up asks for one.
2. Dijkstra's Dutch National Flag: keep three regions while scanning.
     nums[0 .. low-1]    are all 0
     nums[low .. mid-1]  are all 1
     nums[mid .. high]   are still unknown
     nums[high+1 .. n-1] are all 2
3. Look at nums[mid]:
     - 0: swap it into the 0-region (with nums[low]), then low += 1 and
       mid += 1. What came back from `low` was a 1 (or mid == low), which
       is already known, so it is safe to advance mid.
     - 1: it is already in the right place; mid += 1.
     - 2: swap it with nums[high] and shrink high. Do NOT advance mid:
       the value swapped in from the right is unexamined.
4. Stop when mid > high: the unknown region is empty.

Why it works: every step either shrinks the unknown window by one or
keeps all four invariants true, so the loop runs at most n times and
ends with the array split into 0s | 1s | 2s.

Complexity:
  - Time: O(n), a single pass.
  - Space: O(1).
"""

from typing import List


class Solution:
    def sortColors(self, nums: List[int]) -> None:
        low, mid, high = 0, 0, len(nums) - 1
        while mid <= high:
            if nums[mid] == 0:
                nums[low], nums[mid] = nums[mid], nums[low]
                low += 1
                mid += 1
            elif nums[mid] == 1:
                mid += 1
            else:
                nums[mid], nums[high] = nums[high], nums[mid]
                high -= 1


if __name__ == "__main__":
    import random

    cases = [
        [2, 0, 2, 1, 1, 0],
        [2, 0, 1],
        [0],
        [1],
        [2, 2, 2],
        [],
        [1, 0],
        [2, 1, 0, 0, 1, 2],
    ]
    for c in cases:
        arr = c[:]
        Solution().sortColors(arr)
        assert arr == sorted(c), (c, arr)
        print(c, "->", arr)
    for _ in range(500):
        c = [random.randint(0, 2) for _ in range(random.randint(0, 20))]
        arr = c[:]
        Solution().sortColors(arr)
        assert arr == sorted(c)
    print("all tests passed")
