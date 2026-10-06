"""
LeetCode 371: Sum of Two Integers
Difficulty: Medium
Topic: Bit Manipulation

Problem
-------
Given two integers a and b, return a + b without using the + or - operators.
Constraints: -1000 <= a, b <= 1000 (answers fit in a 32-bit signed int).

Example 1:
  Input:  a = 1, b = 2
  Output: 3

Example 2:
  Input:  a = 2, b = 3
  Output: 5

Approach (thought process)
--------------------------
1. Think about adding binary numbers by hand, one column at a time. Each
   column produces a sum bit and maybe a carry into the next column.
2. XOR gives the sum bits while ignoring carries: 0^0=0, 1^0=1, 1^1=0.
   AND finds the columns where both bits are 1, which is exactly where a
   carry is produced; shifting it left by 1 moves it into the next column.
3. So a + b == (a ^ b) + ((a & b) << 1). That is still an addition, but we
   can repeat the trick: set a = a ^ b, b = (a & b) << 1, and loop until
   there's no carry left (b == 0). Then a holds the answer.
4. Python wrinkle: Python ints are unbounded, so a negative number has
   infinitely many leading 1 bits and the carry would never die out. Fix it
   by masking everything to 32 bits (MASK = 0xFFFFFFFF), the way real
   hardware does. The carry then falls off the top after at most 32 rounds.
5. At the end, a is a 32-bit pattern. If its sign bit (bit 31) is set, it
   stands for a negative number, so convert back with ~(a ^ MASK), which
   flips the low 32 bits and then flips everything (sign-extends).

Why it terminates: each round, the carry's lowest set bit moves at least one
position left, so within 32 rounds it is shifted past the mask and becomes 0.

Complexity: O(1) time (at most 32 iterations) and O(1) space.
"""

from __future__ import annotations

MASK = 0xFFFFFFFF  # keep 32 bits, like a machine register
SIGN_BIT = 0x80000000


class Solution:
    def getSum(self, a: int, b: int) -> int:
        """Add a and b using only bitwise operations."""
        a &= MASK
        b &= MASK
        while b:
            carry = ((a & b) << 1) & MASK  # columns that overflow into the next one
            a = (a ^ b) & MASK  # column sums, ignoring carries
            b = carry
        # Reinterpret the 32-bit pattern as a signed integer.
        return a if a < SIGN_BIT else ~(a ^ MASK)


def _demo() -> None:
    sol = Solution()
    cases = [(1, 2, 3), (2, 3, 5), (-1, 1, 0), (-2, -3, -5), (1000, -1000, 0), (-1000, 999, -1), (0, 0, 0)]
    for a, b, expected in cases:
        got = sol.getSum(a, b)
        status = "OK" if got == expected else "FAIL"
        print(f"{status}: getSum({a}, {b}) -> {got} (expected {expected})")
        assert got == expected, f"371 returned {got} for ({a}, {b}), expected {expected}"

    for a in range(-1000, 1001, 7):
        for b in range(-1000, 1001, 13):
            assert sol.getSum(a, b) == a + b, (a, b)
    print("OK: grid of constraint-range pairs matches built-in addition")


if __name__ == "__main__":
    _demo()
