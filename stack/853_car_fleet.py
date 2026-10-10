"""
LeetCode 853: Car Fleet
Link: https://leetcode.com/problems/car-fleet/
Difficulty: Medium
Topic: Stack / Sorting

Problem
-------
n cars drive toward a destination `target` miles away on a one-lane road.
Car i starts at position[i] with speed speed[i]. A car can never pass the car
ahead; if it catches up it slows down and they drive together as one fleet.
A car that catches a fleet exactly at the destination still joins it.
Return how many fleets arrive at the destination.

Example 1:
  Input:  target = 12, position = [10, 8, 0, 5, 3], speed = [2, 4, 1, 1, 3]
  Output: 3

Example 2:
  Input:  target = 100, position = [0, 2, 4], speed = [4, 2, 1]
  Output: 1

Approach (thought process)
--------------------------
1. Simulating the road minute by minute is messy (fractional meeting points,
   chains of merges). Instead, ask one question per car: if the road were
   empty, when would it arrive? time = (target - position) / speed.
2. Order matters only from the front. Sort cars by position, closest to the
   target first. The leading car is never blocked, so it starts a fleet.
3. Walk backward down the road. A car behind can't pass, so if its solo time
   is <= the arrival time of the fleet just ahead, it catches up before (or
   exactly at) the target and is absorbed: it adds nothing new. If its solo
   time is strictly larger, it never catches up and becomes the head of a new,
   slower fleet whose arrival time is its own time.
4. Absorbed cars never change the fleet's arrival time (the fleet moves at its
   slow leader's pace), so we only need to remember the arrival time of the
   most recent fleet. That's a stack where we only ever peek the top; its
   final size is the answer.

Complexity: O(n log n) time for the sort, O(n) space.
"""

from __future__ import annotations

from typing import List


class Solution:
    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:
        cars = sorted(zip(position, speed), reverse=True)  # closest to target first
        fleets: List[float] = []  # arrival time of each fleet, front to back
        for pos, spd in cars:
            t = (target - pos) / spd
            if not fleets or t > fleets[-1]:
                fleets.append(t)  # can't catch the fleet ahead: new fleet
            # else: catches up and merges, fleet time unchanged
        return len(fleets)


def _brute(target: int, position: List[int], speed: List[int]) -> int:
    # Exact rational simulation of "can't pass" via the same arrival-time rule
    # but computed pairwise: a car's effective arrival = max(own time, effective
    # arrival of the car directly ahead). Count distinct effective arrivals.
    from fractions import Fraction

    cars = sorted(zip(position, speed), reverse=True)
    eff: List[Fraction] = []
    for pos, spd in cars:
        t = Fraction(target - pos, spd)
        eff.append(max(t, eff[-1]) if eff else t)
    return len(set(eff))


def _demo() -> None:
    sol = Solution()
    cases = [
        (12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3], 3),
        (10, [3], [3], 1),
        (100, [0, 2, 4], [4, 2, 1], 1),
        (10, [0, 4, 2], [2, 1, 3], 1),
        (10, [6, 8], [3, 2], 2),
    ]
    for target, pos, spd, expected in cases:
        got = sol.carFleet(target, pos, spd)
        status = "OK" if got == expected else "FAIL"
        print(f"{status}: carFleet({target}, {pos}, {spd}) -> {got} (expected {expected})")
        assert got == expected

    import random

    rng = random.Random(853)
    for _ in range(300):
        target = rng.randint(10, 40)
        n = rng.randint(1, 8)
        pos = rng.sample(range(target), n)
        spd = [rng.randint(1, 6) for _ in range(n)]
        assert sol.carFleet(target, pos, spd) == _brute(target, pos, spd), (target, pos, spd)
    print("OK: 300 random cases match exact-fraction reference")


if __name__ == "__main__":
    _demo()
