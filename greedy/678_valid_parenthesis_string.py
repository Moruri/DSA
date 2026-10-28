"""
LeetCode 678: Valid Parenthesis String
Difficulty: Medium
Topic: Greedy / Range of open counts

Problem
-------
A string contains only '(', ')' and '*'. Each '*' can act as '(' or ')' or
the empty string. Return True if some choice makes the string a valid
parentheses sequence.

Examples: "()" -> True, "(*)" -> True, "(*))" -> True, "((*" -> False

Approach (thought process)
--------------------------
1. Without stars you'd track one number: how many '(' are still open. It
   must never go negative and must end at 0.
2. A star makes that number uncertain, so track the whole range of possible
   open counts instead: lo = fewest open brackets possible, hi = most.
   - '(' : lo += 1, hi += 1
   - ')' : lo -= 1, hi -= 1
   - '*' : lo -= 1 (star used as ')'), hi += 1 (star used as '(')
3. If hi drops below 0, even treating every star as '(' can't cover the
   closers seen so far, so it's impossible: return False.
4. Clamp lo at 0, since a negative open count is never a real option; that
   choice of star simply isn't allowed, so we fall back to treating it as
   empty.
5. Every value between lo and hi is reachable (each star shifts the count by
   one step), so at the end the string is valid exactly when lo == 0.
6. This beats the O(n^2) DP over (index, open count) and the two-stack
   approach: one pass, two integers.

Complexity: O(n) time, O(1) space.
"""

from __future__ import annotations


class Solution:
    def checkValidString(self, s: str) -> bool:
        lo = hi = 0
        for ch in s:
            if ch == "(":
                lo += 1
                hi += 1
            elif ch == ")":
                lo -= 1
                hi -= 1
            else:
                lo -= 1
                hi += 1
            if hi < 0:
                return False
            lo = max(lo, 0)
        return lo == 0


if __name__ == "__main__":
    s = Solution()
    cases = [
        ("()", True),
        ("(*)", True),
        ("(*))", True),
        ("((*", False),
        (")(", False),
        ("*", True),
        ("(((((*(()((((*((**(((()()*)()()()*((((**)())*)*)))))))(())(()))())((*()()(((()((()*(())*(()**)()(())", False),
    ]
    for text, expected in cases:
        got = s.checkValidString(text)
        assert got == expected, (text, got, expected)
        print(f"{text[:20]!r:24} -> {got}")
    print("All tests passed.")
