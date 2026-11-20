"""
LeetCode 402: Remove K Digits
Difficulty: Medium
Topic: Monotonic Stack / Greedy

Problem
-------
Given a non-negative integer as a string `num` and an integer k, remove
exactly k digits so the remaining number is as small as possible. Return
it without leading zeros ("0" if nothing is left).

Approach (thought process)
--------------------------
1. Numbers of equal length are compared left to right, so the leftmost
   digits matter most. The greedy question: which digit should go first?
2. Scan left to right. If a digit is bigger than the digit right after it
   (a "peak"), deleting the peak makes the number smaller at the earliest
   possible position. Deleting anything later can never beat that.
3. A stack does this cleanly: for each new digit d, while k > 0 and the top
   of the stack is greater than d, pop it (one removal each). Then push d.
   The stack stays non-decreasing from bottom to top.
4. If removals are still owed after the scan, the stack is non-decreasing,
   so the largest digits sit at the end: chop the last k.
5. Strip leading zeros; an empty result becomes "0".

Why it works: each pop removes the first place where the number goes
down, which is the single deletion that shrinks the number the most. Doing
that k times is optimal.

Complexity
----------
Time:  O(n), since every digit is pushed and popped at most once.
Space: O(n) for the stack.
"""


class Solution:
    def removeKdigits(self, num: str, k: int) -> str:
        stack = []
        for d in num:
            while k and stack and stack[-1] > d:
                stack.pop()
                k -= 1
            stack.append(d)
        if k:
            stack = stack[:-k]
        return "".join(stack).lstrip("0") or "0"


if __name__ == "__main__":
    s = Solution()
    cases = [
        ("1432219", 3, "1219"),
        ("10200", 1, "200"),
        ("10", 2, "0"),
        ("112", 1, "11"),
        ("123456", 3, "123"),
        ("9", 1, "0"),
    ]
    for num, k, want in cases:
        got = s.removeKdigits(num, k)
        assert got == want, (num, k, got, want)
        print(f"removeKdigits({num!r}, {k}) = {got!r}")
    print("All tests passed.")
