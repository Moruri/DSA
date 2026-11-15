"""
LeetCode 438: Find All Anagrams in a String
Difficulty: Medium
Topic: Sliding Window / Frequency Counting

Problem
-------
Given strings s and p, return every start index in s where a substring is
an anagram of p.

Approach (thought process)
--------------------------
1. An anagram of p is any string with exactly p's letter counts. Every
   candidate has length len(p), so the window size is fixed. That points to
   a fixed-size sliding window, not the grow/shrink kind.
2. Brute force re-counts each window: O(n * k). Instead, slide by one: add
   the letter that comes in on the right, remove the one that leaves on the
   left. Each step is O(1).
3. Comparing two 26-letter count arrays each step is O(26), which is fine.
   We can do better and track `matches`, the number of letters (out of 26)
   whose window count equals p's count. Each in/out update changes the
   status of only one letter, so we adjust `matches` in O(1). When
   matches == 26, the window is an anagram.
4. Why it works: two strings are anagrams iff all 26 counts agree, and
   `matches` counts exactly how many of them agree right now.

Complexity
----------
Time:  O(n + k) where n = len(s), k = len(p).
Space: O(1), two arrays of 26 counts.
"""

from typing import List


class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        n, k = len(s), len(p)
        if k > n:
            return []

        need = [0] * 26
        have = [0] * 26
        for i in range(k):
            need[ord(p[i]) - 97] += 1
            have[ord(s[i]) - 97] += 1

        matches = sum(1 for i in range(26) if need[i] == have[i])
        result = [0] if matches == 26 else []

        def bump(idx: int, delta: int) -> None:
            nonlocal matches
            if have[idx] == need[idx]:
                matches -= 1          # was matching, about to change
            have[idx] += delta
            if have[idx] == need[idx]:
                matches += 1          # now matching again

        for right in range(k, n):
            bump(ord(s[right]) - 97, +1)       # letter enters
            bump(ord(s[right - k]) - 97, -1)   # letter leaves
            if matches == 26:
                result.append(right - k + 1)

        return result


if __name__ == "__main__":
    s = Solution()
    assert s.findAnagrams("cbaebabacd", "abc") == [0, 6]
    assert s.findAnagrams("abab", "ab") == [0, 1, 2]
    assert s.findAnagrams("a", "ab") == []
    assert s.findAnagrams("aaaa", "aa") == [0, 1, 2]
    assert s.findAnagrams("xyz", "abc") == []
    print("438 Find All Anagrams in a String: all tests passed")
