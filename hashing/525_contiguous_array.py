"""
LeetCode 525: Contiguous Array
Difficulty: Medium
Topic: Hashing / Prefix Balance

Problem
-------
Given a binary array nums, return the length of the longest contiguous
subarray with an equal number of 0s and 1s.

Approach (thought process)
--------------------------
1. "Equal zeros and ones" is awkward to count directly, so re-label:
   treat every 0 as -1 and every 1 as +1. Now a subarray is balanced
   exactly when its sum is 0.
2. A subarray (i, j] sums to 0 exactly when the running total (prefix
   balance) at j equals the running total at i. So the question becomes:
   for each index j, what is the EARLIEST index where we saw this same
   balance? The distance between them is a balanced subarray.
3. Store only the first index for each balance in a hash map; later
   occurrences should not overwrite it, because the earliest start gives
   the longest stretch.
4. Seed the map with {0: -1}, meaning "balance 0 before the array starts",
   so a balanced prefix starting at index 0 is counted.

This is the same prefix-sum + hash map trick as 560 (Subarray Sum Equals K),
just asking for the longest length instead of a count.

Complexity
----------
Time:  O(n) -- one pass, O(1) average hash operations.
Space: O(n) -- at most 2n + 1 distinct balances in the map.
"""

from typing import List


class Solution:
    def findMaxLength(self, nums: List[int]) -> int:
        first_seen = {0: -1}
        balance = best = 0
        for i, x in enumerate(nums):
            balance += 1 if x == 1 else -1
            if balance in first_seen:
                best = max(best, i - first_seen[balance])
            else:
                first_seen[balance] = i
        return best


if __name__ == "__main__":
    s = Solution()
    cases = [
        ([0, 1], 2),
        ([0, 1, 0], 2),
        ([0, 1, 1, 1, 1, 1, 0, 0, 0], 6),
        ([1, 1, 1], 0),
        ([0, 0, 1, 0, 0, 0, 1, 1], 6),
    ]
    for nums, expected in cases:
        got = s.findMaxLength(nums)
        assert got == expected, (nums, got, expected)
        print(f"{nums} -> {got}")
    print("All tests passed.")
