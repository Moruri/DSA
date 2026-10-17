"""
LeetCode 91: Decode Ways
Difficulty: Medium
Topic: Dynamic Programming / 1-D (Fibonacci-style)

Problem
-------
A message of letters A-Z is encoded as numbers: 'A' -> "1", ..., 'Z' -> "26".
Given a digit string s, return how many ways it can be decoded.
"06" is not a valid code for 'F' (leading zeros are not allowed).

Examples:
  "12"  -> 2  ("AB" from 1,2 or "L" from 12)
  "226" -> 3  (2,2,6 / 22,6 / 2,26)
  "06"  -> 0

Approach (thought process)
--------------------------
1. Look at how a decoding ends. The last letter used either one digit or two
   digits. So the number of ways for the prefix s[:i] depends only on the
   prefixes s[:i-1] and s[:i-2]. That is the recurrence:
     ways[i] = (ways[i-1] if s[i-1] != '0')
             + (ways[i-2] if "10" <= s[i-2:i] <= "26")
2. Base case: ways[0] = 1, the empty prefix has exactly one (empty) decoding.
   This is what makes "12" correctly count the two-digit "L" path.
3. Zeros are the whole trap. A '0' can never stand alone, so it only survives
   as the second digit of "10" or "20". "30" or a leading "0" kills every
   path, and the recurrence naturally returns 0 there.
4. Each step only reads the two previous values, so keep two rolling
   variables instead of an array, just like Fibonacci or Climbing Stairs.

Why it works: every decoding of s[:i] ends in exactly one of the two ways
(one-digit or two-digit last letter), and those two groups never overlap,
so adding their counts counts every decoding exactly once.

Complexity:
  - Time: O(n), one pass.
  - Space: O(1), two rolling counters.
"""


class Solution:
    def numDecodings(self, s: str) -> int:
        prev2, prev1 = 0, 1  # ways[i-2], ways[i-1]; start with ways[0] = 1
        for i in range(1, len(s) + 1):
            cur = 0
            if s[i - 1] != "0":
                cur += prev1
            if i >= 2 and "10" <= s[i - 2:i] <= "26":
                cur += prev2
            prev2, prev1 = prev1, cur
            if cur == 0:
                return 0  # no path survives; later digits cannot revive it
        return prev1


def _brute(s: str) -> int:
    if not s:
        return 1
    total = 0
    if s[0] != "0":
        total += _brute(s[1:])
        if len(s) >= 2 and 10 <= int(s[:2]) <= 26:
            total += _brute(s[2:])
    return total


if __name__ == "__main__":
    import random

    sol = Solution()
    cases = {"12": 2, "226": 3, "06": 0, "0": 0, "10": 1, "27": 1,
             "100": 0, "2101": 1, "11106": 2, "1201234": 3}
    for s, want in cases.items():
        got = sol.numDecodings(s)
        assert got == want, (s, got, want)

    for _ in range(500):
        s = "".join(random.choice("0123456789") for _ in range(random.randint(1, 14)))
        assert sol.numDecodings(s) == _brute(s), s
    print("All tests passed for 91.")
