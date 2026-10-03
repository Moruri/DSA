"""
LeetCode 1143: Longest Common Subsequence
Difficulty: Medium
Topic: Dynamic Programming

Problem
-------
Given two strings `text1` and `text2`, return the length of their longest
common subsequence. A subsequence is formed by deleting zero or more
characters without changing the order of the remaining characters. If there
is no common subsequence, return 0.

Example 1:
  Input:  text1 = "abcde", text2 = "ace"
  Output: 3
  Explanation: "ace"

Example 2:
  Input:  text1 = "abc", text2 = "abc"
  Output: 3

Example 3:
  Input:  text1 = "abc", text2 = "def"
  Output: 0

Approach (thought process)
--------------------------
1. Let `dp[i][j]` be the LCS length of the prefixes `text1[:i]` and
   `text2[:j]`. Empty prefixes give 0 along the first row/column.
2. If `text1[i-1] == text2[j-1]`, both characters are taken:
   `dp[i][j] = dp[i-1][j-1] + 1`.
3. Otherwise skip one side: `dp[i][j] = max(dp[i-1][j], dp[i][j-1])`.
4. Only the previous row is needed, so two rolling 1D arrays (or one with
   careful right-to-left bookkeeping) shrink space to O(min(m, n)). Here we
   keep a full 2D table for clarity; the answer is `dp[m][n]`.

Complexity: O(m · n) time, O(m · n) space (m, n = string lengths).
"""

from __future__ import annotations


class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        """Return the length of the longest common subsequence of text1 and text2."""
        m, n = len(text1), len(text2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        return dp[m][n]


def _demo() -> None:
    sol = Solution()
    cases = [
        ("abcde", "ace", 3),
        ("abc", "abc", 3),
        ("abc", "def", 0),
        ("", "abc", 0),
        ("abc", "", 0),
        ("bsbininm", "jmjkbkjkv", 1),
        ("oxcpqrsvwf", "lcrqswkkyccx", 4),
    ]
    for a, b, expected in cases:
        got = sol.longestCommonSubsequence(a, b)
        status = "OK" if got == expected else "FAIL"
        print(
            f"{status}: longestCommonSubsequence({a!r}, {b!r}) -> {got} "
            f"(expected {expected})"
        )
        assert got == expected, (
            f"1143 longestCommonSubsequence({a!r}, {b!r}) returned {got}, "
            f"expected {expected}"
        )


if __name__ == "__main__":
    _demo()
