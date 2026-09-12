# DSA

Data Structures & Algorithms practice solutions (Python).

## Problems

| # | Title | Difficulty | Topic | Path |
|---|-------|------------|-------|------|
| 560 | [Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) | Medium | Arrays / Prefix Sum | `arrays/560_subarray_sum_equals_k.py` |
| 102 | [Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) | Medium | Trees / BFS | `trees/102_binary_tree_level_order_traversal.py` |
| 49 | [Group Anagrams](https://leetcode.com/problems/group-anagrams/) | Medium | Hashing / Strings | `hashing/49_group_anagrams.py` |

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
