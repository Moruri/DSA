"""
LeetCode 72: Edit Distance
Difficulty: Medium
Topic: Dynamic Programming / 2-D (string alignment)

Problem
-------
Given two strings word1 and word2, return the minimum number of operations
needed to turn word1 into word2. Allowed operations on word1: insert a
character, delete a character, replace a character.

Example 1:
  Input:  word1 = "horse", word2 = "ros"
  Output: 3   (horse -> rorse -> rose -> ros)

Example 2:
  Input:  word1 = "intention", word2 = "execution"
  Output: 5

Approach (thought process)
--------------------------
1. Trying edits greedily fails: fixing one mismatch can make a later one
   cheaper or pricier. We need to compare all alignments, which smells like DP.
2. Look at the LAST characters only. Let dp[i][j] be the cost of turning the
   first i chars of word1 into the first j chars of word2.
   - If word1[i-1] == word2[j-1], they line up for free: dp[i-1][j-1].
   - Otherwise one of three moves ends the alignment, each costing 1:
       replace word1[i-1] with word2[j-1]  -> dp[i-1][j-1] + 1
       delete word1[i-1]                   -> dp[i-1][j]   + 1
       insert word2[j-1] at the end        -> dp[i][j-1]   + 1
     Take the minimum.
3. Base cases: turning a prefix of length i into "" costs i deletions
   (dp[i][0] = i), and "" into a prefix of length j costs j inserts.
4. Each cell only reads the row above and the cell to its left, so one row
   plus a saved "diagonal" value is enough memory.

Complexity: O(m * n) time, O(n) space (n = len(word2)).
"""

from __future__ import annotations

from functools import lru_cache


class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        m, n = len(word1), len(word2)
        row = list(range(n + 1))  # dp[0][j] = j
        for i in range(1, m + 1):
            diag = row[0]          # dp[i-1][0]
            row[0] = i             # dp[i][0]
            for j in range(1, n + 1):
                above = row[j]     # dp[i-1][j]
                if word1[i - 1] == word2[j - 1]:
                    row[j] = diag
                else:
                    row[j] = 1 + min(diag, above, row[j - 1])
                diag = above
        return row[n]


def _brute(a: str, b: str) -> int:
    """Top-down recursion straight from the definition, for cross-checking."""

    @lru_cache(maxsize=None)
    def go(i: int, j: int) -> int:
        if i == len(a):
            return len(b) - j
        if j == len(b):
            return len(a) - i
        if a[i] == b[j]:
            return go(i + 1, j + 1)
        return 1 + min(go(i + 1, j + 1), go(i + 1, j), go(i, j + 1))

    return go(0, 0)


if __name__ == "__main__":
    s = Solution()
    assert s.minDistance("horse", "ros") == 3
    assert s.minDistance("intention", "execution") == 5
    assert s.minDistance("", "abc") == 3
    assert s.minDistance("abc", "") == 3
    assert s.minDistance("same", "same") == 0

    import random

    for _ in range(500):
        a = "".join(random.choice("abc") for _ in range(random.randint(0, 8)))
        b = "".join(random.choice("abc") for _ in range(random.randint(0, 8)))
        assert s.minDistance(a, b) == _brute(a, b), (a, b)
    print("All tests passed.")
