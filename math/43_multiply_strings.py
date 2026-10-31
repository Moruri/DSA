"""
LeetCode 43: Multiply Strings
Difficulty: Medium
Topic: Math / Grade-school Multiplication

Problem
-------
Given two non-negative integers num1 and num2 as decimal strings, return their
product as a string. You may not convert the inputs to integers directly or
use a big-integer library.

Examples:
  num1 = "2",   num2 = "3"    ->  "6"
  num1 = "123", num2 = "456"  ->  "56088"

Approach (thought process)
--------------------------
1. Do what you'd do on paper, but without writing out the shifted rows and
   adding them at the end. Every digit pair contributes directly to one slot.
2. Key index fact: if num1 has m digits and num2 has n, the product has at
   most m + n digits. Digit i of num1 times digit j of num2 (indexes from the
   left) lands in positions i + j (tens part) and i + j + 1 (ones part) of a
   result array of length m + n.
3. Loop i and j from the right. For each pair compute
   total = d1 * d2 + res[i + j + 1], store total % 10 at i + j + 1, and add
   total // 10 into res[i + j]. Going right-to-left means a slot's own carry
   has already been folded in before we move left past it.
4. Strip leading zeros (there is at most one from the m + n sizing, more
   only when the answer is 0) and join.

Why it works: the product is the sum over i, j of d1[i] * d2[j] * 10^(place),
and position i + j + 1 is exactly that place in the left-aligned array. The
carry step just keeps every slot a single digit while preserving the total,
and since we always process the rightmost unfinished slot first, every carry
eventually lands in a slot that will itself be normalized.

Complexity:
  - Time: O(m * n), one multiply per digit pair.
  - Space: O(m + n) for the result digits.
"""


class Solution:
    def multiply(self, num1: str, num2: str) -> str:
        if num1 == "0" or num2 == "0":
            return "0"
        m, n = len(num1), len(num2)
        res = [0] * (m + n)
        for i in range(m - 1, -1, -1):
            d1 = ord(num1[i]) - 48
            for j in range(n - 1, -1, -1):
                total = d1 * (ord(num2[j]) - 48) + res[i + j + 1]
                res[i + j + 1] = total % 10
                res[i + j] += total // 10
        start = 0
        while start < len(res) - 1 and res[start] == 0:
            start += 1
        return "".join(chr(48 + d) for d in res[start:])


if __name__ == "__main__":
    import random

    sol = Solution()
    assert sol.multiply("2", "3") == "6"
    assert sol.multiply("123", "456") == "56088"
    assert sol.multiply("0", "9999") == "0"
    assert sol.multiply("999", "999") == "998001"
    assert sol.multiply("1", "1") == "1"

    rng = random.Random(43)
    for _ in range(3000):
        a = rng.randint(0, 10 ** rng.randint(1, 40))
        b = rng.randint(0, 10 ** rng.randint(1, 40))
        assert sol.multiply(str(a), str(b)) == str(a * b), (a, b)  # int() only in the checker
    print("All tests passed for 43.")
