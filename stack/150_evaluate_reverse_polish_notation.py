"""
LeetCode 150: Evaluate Reverse Polish Notation
Difficulty: Medium
Topic: Stack (Expression Evaluation)

Problem
-------
Given an array of string tokens representing an arithmetic expression in
Reverse Polish (postfix) Notation, evaluate it and return the integer result.
Operators are +, -, *, /. Division truncates toward zero. The input is
always a valid expression.

Example:
  ["2", "1", "+", "3", "*"]  -> ((2 + 1) * 3) = 9
  ["4", "13", "5", "/", "+"] -> (4 + (13 / 5)) = 6

Approach (thought process)
--------------------------
1. In postfix, an operator always applies to the two most recent values that
   haven't been consumed yet. "Most recent, not yet used" is exactly what a
   stack hands you.
2. Scan left to right. A number gets pushed. An operator pops two values,
   computes, and pushes the result back, because that result is now a value
   for some later operator.
3. Order matters for - and /: the FIRST pop is the right operand, the second
   pop is the left one (a b - means a - b).
4. Truncation trap: Python's // floors toward negative infinity, so -7 // 2 is
   -4 but LeetCode wants -3. Use int(a / b), which truncates toward zero
   (safe here since values fit easily in a float).
5. When the tokens run out, exactly one value remains: the answer.

Why it works: postfix has no parentheses or precedence; the token order
itself encodes the evaluation tree, and the stack replays a post-order walk
of that tree, so each operator meets precisely its two subtrees' results.

Complexity:
  - Time: O(n) for n tokens, each pushed/popped at most once.
  - Space: O(n) in the worst case (many numbers before operators).
"""

from typing import List


class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        ops = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: int(a / b),
        }
        stack: List[int] = []
        for tok in tokens:
            if tok in ops:
                right = stack.pop()
                left = stack.pop()
                stack.append(ops[tok](left, right))
            else:
                stack.append(int(tok))
        return stack[-1]


if __name__ == "__main__":
    s = Solution()
    assert s.evalRPN(["2", "1", "+", "3", "*"]) == 9
    assert s.evalRPN(["4", "13", "5", "/", "+"]) == 6
    assert s.evalRPN(
        ["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]
    ) == 22
    assert s.evalRPN(["-7", "2", "/"]) == -3
    assert s.evalRPN(["42"]) == 42
    print("All tests passed for 150. Evaluate Reverse Polish Notation")
