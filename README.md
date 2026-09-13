# DSA

Data Structures & Algorithms practice solutions (Python).

## Problems

| # | Title | Difficulty | Topic | Path |
|---|-------|------------|-------|------|
| 560 | [Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) | Medium | Arrays / Prefix Sum | `arrays/560_subarray_sum_equals_k.py` |
| 102 | [Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) | Medium | Trees / BFS | `trees/102_binary_tree_level_order_traversal.py` |
| 49 | [Group Anagrams](https://leetcode.com/problems/group-anagrams/) | Medium | Hashing / Strings | `hashing/49_group_anagrams.py` |
| 198 | [House Robber](https://leetcode.com/problems/house-robber/) | Medium | Dynamic Programming | `dp/198_house_robber.py` |
| 33 | [Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/) | Medium | Binary Search | `binary_search/33_search_in_rotated_sorted_array.py` |

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

## 102 — Binary Tree Level Order Traversal

**Problem.** Given the root of a binary tree, return the level order traversal of its nodes' values (left to right, level by level).

**Thought process.**
1. Level order is breadth-first: finish one depth before the next.
2. Use a queue (BFS). While non-empty, process exactly the nodes currently in the queue — that is one level.
3. Collect each node's value, then enqueue its left and right children for the next round.
4. Append each level's list to the answer; an empty root yields `[]`.

**Complexity.** O(n) time, O(n) space (n = number of nodes).

Run the demo:

```bash
python3 trees/102_binary_tree_level_order_traversal.py
```

## 49 — Group Anagrams

**Problem.** Given an array of strings `strs`, group the anagrams together. Return the groups in any order.

**Thought process.**
1. Two strings are anagrams iff they share the same multiset of characters.
2. Use the sorted character string as a hash-map key (`"eat"` and `"tea"` both sort to `"aet"`).
3. Scan once: append each word to the list keyed by its sorted form.
4. Return the map's values. (Letter-count tuples work the same idea in O(n·k).)

**Complexity.** O(n · k log k) time, O(n · k) space (n strings, max length k).

Run the demo:

```bash
python3 hashing/49_group_anagrams.py
```

## 198 — House Robber

**Problem.** Given an integer array `nums` where `nums[i]` is the money in house `i`, return the maximum amount you can rob without robbing two adjacent houses.

**Thought process.**
1. Trying every subset of non-adjacent houses is exponential — too slow.
2. The decision at house `i` depends only on `i-1` and `i-2`. Let `dp[i]` be the best loot from houses `0..i`: either skip `i` (`dp[i-1]`) or rob it (`dp[i-2] + nums[i]`).
3. So `dp[i] = max(dp[i-1], dp[i-2] + nums[i])`, with virtual `dp[-1] = dp[-2] = 0` as base cases.
4. Only the last two values are needed, so two rolling variables replace the array; the answer is the final `dp` value (0 for an empty street).

**Complexity.** O(n) time, O(1) extra space.

Run the demo:

```bash
python3 dp/198_house_robber.py
```

## 33 — Search in Rotated Sorted Array

**Problem.** Given a distinct-valued sorted array `nums` that was rotated at an unknown pivot, and a `target`, return the index of `target` or `-1`. Must run in O(log n).

**Thought process.**
1. O(log n) points to binary search, but the array is not fully sorted.
2. Splitting a rotated sorted array at `mid` always leaves at least one sorted half; `nums[lo] <= nums[mid]` tells you it is the left one, otherwise the right.
3. Check in O(1) whether `target` falls in the sorted half's value range — if so, search there; otherwise search the other half.
4. Each step halves the range, exactly like ordinary binary search. Return `mid` on a hit, `-1` once `lo > hi`.

**Complexity.** O(log n) time, O(1) extra space.

Run the demo:

```bash
python3 binary_search/33_search_in_rotated_sorted_array.py
```
