"""
LeetCode 97: Interleaving String
Difficulty: Medium
Topic: Dynamic Programming / 2D Grid of Prefixes

Problem
-------
Given strings s1, s2, s3, return True if s3 is formed by interleaving s1 and
s2: s3 uses every character of both, keeping each string's own order.

Approach (thought process)
--------------------------
1. Quick filter: if len(s1) + len(s2) != len(s3), it's impossible.
2. Greedy fails: when s1[i] == s2[j] == s3[i+j] we don't know which string to
   take from, and a wrong pick can doom us later ("aabcc"/"dbbca"/"aadbbcbcac").
   So we need to remember choices -> DP over prefixes.
3. State: dp[i][j] = can the first i chars of s1 and first j chars of s2 build
   the first i+j chars of s3? The next char of s3 is s3[i+j-1], and it must
   come from either the end of s1's prefix or the end of s2's prefix:
       dp[i][j] = (dp[i-1][j] and s1[i-1] == s3[i+j-1])
               or (dp[i][j-1] and s2[j-1] == s3[i+j-1])
   Base: dp[0][0] = True.
4. Picture it as a grid: you start top-left, each step right "spends" an s2
   char, each step down spends an s1 char, and a step is only allowed when the
   spent char matches s3's next char. The answer is whether bottom-right is
   reachable.
5. Each row only reads the row above and the cell to the left, so a single
   1D array of length len(s2)+1 is enough.

Complexity
----------
Time:  O(m * n) for m = len(s1), n = len(s2).
Space: O(n) with the rolling row.
"""


class Solution:
    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
        m, n = len(s1), len(s2)
        if m + n != len(s3):
            return False
        dp = [False] * (n + 1)
        for i in range(m + 1):
            for j in range(n + 1):
                if i == 0 and j == 0:
                    dp[j] = True
                    continue
                from_s1 = i > 0 and dp[j] and s1[i - 1] == s3[i + j - 1]
                from_s2 = j > 0 and dp[j - 1] and s2[j - 1] == s3[i + j - 1]
                dp[j] = from_s1 or from_s2
        return dp[n]


if __name__ == "__main__":
    s = Solution()
    cases = [
        ("aabcc", "dbbca", "aadbbcbcac", True),
        ("aabcc", "dbbca", "aadbbbaccc", False),
        ("", "", "", True),
        ("a", "", "a", True),
        ("", "b", "a", False),
        ("ab", "ab", "abab", True),
        ("abc", "d", "abcde", False),
    ]
    for s1, s2, s3, expected in cases:
        got = s.isInterleave(s1, s2, s3)
        assert got == expected, (s1, s2, s3, got, expected)
        print(f"s1={s1!r}, s2={s2!r}, s3={s3!r} -> {got}")
    print("All tests passed.")
