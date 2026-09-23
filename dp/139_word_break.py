"""
LeetCode 139: Word Break
Link: https://leetcode.com/problems/word-break/
Difficulty: Medium
Topic: Dynamic Programming

Problem
-------
Given a string s and a dictionary of strings wordDict, return true if s can be
segmented into a space-separated sequence of one or more dictionary words.

Note that the same word in the dictionary may be reused multiple times in the
segmentation.

Example 1:
  Input:  s = "leetcode", wordDict = ["leet", "code"]
  Output: true
  Explanation: Return true because "leetcode" can be segmented as "leet code".

Example 2:
  Input:  s = "applepenapple", wordDict = ["apple", "pen"]
  Output: true
  Explanation: Return true because "applepenapple" can be segmented as
               "apple pen apple". Note that you are allowed to reuse a
               dictionary word.

Example 3:
  Input:  s = "catsandog", wordDict = ["cats", "dog", "sand", "and", "cat"]
  Output: false

Approach (thought process)
--------------------------
1. Trying every way to split s is exponential (Catalan-like) without memo —
   too slow for |s| up to a few hundred.
2. Define dp[i] = True iff the prefix s[0:i] can be segmented into dictionary
   words. Then dp[0] = True (empty prefix is vacuously segmented).
3. For each end index i in 1..n, try every earlier break j < i: if dp[j] is
   True and s[j:i] is in the dictionary, mark dp[i] True and stop early for
   that i.
4. Put wordDict in a set for O(1) membership. Optionally skip candidates
   longer than the longest dictionary word to cut useless slices.
5. The answer is dp[n]: whether the whole string is reachable from a chain of
   valid dictionary cuts.

Complexity: O(n² · k) time in the naive slice check (n = |s|, k = average
check cost; with a set of words and length bounding this is fine for the
constraints), O(n + total dictionary size) space.
"""

from __future__ import annotations

from typing import List, Set


class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        """Return True if s can be segmented into dictionary words."""
        words: Set[str] = set(wordDict)
        if not words:
            return False

        max_len = max(len(w) for w in words)
        n = len(s)
        dp = [False] * (n + 1)
        dp[0] = True

        for i in range(1, n + 1):
            # Only need to look back as far as the longest dictionary word.
            start = max(0, i - max_len)
            for j in range(start, i):
                if dp[j] and s[j:i] in words:
                    dp[i] = True
                    break

        return dp[n]


def _demo() -> None:
    sol = Solution()
    cases = [
        ("leetcode", ["leet", "code"], True),
        ("applepenapple", ["apple", "pen"], True),
        ("catsandog", ["cats", "dog", "sand", "and", "cat"], False),
        ("a", ["a"], True),
        ("a", ["b"], False),
        ("aaaaaaa", ["aaaa", "aaa"], True),
        ("", ["a"], True),  # empty string: dp[0] is True; n=0
        ("cars", ["car", "ca", "rs"], True),
        ("cbca", ["bc", "ca"], False),
    ]
    for s, word_dict, expected in cases:
        got = sol.wordBreak(s, word_dict)
        status = "OK" if got == expected else "FAIL"
        print(
            f"{status}: s={s!r}, wordDict={word_dict} -> {got} "
            f"(expected {expected})"
        )
        assert got == expected, (
            f"139 wordBreak({s!r}, {word_dict}) returned {got}, "
            f"expected {expected}"
        )


if __name__ == "__main__":
    _demo()