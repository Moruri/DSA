"""
LeetCode 1094: Car Pooling
Difficulty: Medium
Topic: Arrays / Difference Array (sweep line)

Problem
-------
A car with `capacity` empty seats drives east only. trips[i] =
[numPassengers, from, to]: pick up numPassengers at km `from`, drop them at
km `to`. Return True if every trip can be served without ever exceeding
capacity.

Approach (thought process)
--------------------------
1. The only question is: at any kilometre, how many people are in the car?
   If that load never exceeds capacity, the answer is True.
2. Brute force adds each trip's passengers to every km in [from, to) --
   O(trips * distance). Wasteful: a trip only *changes* the load at two
   points.
3. Difference array: delta[from] += p, delta[to] -= p. (They leave at `to`,
   so that seat is free again at km `to` -- drop-off happens before
   pick-up at the same point.)
4. Sweep km 0..1000 keeping a running sum of delta; that running sum IS the
   load. The moment it exceeds capacity, return False.
5. Locations are bounded (<= 1000), so a fixed-size array beats sorting. If
   they were huge, sort the 2*T events (ties: drop-offs first) or use a
   min-heap of drop-off times -- same sweep-line idea.

Why it works: the prefix sum of delta at km x equals the total passengers
of trips with from <= x < to, which is exactly who is in the car at x.
Checking every x where the load can change covers every possible overflow.

Complexity
----------
Time:  O(T + M), T = trips, M = 1001 locations.
Space: O(M) for the delta array.
"""

from typing import List


class Solution:
    def carPooling(self, trips: List[List[int]], capacity: int) -> bool:
        delta = [0] * 1001
        for p, start, end in trips:
            delta[start] += p
            delta[end] -= p
        load = 0
        for change in delta:
            load += change
            if load > capacity:
                return False
        return True


def brute(trips: List[List[int]], capacity: int) -> bool:
    for x in range(1001):
        if sum(p for p, a, b in trips if a <= x < b) > capacity:
            return False
    return True


if __name__ == "__main__":
    s = Solution()
    cases = [
        ([[2, 1, 5], [3, 3, 7]], 4, False),
        ([[2, 1, 5], [3, 3, 7]], 5, True),
        ([[2, 1, 5], [3, 5, 7]], 3, True),  # drop-off before pick-up at km 5
        ([[3, 2, 7], [3, 7, 9], [8, 3, 9]], 11, True),
        ([[9, 0, 1], [3, 3, 7]], 4, False),
    ]
    for trips, cap, want in cases:
        got = s.carPooling(trips, cap)
        assert got == want, (trips, cap, got, want)
        print(f"carPooling({trips}, {cap}) = {got}")

    import random
    random.seed(1094)
    for _ in range(200):
        trips = []
        for _ in range(random.randint(1, 8)):
            a = random.randint(0, 20)
            b = random.randint(a + 1, 25)
            trips.append([random.randint(1, 5), a, b])
        cap = random.randint(1, 15)
        assert s.carPooling(trips, cap) == brute(trips, cap), (trips, cap)
    print("random cross-check vs brute force OK")
    print("All tests passed.")
