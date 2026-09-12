"""
LeetCode 49: Group Anagrams
Difficulty: Medium
Topic: Hashing / Strings

Problem
-------
Given an array of strings strs, group the anagrams together. You can return
the answer in any order.

An Anagram is a word or phrase formed by rearranging the letters of a
different word or phrase, typically using all the original letters exactly
once.

Example 1:
  Input:  strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
  Output: [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]
  (order of groups and of strings within a group may vary)

Example 2:
  Input:  strs = [""]
  Output: [[""]]

Example 3:
  Input:  strs = ["a"]
  Output: [["a"]]

Approach (thought process)
--------------------------
1. Two strings are anagrams iff they have the same multiset of characters.
2. A simple signature is the sorted character string: "eat" and "tea" both
   sort to "aet". Use that as a hash-map key.
3. Scan once: for each word, append it to the list keyed by its sorted form.
4. Return the map's values (the groups). Sorting each word of length k costs
   O(k log k); overall O(n * k log k) for n strings.

Alternative: count letters into a 26-tuple key for O(n * k) time — same idea.

Complexity: O(n * k log k) time, O(n * k) space (n strings, max length k).
"""

from __future__ import annotations

from collections import defaultdict
from typing import Dict, List


class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        """Group strings that are anagrams of each other."""
        groups: Dict[str, List[str]] = defaultdict(list)
        for word in strs:
            key = "".join(sorted(word))
            groups[key].append(word)
        return list(groups.values())


def _normalize(groups: List[List[str]]) -> List[tuple[str, ...]]:
    """Sort for order-independent comparison of anagram groups."""
    return sorted(tuple(sorted(g)) for g in groups)


def _demo() -> None:
    sol = Solution()
    cases = [
        (
            ["eat", "tea", "tan", "ate", "nat", "bat"],
            [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]],
        ),
        ([""], [[""]]),
        (["a"], [["a"]]),
        (["ab", "ba", "abc"], [["ab", "ba"], ["abc"]]),
    ]
    for strs, expected in cases:
        got = sol.groupAnagrams(strs)
        status = "OK" if _normalize(got) == _normalize(expected) else "FAIL"
        print(f"{status}: strs={strs} -> {got} (expected ~{expected})")


if __name__ == "__main__":
    _demo()
