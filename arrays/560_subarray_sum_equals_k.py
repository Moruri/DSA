"""
LeetCode 560: Subarray Sum Equals K
Difficulty: Medium
Topic: Arrays / Prefix Sum / Hash Map

Problem
-------
Given an integer array nums and an integer k, return the total number of
contiguous subarrays whose sum equals k.

Example 1:
  Input:  nums = [1, 1, 1], k = 2
    Output: 2
      Explanation: [1,1] at indices 0..1 and [1,1] at indices 1..2

      Example 2:
        Input:  nums = [1, 2, 3], k = 3
          Output: 2
            Explanation: [1,2] and [3]

            Approach (thought process)
            --------------------------
            1. Brute force: try every subarray nums[i..j], sum it, count matches.
               That is O(n^2) time (or O(n^3) if you re-sum each window) — too slow
                  for large n.

                  2. Key insight: if the prefix sum up to index j is S_j, and the prefix
                     sum up to index i-1 is S_{i-1}, then the subarray nums[i..j] sums to
                        S_j - S_{i-1}. We want S_j - S_{i-1} == k, i.e. S_{i-1} == S_j - k.

                        3. While scanning left to right, keep a hash map of how many times each
                           prefix sum has appeared so far. For the current sum S, add
                              count[S - k] to the answer, then record S in the map.

                              4. Seed the map with {0: 1} so a prefix that itself equals k is counted
                                 (subarray starting at index 0).

                                 Complexity: O(n) time, O(n) extra space.
                                 """

from __future__ import annotations

from collections import defaultdict
from typing import List


class Solution:
      def subarraySum(self, nums: List[int], k: int) -> int:
                """Count contiguous subarrays whose sum equals k."""
                prefix_counts: dict[int, int] = defaultdict(int)
                prefix_counts[0] = 1  # empty prefix: sum 0 seen once

        running = 0
        answer = 0

        for value in nums:
                      running += value
                      # How many earlier prefixes make (running - earlier) == k?
                      answer += prefix_counts[running - k]
                      prefix_counts[running] += 1

        return answer


def _demo() -> None:
      sol = Solution()
    cases = [
              ([1, 1, 1], 2, 2),
              ([1, 2, 3], 3, 2),
              ([1, -1, 0], 0, 3),
              ([3, 4, 7, 2, -3, 1, 4, 2], 7, 4),
    ]
    for nums, k, expected in cases:
              got = sol.subarraySum(nums, k)
              status = "OK" if got == expected else "FAIL"
              print(f"{status}: nums={nums}, k={k} -> {got} (expected {expected})")


if __name__ == "__main__":
      _demo()
