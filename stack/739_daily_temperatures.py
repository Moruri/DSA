"""
LeetCode 739: Daily Temperatures
Link: https://leetcode.com/problems/daily-temperatures/
Difficulty: Medium
Topic: Stack / Monotonic Stack

Problem
-------
Given an array of integers temperatures representing daily temperatures,
return an array answer such that answer[i] is the number of days you have to
wait after the i-th day to get a warmer temperature. If there is no future day
with a warmer temperature, answer[i] == 0.

Example 1:
  Input:  temperatures = [73, 74, 75, 71, 69, 72, 76, 73]
  Output: [1, 1, 4, 2, 1, 1, 0, 0]

Example 2:
  Input:  temperatures = [30, 40, 50, 60]
  Output: [1, 1, 1, 0]

Example 3:
  Input:  temperatures = [30, 60, 90]
  Output: [1, 1, 0]

Approach (thought process)
--------------------------
1. Brute force: for each day scan forward until a strictly warmer day is
   found. O(n^2) in the worst case (a non-increasing sequence) — too slow for
   n up to 10^5.
2. This is a "next greater element" question. The waste in brute force is
   re-scanning the same cold days over and over. Observation: once day j is
   warmer than day i, day i is resolved forever and never needs looking at
   again.
3. Keep a stack of indices whose answer is still unknown. Walk left to right;
   for the current day j, while the stack top index i has a colder temperature
   than temperatures[j], day j is the first warmer day for i: set
   answer[i] = j - i and pop it. Then push j.
4. The stack therefore always holds indices with non-increasing temperatures
   (a monotonic stack). Anything still on the stack at the end never saw a
   warmer day, and its answer stays at the default 0.
5. Every index is pushed once and popped at most once, so the total work is
   linear even though the inner while-loop looks nested.

Complexity: O(n) time, O(n) extra space for the stack (plus the output).
"""

from __future__ import annotations

from typing import List


class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        """For each day, return how many days until a strictly warmer one (0 if never)."""
        n = len(temperatures)
        answer = [0] * n
        stack: List[int] = []  # indices with unresolved answers; temps non-increasing

        for j, temp in enumerate(temperatures):
            # Day j is the first strictly warmer day for every colder index on top.
            while stack and temperatures[stack[-1]] < temp:
                i = stack.pop()
                answer[i] = j - i
            stack.append(j)

        return answer


def _brute_force(temperatures: List[int]) -> List[int]:
    """O(n^2) reference used to cross-check the stack solution in the demo."""
    n = len(temperatures)
    out = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            if temperatures[j] > temperatures[i]:
                out[i] = j - i
                break
    return out


def _demo() -> None:
    sol = Solution()
    cases = [
        ([73, 74, 75, 71, 69, 72, 76, 73], [1, 1, 4, 2, 1, 1, 0, 0]),
        ([30, 40, 50, 60], [1, 1, 1, 0]),
        ([30, 60, 90], [1, 1, 0]),
        ([], []),
        ([50], [0]),
        # Strictly decreasing: nothing ever gets warmer.
        ([90, 80, 70, 60], [0, 0, 0, 0]),
        # Equal temperatures are NOT warmer; must wait for a strict increase.
        ([70, 70, 70, 71], [3, 2, 1, 0]),
        ([55, 38, 53, 81, 61, 93, 97, 32, 43, 78], [3, 1, 1, 2, 1, 1, 0, 1, 1, 0]),
    ]
    for temps, expected in cases:
        got = sol.dailyTemperatures(temps)
        status = "OK" if got == expected else "FAIL"
        print(f"{status}: temperatures={temps} -> {got} (expected {expected})")
        assert got == expected, f"739 dailyTemperatures({temps}) returned {got}, expected {expected}"

    # Randomised cross-check against the brute-force reference.
    import random

    rng = random.Random(739)
    for _ in range(200):
        temps = [rng.randint(30, 100) for _ in range(rng.randint(0, 40))]
        assert sol.dailyTemperatures(temps) == _brute_force(temps), f"mismatch on {temps}"
    print("OK: 200 random cases match the brute-force reference")


if __name__ == "__main__":
    _demo()
