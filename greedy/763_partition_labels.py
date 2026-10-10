"""
LeetCode 763: Partition Labels
Link: https://leetcode.com/problems/partition-labels/
Difficulty: Medium
Topic: Greedy / Hashing

Problem
-------
Split string s into as many parts as possible so that each letter appears in
at most one part. Concatenating the parts must give back s. Return the sizes
of the parts.

Example 1:
  Input:  s = "ababcbacadefegdehijhklij"
  Output: [9, 7, 8]   ("ababcbaca", "defegde", "hijhklij")

Example 2:
  Input:  s = "eccbbbbdec"
  Output: [10]

Approach (thought process)
--------------------------
1. The constraint is about each letter's span: if 'a' shows up at index 0 and
   at index 8, the part that holds index 0 must stretch at least to index 8.
2. So first record last[c] = the last index where letter c appears (one pass).
3. Second pass, left to right, keeping `end` = the furthest last-occurrence of
   any letter seen in the current part. Every new letter can push `end`
   further right (like a fence that has to keep moving out).
4. When the index i reaches `end`, every letter inside the part has already
   had its final appearance, so we can cut here safely. Cutting as early as
   possible is what maximizes the number of parts: any earlier cut would split
   some letter, and waiting longer would only merge parts that could have been
   separate.
5. This is the same idea as merging intervals [first[c], last[c]], just done
   in one sweep without building the intervals.

Complexity: O(n) time, O(1) extra space (at most 26 letters).
"""

from __future__ import annotations

from typing import List


class Solution:
    def partitionLabels(self, s: str) -> List[int]:
        last = {ch: i for i, ch in enumerate(s)}
        sizes: List[int] = []
        start = end = 0
        for i, ch in enumerate(s):
            end = max(end, last[ch])
            if i == end:
                sizes.append(end - start + 1)
                start = i + 1
        return sizes


def _brute(s: str) -> List[int]:
    # Cut at every position where the prefix and suffix share no letters.
    sizes, start = [], 0
    for i in range(1, len(s) + 1):
        if i == len(s) or not (set(s[:i]) & set(s[i:])):
            sizes.append(i - start)
            start = i
    return sizes


def _demo() -> None:
    sol = Solution()
    cases = [
        ("ababcbacadefegdehijhklij", [9, 7, 8]),
        ("eccbbbbdec", [10]),
        ("a", [1]),
        ("abc", [1, 1, 1]),
        ("abca", [4]),
    ]
    for s, expected in cases:
        got = sol.partitionLabels(s)
        status = "OK" if got == expected else "FAIL"
        print(f"{status}: partitionLabels({s!r}) -> {got} (expected {expected})")
        assert got == expected

    import random

    rng = random.Random(763)
    for _ in range(300):
        s = "".join(rng.choice("abcde") for _ in range(rng.randint(1, 14)))
        assert sol.partitionLabels(s) == _brute(s), s
    print("OK: 300 random cases match brute force")


if __name__ == "__main__":
    _demo()
