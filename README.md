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
| 3 | [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | Medium | Sliding Window | `sliding_window/3_longest_substring_without_repeating_characters.py` |
| 200 | [Number of Islands](https://leetcode.com/problems/number-of-islands/) | Medium | Graphs / DFS | `graphs/200_number_of_islands.py` |
| 15 | [3Sum](https://leetcode.com/problems/3sum/) | Medium | Two Pointers | `two_pointers/15_3sum.py` |
| 739 | [Daily Temperatures](https://leetcode.com/problems/daily-temperatures/) | Medium | Monotonic Stack | `stack/739_daily_temperatures.py` |
| 56 | [Merge Intervals](https://leetcode.com/problems/merge-intervals/) | Medium | Intervals / Sorting | `intervals/56_merge_intervals.py` |
| 215 | [Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) | Medium | Heaps / Quickselect | `heap/215_kth_largest_element_in_an_array.py` |
| 2 | [Add Two Numbers](https://leetcode.com/problems/add-two-numbers/) | Medium | Linked Lists | `linked_list/2_add_two_numbers.py` |
| 78 | [Subsets](https://leetcode.com/problems/subsets/) | Medium | Backtracking | `backtracking/78_subsets.py` |
| 146 | [LRU Cache](https://leetcode.com/problems/lru-cache/) | Medium | Design | `design/146_lru_cache.py` |
| 547 | [Number of Provinces](https://leetcode.com/problems/number-of-provinces/) | Medium | Union-Find | `union_find/547_number_of_provinces.py` |
| 207 | [Course Schedule](https://leetcode.com/problems/course-schedule/) | Medium | Graphs / Topological Sort | `topological_sort/207_course_schedule.py` |

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

## 3 — Longest Substring Without Repeating Characters

**Problem.** Given a string `s`, return the length of the longest substring that contains no duplicate characters.

**Thought process.**
1. Checking every substring for duplicates is O(n³) (O(n²) substrings, O(n) to validate each) — too slow.
2. If `s[i..j]` contains a repeat, extending `j` can never fix it; only advancing `i` can. That monotonic structure is what a sliding window exploits.
3. Keep a window `[left, right]` with no duplicates. Before adding `s[right]`, if that character is already inside the window, jump `left` to one past its previous index.
4. A hash map `last_seen[ch] -> latest index` makes the jump O(1); guarding with `last_seen[ch] >= left` ignores stale indices so the window never moves backwards. After each step record `right - left + 1`.

**Complexity.** O(n) time, O(min(n, alphabet)) extra space.

Run the demo:

```bash
python3 sliding_window/3_longest_substring_without_repeating_characters.py
```

## 200 — Number of Islands

**Problem.** Given an `m x n` grid of `'1'` (land) and `'0'` (water), return the number of islands, where an island is a group of land cells connected horizontally or vertically.

**Thought process.**
1. Treat the grid as an implicit graph: land cells are vertices, 4-directional neighbours are edges. An island is a connected component.
2. Count components by scanning every cell; each unvisited `'1'` starts a new island, so increment the count and flood-fill that component.
3. The flood fill is a DFS over in-bounds `'1'` neighbours. Overwrite visited cells with `'0'` (sink the island) so no separate visited set is needed.
4. Use an explicit stack instead of recursion — a 300×300 all-land grid would exceed Python's recursion limit. Mark cells on push so each is pushed at most once.

**Complexity.** O(m · n) time, O(m · n) worst-case stack space.

Run the demo:

```bash
python3 graphs/200_number_of_islands.py
```

## 15 — 3Sum

**Problem.** Given an integer array `nums`, return all unique triplets `[nums[i], nums[j], nums[k]]` with distinct indices such that the three values sum to `0`.

**Thought process.**
1. Brute force over every `(i, j, k)` is O(n³) — too slow for n up to 3000.
2. Fix the smallest element `nums[i]` as an anchor; the rest is a 2Sum for `-nums[i]`. Sorting first turns that into a two-pointer sweep: `lo` just after the anchor, `hi` at the end. Too small → `lo += 1`; too big → `hi -= 1`; zero → record it.
3. Sorting also makes dedup trivial: skip an anchor equal to the previous one, and after each hit step `lo`/`hi` past any repeated values so the same triplet is never emitted twice.
4. Stop early once `nums[i] > 0` — everything after a positive anchor is positive, so no triple can reach zero.

**Complexity.** O(n²) time, O(1) extra space beyond the output (ignoring the sort).

Run the demo:

```bash
python3 two_pointers/15_3sum.py
```

## 739 — Daily Temperatures

**Problem.** Given `temperatures`, return `answer` where `answer[i]` is the number of days after day `i` until a strictly warmer temperature, or `0` if there is none.

**Thought process.**
1. Scanning forward from each day is O(n²) on a non-increasing sequence — too slow for n up to 10⁵.
2. This is "next greater element". The waste is re-scanning the same cold days; once day `j` is warmer than day `i`, day `i` is resolved forever.
3. Keep a stack of indices whose answer is still unknown. For each day `j`, while the top index `i` is colder than `temperatures[j]`, set `answer[i] = j - i` and pop. Then push `j`.
4. The stack stays non-increasing in temperature (a monotonic stack). Indices still on it at the end never saw a warmer day and keep the default `0`. Each index is pushed once and popped at most once, so the nested-looking loop is linear.

**Complexity.** O(n) time, O(n) extra space for the stack.

Run the demo:

```bash
python3 stack/739_daily_temperatures.py
```

## 56 — Merge Intervals

**Problem.** Given an array of `intervals` where `intervals[i] = [start_i, end_i]`, merge all overlapping intervals and return the non-overlapping intervals that cover all of the input.

**Thought process.**
1. Repeatedly scanning for any overlapping pair and merging it is O(n²) per pass — too slow for n up to 10⁴.
2. Once the intervals are sorted by start, a new interval can only overlap the *last* merged block; everything earlier already ended before that block began.
3. Sort, then sweep left to right. If the current `start` is past the last block's end, there is a gap — append a new block. Otherwise extend the last block's end to `max(last_end, end)` (the max handles fully contained intervals like `[1, 10]` then `[2, 3]`).
4. Touching intervals (`[1, 4]` and `[4, 5]`) must merge, so the gap test is strict (`start > last_end`). The output comes out sorted and disjoint for free.

**Complexity.** O(n log n) time (the sort), O(n) space for the output.

Run the demo:

```bash
python3 intervals/56_merge_intervals.py
```

## 215 — Kth Largest Element in an Array

**Problem.** Given an integer array `nums` and an integer `k`, return the k-th largest element in sorted order (not the k-th distinct element), ideally without fully sorting.

**Thought process.**
1. Sorting descending and taking index `k-1` is O(n log n) — correct, but we only need one order statistic, not the whole ordering.
2. Keep a min-heap of size `k`. Seed it with the first `k` elements (`heapify`), then for each remaining element, if it beats the root, `heapreplace` the root with it. The heap always holds the `k` largest values seen so far, so its root is the k-th largest.
3. Each heap operation is O(log k), so the total is O(n log k) with O(k) space — a big win when `k << n`, and it streams. `heapq.nlargest(k, nums)[-1]` is the same idea in one line.
4. Alternative — quickselect: pick a random pivot, three-way partition into `>`, `==`, `<`, and recurse only into the side holding rank `k`. Expected O(n) time and O(1) extra space in place, but with an O(n²) worst case; the file includes it as `findKthLargestQuickselect` for comparison.

**Complexity.** O(n log k) time, O(k) extra space (heap). Quickselect: O(n) expected time.

Run the demo:

```bash
python3 heap/215_kth_largest_element_in_an_array.py
```

## 2 — Add Two Numbers

**Problem.** You are given two non-empty linked lists representing two non-negative integers. Digits are stored in reverse order, and each node contains a single digit. Add the two numbers and return the sum as a linked list (also reverse-order).

**Thought process.**
1. Turning each list into an integer, adding, then rebuilding works but fights the linked-list framing and is awkward for very long inputs.
2. Digits are already least-significant-first, so walk both lists in lockstep. At each step add the two digits plus any carry, emit `sum % 10`, and keep `sum // 10` as the next carry.
3. When one list ends, keep walking the other with a zero digit. After both finish, append one more node if a carry remains.
4. A dummy head makes the first digit just another append. Return `dummy.next`.

**Complexity.** O(max(m, n)) time, O(1) extra space beyond the output (m, n = input lengths).

Run the demo:

```bash
python3 linked_list/2_add_two_numbers.py
```

## 78 — Subsets

**Problem.** Given an integer array `nums` of unique elements, return all possible subsets (the power set). Duplicate subsets are not allowed; order does not matter.

**Thought process.**
1. The power set of n distinct elements has size 2ⁿ. A bitmask loop works, but the recursive include/skip (or "choose from the suffix") tree is the standard interview framing.
2. Backtracking: for each start index, append `nums[start]`, recurse from `start + 1` (only later elements, so no duplicates), then pop.
3. Every time you enter the recursive call, the current path is already a valid subset — snapshot `path[:]` into the answer before exploring further choices.
4. Snapshotting is required: mutating the shared path later would corrupt earlier results.

**Complexity.** O(n · 2ⁿ) time (copy each subset), O(n) recursion depth beyond the output.

Run the demo:

```bash
python3 backtracking/78_subsets.py
```

## 146 — LRU Cache

**Problem.** Design an LRU cache with `get(key)` and `put(key, value)`. Both must run in O(1); when capacity is exceeded, evict the least recently used key before inserting.

**Thought process.**
1. A plain dict is O(1) by key but has no recency order; a list tracks order but lookups/moves are O(n). We need both.
2. Pair a hash map (`key -> node`) with a doubly linked list ordered least-recent → most-recent, using dummy head/tail sentinels so splices stay O(1).
3. `get`: miss → `-1`; hit → move the node to the tail (most recent) and return its value.
4. `put`: update + refresh if the key exists; otherwise append a new node and, if over capacity, unlink the node after the head (the LRU) and drop it from the map.

**Complexity.** O(1) time per `get`/`put`, O(capacity) space.

Run the demo:

```bash
python3 design/146_lru_cache.py
```

## 547 — Number of Provinces

**Problem.** Given an `n x n` adjacency matrix `isConnected`, return the number of provinces (connected components of cities; connectivity is transitive).

**Thought process.**
1. A province is a connected component in an undirected graph: cities are vertices, `isConnected[i][j] == 1` edges (symmetric matrix).
2. DFS/BFS also works (same idea as Number of Islands); Union-Find fits the disjoint-set theme and the matrix as a batch of undirected edges.
3. Start with `n` singleton sets. For every `i < j` with `isConnected[i][j] == 1`, `union(i, j)`. The number of distinct roots left is the province count.
4. Path compression + union-by-rank keeps each operation nearly O(1) (inverse Ackermann).

**Complexity.** O(n² · α(n)) time, O(n) extra space.

Run the demo:

```bash
python3 union_find/547_number_of_provinces.py
```

## 207 — Course Schedule

**Problem.** There are `numCourses` courses labeled `0..numCourses-1`. Given `prerequisites` where each `[a, b]` means you must take `b` before `a`, return whether you can finish every course.

**Thought process.**
1. Finishing every course is possible iff the prerequisite graph has a valid ordering — i.e. it is a DAG (no cycles).
2. Draw an edge `b → a` for each pair `[a, b]` ("`b` unlocks `a`"). Track each course's indegree (how many prereqs it still needs).
3. Kahn's algorithm: put every indegree-0 course in a queue. Repeatedly take one, decrement its neighbors' indegrees, and enqueue any neighbor that hits 0.
4. If the number of courses taken equals `numCourses`, every node entered the order — no cycle. Leftover positive indegrees mean a cycle.

**Complexity.** O(V + E) time and space (V = `numCourses`, E = `|prerequisites|`).

Run the demo:

```bash
python3 topological_sort/207_course_schedule.py
```
