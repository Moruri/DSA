"""
LeetCode 15: 3Sum
Link: https://leetcode.com/problems/3sum/
Difficulty: Medium
Topic: Two Pointers / Sorting

Problem
-------
Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]]
such that i != j, i != k, j != k, and nums[i] + nums[j] + nums[k] == 0.

The solution set must not contain duplicate triplets. Triplets may be returned
in any order.

Example 1:
  Input:  nums = [-1, 0, 1, 2, -1, -4]
  Output: [[-1, -1, 2], [-1, 0, 1]]

Example 2:
  Input:  nums = [0, 1, 1]
  Output: []

Example 3:
  Input:  nums = [0, 0, 0]
  Output: [[0, 0, 0]]

Approach (thought process)
--------------------------
1. Brute force: try every (i, j, k) triple — O(n^3) — and dedupe with a set of
   sorted tuples. Far too slow for n up to 3000.
2. Reduce to 2Sum: fix the smallest element nums[i], then look for a pair in
   the remainder that sums to -nums[i]. A hash set gives O(n) per anchor, but
   deduplication gets fiddly.
3. Sorting first makes both the search and the dedup clean. With a sorted
   array, the pair search becomes the classic two-pointer sweep: lo just after
   the anchor, hi at the end. If the total is too small, move lo right (bigger
   value); if too big, move hi left (smaller value); if zero, record it.
   Each step discards one index for good, so the sweep is O(n) per anchor.
4. Duplicates are handled by skipping equal neighbours: if nums[i] == nums[i-1]
   the anchor was already fully explored, so continue. After recording a hit,
   advance lo past any copies of nums[lo] and hi past any copies of nums[hi]
   so the same triplet is never emitted twice.
5. Early exits: once nums[i] > 0 every remaining value is positive and no
   triple can sum to zero, so stop. Anchors only need to run to n - 3.

Complexity: O(n^2) time (sort is O(n log n), dominated by the n two-pointer
sweeps), O(1) extra space beyond the output (ignoring the sort's own space).
"""

from __future__ import annotations

from typing import List


class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        """Return all unique triplets that sum to zero."""
        nums.sort()
        n = len(nums)
        result: List[List[int]] = []

        for i in range(n - 2):
            # Sorted, so anything after a positive anchor is positive too.
            if nums[i] > 0:
                break
            # Same anchor value as before -> same triplets as before; skip.
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            lo, hi = i + 1, n - 1
            while lo < hi:
                total = nums[i] + nums[lo] + nums[hi]
                if total < 0:
                    lo += 1
                elif total > 0:
                    hi -= 1
                else:
                    result.append([nums[i], nums[lo], nums[hi]])
                    lo += 1
                    hi -= 1
                    # Step over duplicates so the same pair is not reused.
                    while lo < hi and nums[lo] == nums[lo - 1]:
                        lo += 1
                    while lo < hi and nums[hi] == nums[hi + 1]:
                        hi -= 1

        return result


def _normalise(triplets: List[List[int]]) -> List[tuple]:
    """Order-independent form so demo comparisons ignore output ordering."""
    return sorted(tuple(sorted(t)) for t in triplets)


def _demo() -> None:
    sol = Solution()
    cases = [
        ([-1, 0, 1, 2, -1, -4], [[-1, -1, 2], [-1, 0, 1]]),
        ([0, 1, 1], []),
        ([0, 0, 0], [[0, 0, 0]]),
        ([], []),
        ([1, 2], []),
        # Many duplicates: exactly one [0, 0, 0] must appear.
        ([0, 0, 0, 0, 0], [[0, 0, 0]]),
        # All positive -> early break on anchor.
        ([1, 2, 3, 4, 5], []),
        # All negative -> no triple can reach zero.
        ([-5, -4, -3, -2, -1], []),
        (
            [-2, 0, 1, 1, 2],
            [[-2, 0, 2], [-2, 1, 1]],
        ),
        (
            [3, 0, -2, -1, 1, 2],
            [[-2, -1, 3], [-2, 0, 2], [-1, 0, 1]],
        ),
    ]
    for nums, expected in cases:
        got = sol.threeSum(nums[:])  # copy: threeSum sorts its input in place
        ok = _normalise(got) == _normalise(expected)
        status = "OK" if ok else "FAIL"
        print(f"{status}: nums={nums} -> {got} (expected {expected})")
        assert ok, f"15 threeSum({nums}) returned {got}, expected {expected}"

    # Every emitted triplet must actually sum to zero and be unique.
    sample = [-4, -2, -2, -2, 0, 1, 2, 2, 2, 3, 3, 4, 4, 6, 6]
    out = sol.threeSum(sample[:])
    assert all(sum(t) == 0 for t in out), "15 threeSum produced a non-zero triplet"
    assert len(_normalise(out)) == len(set(_normalise(out))), "15 threeSum produced duplicates"
    print(f"OK: {len(out)} unique zero-sum triplets found in {sample}")


if __name__ == "__main__":
    _demo()
