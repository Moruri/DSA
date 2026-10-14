"""
LeetCode 134: Gas Station
Difficulty: Medium
Topic: Greedy / Running Balance

Problem
-------
There are n stations on a circular route. Station i gives gas[i] fuel, and
driving from i to i + 1 costs cost[i]. Starting with an empty tank, return
the index of the station you can start from to drive one full lap, or -1 if
no start works. The answer, if it exists, is unique.

Example:
  gas = [1, 2, 3, 4, 5], cost = [3, 4, 5, 1, 2] -> 3
  gas = [2, 3, 4],       cost = [3, 4, 3]       -> -1

Approach (thought process)
--------------------------
1. Brute force tries each start and simulates a lap: O(n^2).
2. Look at net fuel per leg: diff[i] = gas[i] - cost[i]. If the sum of all
   diffs is negative, no start can ever finish the lap. That's the -1 test.
3. Otherwise, scan once and keep a running tank from the current candidate
   start. If the tank drops below zero at station i, then no station between
   the candidate and i can be the start either, so jump the candidate to
   i + 1 and reset the tank to 0.
4. When the scan ends and the total was non-negative, the last candidate is
   the answer.

Why skipping is safe: suppose we started at s and first went negative after
leaving station i. Every prefix from s up to just before i was non-negative,
so arriving at any middle station k came with a tank >= 0. Starting fresh at
k means arriving at i with even less (or the same), so it fails at i too.

Why the last candidate finishes the lap: total = (deficit before start) +
(gain from start to the end). The gain from the start to the end is >= 0,
and total >= 0 means it covers the deficit of the stations we skipped, so
wrapping around we never go negative.

Complexity:
  - Time: O(n), single pass.
  - Space: O(1).
"""

from typing import List


class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        total = 0
        tank = 0
        start = 0
        for i, (g, c) in enumerate(zip(gas, cost)):
            diff = g - c
            total += diff
            tank += diff
            if tank < 0:
                start = i + 1
                tank = 0
        return start if total >= 0 else -1


def _brute(gas: List[int], cost: List[int]) -> int:
    n = len(gas)
    for s in range(n):
        tank = 0
        ok = True
        for step in range(n):
            i = (s + step) % n
            tank += gas[i] - cost[i]
            if tank < 0:
                ok = False
                break
        if ok:
            return s
    return -1


if __name__ == "__main__":
    s = Solution()
    assert s.canCompleteCircuit([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]) == 3
    assert s.canCompleteCircuit([2, 3, 4], [3, 4, 3]) == -1
    assert s.canCompleteCircuit([5], [4]) == 0
    assert s.canCompleteCircuit([4], [5]) == -1
    assert s.canCompleteCircuit([3, 1, 1], [1, 2, 2]) == 0
    assert s.canCompleteCircuit([5, 1, 2, 3, 4], [4, 4, 1, 5, 1]) == 4

    import random

    for _ in range(1000):
        n = random.randint(1, 8)
        gas = [random.randint(0, 6) for _ in range(n)]
        cost = [random.randint(0, 6) for _ in range(n)]
        expected = _brute(gas, cost)
        got = s.canCompleteCircuit(gas, cost)
        # When several starts work (zero-net ties), any valid start is fine.
        if expected == -1:
            assert got == -1, (gas, cost, got)
        else:
            tank, ok = 0, True
            for step in range(n):
                i = (got + step) % n
                tank += gas[i] - cost[i]
                if tank < 0:
                    ok = False
            assert ok, (gas, cost, got)
    print("All tests passed.")
