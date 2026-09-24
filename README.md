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
| 238 | [Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/) | Medium | Arrays / Prefix Products | `arrays/238_product_of_array_except_self.py` |
| 208 | [Implement Trie (Prefix Tree)](https://leetcode.com/problems/implement-trie-prefix-tree/) | Medium | Trie / Prefix Tree | `trie/208_implement_trie.py` |
| 994 | [Rotting Oranges](https://leetcode.com/problems/rotting-oranges/) | Medium | Graphs / Multi-source BFS | `graphs/994_rotting_oranges.py` |
| 322 | [Coin Change](https://leetcode.com/problems/coin-change/) | Medium | Dynamic Programming | `dp/322_coin_change.py` |
| 424 | [Longest Repeating Character Replacement](https://leetcode.com/problems/longest-repeating-character-replacement/) | Medium | Sliding Window | `sliding_window/424_longest_repeating_character_replacement.py` |
| 98 | [Validate Binary Search Tree](https://leetcode.com/problems/validate-binary-search-tree/) | Medium | Trees / BST | `trees/98_validate_binary_search_tree.py` |
| 11 | [Container With Most Water](https://leetcode.com/problems/container-with-most-water/) | Medium | Two Pointers | `two_pointers/11_container_with_most_water.py` |
| 139 | [Word Break](https://leetcode.com/problems/word-break/) | Medium | Dynamic Programming | `dp/139_word_break.py` |
| 54 | [Spiral Matrix](https://leetcode.com/problems/spiral-matrix/) | Medium | Matrix / Simulation | `matrix/54_spiral_matrix.py` |
| 39 | [Combination Sum](https://leetcode.com/problems/combination-sum/) | Medium | Backtracking | `backtracking/39_combination_sum.py` |

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

## 238 — Product of Array Except Self

**Problem.** Given an integer array `nums`, return an array `answer` where `answer[i]` is the product of every element of `nums` except `nums[i]`. Do it in O(n) without division.

**Thought process.**
1. Division is banned, and multiplying everything except index `i` naively is O(n²).
2. `answer[i]` is (product of everything left of `i`) times (product of everything right of `i`).
3. Left-to-right pass: fill `answer[i]` with the running left product, then multiply the runner by `nums[i]`.
4. Right-to-left pass: multiply each `answer[i]` by a running right product, then fold `nums[i]` into that runner.
5. One output array plus a scalar for the right product meets the O(1) extra-space follow-up.

**Complexity.** O(n) time, O(1) extra space beyond the output.

Run the demo:

```bash
python3 arrays/238_product_of_array_except_self.py
```

## 208 — Implement Trie (Prefix Tree)

**Problem.** Implement a trie with `insert(word)`, `search(word)` (exact word), and `startsWith(prefix)`.

**Thought process.**
1. A plain set of words makes exact search easy but `startsWith` still scans every word.
2. Store characters on tree edges: each node maps `child_char → child_node` and marks whether a full word ends there.
3. `insert` walks or creates one child per character, then sets the end-of-word flag.
4. `search` walks the path and requires the end flag; `startsWith` only needs the path to exist.
5. Shared prefixes reuse nodes, so total space tracks unique character paths across all words.

**Complexity.** O(L) time per operation for a string of length L; space O(total characters inserted).

Run the demo:

```bash
python3 trie/208_implement_trie.py
```

## 994 — Rotting Oranges

**Problem.** In an `m x n` grid of empty (0), fresh (1), and rotten (2) oranges, every minute every fresh orange adjacent (4-dir) to a rotten one becomes rotten. Return the minutes until no fresh oranges remain, or `-1` if impossible.

**Thought process.**
1. Rot spreads simultaneously from every rotten cell each minute — multi-source BFS on the grid graph.
2. Seed a queue with all initial rotten cells and count the fresh oranges; if the count is already 0, return 0.
3. Process the queue level by level (one minute per level): infect every fresh 4-neighbour, enqueue it, and decrement the fresh count.
4. When BFS ends, return the minutes if every fresh orange was reached; otherwise `-1` (unreachable pockets).

**Complexity.** O(m · n) time, O(m · n) space for the queue.

Run the demo:

```bash
python3 graphs/994_rotting_oranges.py
```

## 322 — Coin Change

**Problem.** Given coin denominations `coins` and a target `amount`, return the fewest coins needed to make that amount (unlimited supply of each coin), or `-1` if impossible.

**Thought process.**
1. Greedy fails on some denomination sets, so use exact DP.
2. Let `dp[x]` be the fewest coins for amount `x`; `dp[0] = 0`, and unreachable amounts stay at a sentinel `amount + 1`.
3. For each `x` from 1..amount and each coin `c ≤ x`, set `dp[x] = min(dp[x], dp[x - c] + 1)` when `x - c` is reachable.
4. After filling, return `dp[amount]` or `-1` if it is still the sentinel.

**Complexity.** O(amount · len(coins)) time, O(amount) space.

Run the demo:

```bash
python3 dp/322_coin_change.py
```

## 424 — Longest Repeating Character Replacement

**Problem.** Given a string `s` and an integer `k`, you may replace any character with any other uppercase English letter at most `k` times. Return the length of the longest substring that can be made all the same letter after those replacements.

**Thought process.**
1. Inside a window of length `L`, the cheapest uniform rewrite keeps the most frequent character and replaces the rest — valid iff `L - max_freq ≤ k`.
2. Grow a sliding window while maintaining character counts and the peak frequency in the window.
3. When replacements needed exceed `k`, advance the left edge and decrement the leaving character's count.
4. Track the maximum valid window length; each index enters/leaves at most once.

**Complexity.** O(n) time, O(1) space (fixed alphabet of 26).

Run the demo:

```bash
python3 sliding_window/424_longest_repeating_character_replacement.py
```

## 98 — Validate Binary Search Tree

**Problem.** Given the root of a binary tree, return whether it is a valid BST: every node's left subtree holds only keys strictly less than the node, every right subtree only keys strictly greater, and both subtrees are themselves valid BSTs.

**Thought process.**
1. Checking only immediate children is not enough — a deep descendant can violate an ancestor's bound.
2. Propagate an open interval `(lo, hi)` down the tree; the root starts unbounded.
3. A node with value `v` must satisfy `lo < v < hi`; its left child inherits `(lo, v)` and its right child `(v, hi)`.
4. Empty subtrees are valid; use `None` sentinels for unbound ends so extreme 32-bit values stay safe.

**Complexity.** O(n) time, O(h) space for the recursion stack (h = height).

Run the demo:

```bash
python3 trees/98_validate_binary_search_tree.py
```


## 11 — Container With Most Water

**Problem.** You are given `n` vertical lines where the `i`-th line has endpoints `(i, 0)` and `(i, height[i])`. Choose two lines that, with the x-axis, form a container holding the most water (no slanting). Return that maximum area.

**Thought process.**
1. Checking every pair is O(n²) — too slow for large `n`.
2. Area equals `min(height[lo], height[hi]) * (hi - lo)`. Start at the widest span (`lo = 0`, `hi = n - 1`) so width is maximised first.
3. The shorter line limits the height; moving the taller pointer can never raise that min, so always advance the shorter side.
4. Track a running maximum while `lo < hi`; each index is visited at most once.

**Complexity.** O(n) time, O(1) extra space.

Run the demo:

```bash
python3 two_pointers/11_container_with_most_water.py
```

## 139 — Word Break

**Problem.** Given a string `s` and a dictionary `wordDict`, return whether `s` can be segmented into a space-separated sequence of one or more dictionary words (words may be reused).

**Thought process.**
1. Enumerating every split is exponential without memoisation.
2. Let `dp[i]` mean the prefix `s[0:i]` can be segmented; `dp[0] = True` for the empty prefix.
3. For each end `i`, try a prior break `j`: if `dp[j]` and `s[j:i]` is in the dictionary, set `dp[i] = True`.
4. Store `wordDict` in a set and bound the look-back by the longest word length; the answer is `dp[n]`.

**Complexity.** O(n²) time with set lookups (n = `|s|`), O(n + dictionary size) space.

Run the demo:

```bash
python3 dp/139_word_break.py
```


## 54 — Spiral Matrix

**Problem.** Given an `m x n` matrix, return all elements of the matrix in spiral order (clockwise from the top-left).

**Thought process.**
1. Peeling layer by layer is clearer than a direction+visited walk and needs no extra visited set.
2. Keep four bounds (`top`, `bottom`, `left`, `right`). Walk left→right on the top row, top→bottom on the right column, then (if still a row/column left) right→left on the bottom and bottom→top on the left.
3. Shrink the corresponding bound after each side; the inner-leg guards prevent double-counting a lone remaining row or column.
4. Empty input yields `[]`; each cell is emitted exactly once.

**Complexity.** O(m · n) time, O(1) extra space beyond the output.

Run the demo:

```bash
python3 matrix/54_spiral_matrix.py
```

## 39 — Combination Sum

**Problem.** Given distinct integers `candidates` and a `target`, return all unique combinations that sum to `target`. The same number may be chosen unlimited times; order within a combination does not matter.

**Thought process.**
1. Backtracking: pick a candidate, subtract from the remaining target, recurse.
2. Only consider candidates at or after the current start index so `[2, 3]` and `[3, 2]` are not both emitted; reuse the same index to allow unlimited repeats of one value.
3. Sort first and prune once `candidates[i] > remaining` (later values are larger).
4. Snapshot the path when remaining hits 0; always pop after exploring a branch.

**Complexity.** O(n^{T/m}) time worst case (n candidates, T = target, m = smallest candidate), O(T/m) recursion depth beyond the output.

Run the demo:

```bash
python3 backtracking/39_combination_sum.py
```
