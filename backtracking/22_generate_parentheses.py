"""
LeetCode 22: Generate Parentheses
Difficulty: Medium
Topic: Backtracking / Constrained Generation

Problem
-------
Given n pairs of parentheses, return every combination of well-formed
(balanced) parentheses strings of length 2n.

Example:
  Input:  n = 3
  Output: ["((()))", "(()())", "(())()", "()(())", "()()()"]

Approach (thought process)
--------------------------
1. Brute force would build all 2^(2n) strings of '(' and ')' and filter the
   balanced ones. Most of those are garbage, e.g. anything starting with ')'.
2. Better: build the string one character at a time and never take a step
   that can't lead to a valid answer. That's backtracking with pruning.
3. What makes a prefix "still fixable"? Two counters:
     - open_used: how many '(' we've placed (can't exceed n).
     - close_used: how many ')' we've placed (can't exceed open_used, or some
       ')' would have nothing to close).
   So at each step:
     - add '(' if open_used < n
     - add ')' if close_used < open_used
4. When the string reaches length 2n, both counters equal n and the prefix
   rule held at every step, so the string is balanced. Record it.
5. Use a list as a mutable buffer (append / pop) instead of building new
   strings at every level.

Why it works: a string is balanced exactly when no prefix has more ')' than
'(' and the totals match. The two rules enforce the prefix condition at every
step and the length check enforces the totals, so we generate every valid
string and nothing else, each exactly once (different choices at the first
differing position give different strings).

Complexity: the number of answers is the nth Catalan number,
C(n) ~ 4^n / (n^1.5 * sqrt(pi)). Each answer costs O(n) to copy, so time is
O(4^n / sqrt(n)); recursion depth and buffer are O(n) extra space (not
counting the output).
"""

from typing import List


class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        result: List[str] = []
        buf: List[str] = []

        def build(open_used: int, close_used: int) -> None:
            if len(buf) == 2 * n:
                result.append("".join(buf))
                return
            if open_used < n:
                buf.append("(")
                build(open_used + 1, close_used)
                buf.pop()
            if close_used < open_used:
                buf.append(")")
                build(open_used, close_used + 1)
                buf.pop()

        build(0, 0)
        return result


def _is_balanced(s: str) -> bool:
    depth = 0
    for ch in s:
        depth += 1 if ch == "(" else -1
        if depth < 0:
            return False
    return depth == 0


if __name__ == "__main__":
    s = Solution()
    assert s.generateParenthesis(1) == ["()"]
    assert sorted(s.generateParenthesis(3)) == sorted(
        ["((()))", "(()())", "(())()", "()(())", "()()()"]
    )
    catalan = [1, 1, 2, 5, 14, 42, 132, 429, 1430]
    for n in range(1, 9):
        out = s.generateParenthesis(n)
        assert len(out) == catalan[n], (n, len(out))
        assert len(set(out)) == len(out)
        assert all(_is_balanced(x) for x in out)
    print("n=3 ->", s.generateParenthesis(3))
    print("All tests passed.")
