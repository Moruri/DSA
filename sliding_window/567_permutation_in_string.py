"""
LeetCode 567: Permutation in String
Difficulty: Medium
Topic: Sliding Window / Fixed-size Frequency Match

Problem
-------
Given two strings s1 and s2 (lowercase English letters), return True if s2
contains a permutation of s1 as a contiguous substring, i.e. some window of
s2 is an anagram of s1.

Example:
  s1 = "ab", s2 = "eidbaooo" -> True   ("ba")
  s1 = "ab", s2 = "eidboaoo" -> False

Approach (thought process)
--------------------------
1. "Permutation of s1" just means "same letter counts as s1". Order is
   irrelevant, so compare frequency counts, not strings.
2. Any match must be exactly len(s1) characters long, so the window size is
   fixed. Slide a window of that size across s2.
3. Naive version: recount each window, O(26 * n) with array compares. Fine,
   but we can do better by tracking how many of the 26 letters currently
   have matching counts ("matches").
     - Build counts for s1 and the first window of s2, then count how many
       letters agree.
     - Each slide adds one char on the right and drops one on the left.
       Only those two letters can change agreement, so update `matches`
       for just them: if a letter's count becomes equal, matches += 1; if
       it was equal and now isn't, matches -= 1.
     - The moment matches == 26, the window is an anagram.

Why it works: two multisets of letters are equal exactly when all 26 counts
agree, and `matches` is maintained as precisely that number with O(1) work
per step.

Complexity:
  - Time: O(len(s1) + len(s2)). Each step does constant work.
  - Space: O(1), two arrays of 26 counters.
"""

from collections import Counter


class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        m, n = len(s1), len(s2)
        if m > n:
            return False

        need = [0] * 26
        have = [0] * 26
        for a, b in zip(s1, s2[:m]):
            need[ord(a) - 97] += 1
            have[ord(b) - 97] += 1

        matches = sum(1 for i in range(26) if need[i] == have[i])

        for right in range(m, n):
            if matches == 26:
                return True

            add = ord(s2[right]) - 97
            have[add] += 1
            if have[add] == need[add]:
                matches += 1
            elif have[add] == need[add] + 1:
                matches -= 1

            drop = ord(s2[right - m]) - 97
            have[drop] -= 1
            if have[drop] == need[drop]:
                matches += 1
            elif have[drop] == need[drop] - 1:
                matches -= 1

        return matches == 26


def _brute(s1: str, s2: str) -> bool:
    target = Counter(s1)
    m = len(s1)
    return any(Counter(s2[i:i + m]) == target for i in range(len(s2) - m + 1))


if __name__ == "__main__":
    s = Solution()
    assert s.checkInclusion("ab", "eidbaooo") is True
    assert s.checkInclusion("ab", "eidboaoo") is False
    assert s.checkInclusion("adc", "dcda") is True
    assert s.checkInclusion("abc", "ab") is False
    assert s.checkInclusion("a", "a") is True
    assert s.checkInclusion("hello", "ooolleoooleh") is False

    import random

    for _ in range(3000):
        s1 = "".join(random.choice("abc") for _ in range(random.randint(1, 4)))
        s2 = "".join(random.choice("abc") for _ in range(random.randint(1, 10)))
        assert s.checkInclusion(s1, s2) == _brute(s1, s2), (s1, s2)
    print("All tests passed.")
