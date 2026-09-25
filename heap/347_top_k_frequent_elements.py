"""
LeetCode 347: Top K Frequent Elements
Link: https://leetcode.com/problems/top-k-frequent-elements/
Difficulty: Medium
Topic: Heap / Bucket Sort

Problem
-------
Given an integer array nums and an integer k, return the k most frequent
elements. You may return the answer in any order.

Example 1:
  Input:  nums = [1, 1, 1, 2, 2, 3], k = 2
  Output: [1, 2]

Example 2:
  Input:  nums = [1], k = 1
  Output: [1]

Approach (thought process)
--------------------------
1. Count frequencies with a hash map in one pass — O(n). We now know how often
   each distinct value appears.
2. Heap approach: keep a min-heap of size k keyed by frequency. Push
   (freq, value); whenever the heap exceeds k, pop the least frequent. After
   the scan the heap holds the k most frequent values. O(n log k) time.
3. Bucket-sort approach (preferred here for O(n)): make an array of buckets
   where index i holds every value whose frequency is exactly i. The maximum
   frequency is at most n, so the buckets fit in O(n) space. Walk buckets from
   high frequency down to 1 and collect values until you have k of them.
4. Order among the k answers is free — any order is accepted. Ties between
   values with the same frequency can go either way.

Complexity (bucket sort): O(n) time, O(n) extra space.
Complexity (heap): O(n log k) time, O(n) for the counts + O(k) for the heap.
"""

from __future__ import annotations

import heapq
from collections import Counter
from typing import List


class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        """Return the k most frequent elements using frequency buckets."""
        counts = Counter(nums)
        # buckets[f] = list of values that appear exactly f times.
        # Index 0 is unused; max frequency is len(nums).
        buckets: List[List[int]] = [[] for _ in range(len(nums) + 1)]
        for value, freq in counts.items():
            buckets[freq].append(value)

        result: List[int] = []
        for freq in range(len(buckets) - 1, 0, -1):
            for value in buckets[freq]:
                result.append(value)
                if len(result) == k:
                    return result
        return result

    def topKFrequentHeap(self, nums: List[int], k: int) -> List[int]:
        """Alternative: min-heap of size k keyed by frequency."""
        counts = Counter(nums)
        # heap holds (freq, value); smallest freq sits at the root.
        heap: List[tuple[int, int]] = []
        for value, freq in counts.items():
            heapq.heappush(heap, (freq, value))
            if len(heap) > k:
                heapq.heappop(heap)
        return [value for _, value in heap]


def _demo() -> None:
    sol = Solution()
    cases = [
        ([1, 1, 1, 2, 2, 3], 2, {1, 2}),
        ([1], 1, {1}),
        ([4, 4, 4, 4], 1, {4}),
        ([1, 2], 2, {1, 2}),
        # All frequencies equal — any k of them is fine; take the full set.
        ([5, 6, 7], 3, {5, 6, 7}),
        # One value dominates.
        ([9, 9, 9, 8, 8, 7], 2, {9, 8}),
        # Negatives and zero.
        ([-1, -1, 0, 0, 0, 2], 2, {0, -1}),
    ]
    for nums, k, expected in cases:
        got = set(sol.topKFrequent(list(nums), k))
        got_heap = set(sol.topKFrequentHeap(list(nums), k))
        status = "OK" if got == expected == got_heap else "FAIL"
        print(
            f"{status}: nums={nums}, k={k} -> bucket={sorted(got)}, "
            f"heap={sorted(got_heap)} (expected {sorted(expected)})"
        )
        assert got == expected, f"347 bucket({nums}, {k}) -> {got}, expected {expected}"
        assert got_heap == expected, f"347 heap({nums}, {k}) -> {got_heap}, expected {expected}"
        assert len(got) == k

    # Cross-check: the returned set must be the k highest-frequency values.
    import random

    rng = random.Random(347)
    for _ in range(200):
        n = rng.randint(1, 40)
        nums = [rng.randint(-10, 10) for _ in range(n)]
        distinct = len(set(nums))
        k = rng.randint(1, distinct)
        counts = Counter(nums)
        # Values sorted by frequency descending; take top k (ties arbitrary).
        ranked = sorted(counts.keys(), key=lambda v: counts[v], reverse=True)
        min_kept_freq = counts[ranked[k - 1]]
        # Every returned value must have freq >= that cutoff, and we keep k.
        for method in (sol.topKFrequent, sol.topKFrequentHeap):
            got = method(list(nums), k)
            assert len(got) == k
            assert len(set(got)) == k
            assert all(counts[v] >= min_kept_freq for v in got)
            # Must include every value strictly above the cutoff.
            must = {v for v, f in counts.items() if f > min_kept_freq}
            assert must.issubset(set(got))
    print("OK: 200 random cases agree on top-k frequency membership")


if __name__ == "__main__":
    _demo()
