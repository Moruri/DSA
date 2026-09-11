# DSA

Data Structures & Algorithms practice solutions (Python).

## Problems

| # | Title | Difficulty | Topic | Path |
|---|-------|------------|-------|------|
| 560 | [Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) | Medium | Arrays / Prefix Sum | `arrays/560_subarray_sum_equals_k.py` |

## 560 — Subarray Sum Equals K

**Problem.** Given an integer array `nums` and an integer `k`, return the total number of contiguous subarrays whose sum equals `k`.

**Thought process.**
1. Brute force checks every `nums[i..j]` — O(n²), too slow.
2. Prefix sum insight: sum of `nums[i..j]` is `S_j - S_{i-1}`. We want that equal to `k`, so `S_{i-1} == S_j - k`.
3. Scan left to right with a hash map of how often each prefix sum has appeared. For current sum `S`, add `count[S - k]` to the answer, then record `S`.
4. Seed the map with `{0: 1}` so a prefix that itself equals `k` counts.

**Complexity.** O(n) time, O(n) extra space.

Run the demo:

```bash
python3 arrays/560_subarray_sum_equals_k.py
```
