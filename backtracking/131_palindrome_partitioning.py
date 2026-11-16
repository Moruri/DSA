"""
LeetCode 131: Palindrome Partitioning
Difficulty: Medium
Topic: Backtracking / DP Precompute

Problem
-------
Split string s into pieces so that every piece is a palindrome. Return all
such partitions.

Approach (thought process)
--------------------------
1. A partition is a sequence of "cut" choices: from index `start`, pick an end
   `end` so that s[start:end+1] is a palindrome, then solve the rest from
   end+1. That is a decision tree, so backtracking fits.
2. The costly part is checking palindromes over and over. Precompute a table
   is_pal[i][j] once with DP: s[i:j+1] is a palindrome when s[i] == s[j] and
   the inside s[i+1:j] is a palindrome (or the piece has length <= 2).
   Fill i from right to left so is_pal[i+1][j-1] is ready when we need it.
3. DFS(start): if start == n, the current path covers the whole string, so
   save a copy. Otherwise try each end with is_pal[start][end], push the
   piece, recurse, pop (the "undo" step of backtracking).
4. Why it works: every valid partition corresponds to exactly one path of
   palindromic cuts, and the DFS tries every cut at every position, so it
   lists each partition once and never a bad one.

Complexity
----------
Time:  O(n^2) for the table + O(n * 2^n) for the output in the worst case
       ("aaaa...": every cut is valid, 2^(n-1) partitions).
Space: O(n^2) table + O(n) recursion depth (output not counted).
"""

from typing import List


class Solution:
    def partition(self, s: str) -> List[List[str]]:
        n = len(s)
        is_pal = [[False] * n for _ in range(n)]
        for i in range(n - 1, -1, -1):
            for j in range(i, n):
                if s[i] == s[j] and (j - i < 2 or is_pal[i + 1][j - 1]):
                    is_pal[i][j] = True

        result: List[List[str]] = []
        path: List[str] = []

        def dfs(start: int) -> None:
            if start == n:
                result.append(path[:])
                return
            for end in range(start, n):
                if is_pal[start][end]:
                    path.append(s[start:end + 1])
                    dfs(end + 1)
                    path.pop()

        dfs(0)
        return result


if __name__ == "__main__":
    sol = Solution()
    out = sol.partition("aab")
    assert sorted(out) == sorted([["a", "a", "b"], ["aa", "b"]]), out
    assert sol.partition("a") == [["a"]]
    assert len(sol.partition("aaaa")) == 8  # 2^(4-1)
    print("aab ->", out)
    print("All tests passed.")
