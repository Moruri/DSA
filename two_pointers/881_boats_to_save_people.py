"""
LeetCode 881: Boats to Save People
Difficulty: Medium
Topic: Two Pointers / Greedy Pairing

Problem
-------
people[i] is a weight; every boat carries at most 2 people with total weight
<= limit (each person weighs <= limit). Return the minimum number of boats.

Approach (thought process)
--------------------------
1. The heaviest person is the hardest to place: they need a boat no matter
   what. The only question is whether someone can ride with them.
2. The best partner for the heaviest person is the LIGHTEST person left:
   if even the lightest doesn't fit, nobody does, so the heavy one sails
   alone. If the lightest fits, pairing them never hurts (exchange argument
   below).
3. Sort, put i at the lightest and j at the heaviest. Each step launches one
   boat with people[j] (j -= 1) and also takes people[i] if
   people[i] + people[j] <= limit (i += 1). Stop when the pointers cross.

Why it works (exchange argument): take any optimal plan where heaviest H
rides with X (or alone) and lightest L rides with Y (or alone). If
L + H <= limit, swap L and X: the boat {H, L} fits by assumption, and
{X, Y} fits because Y <= H gives X + Y <= X + H <= limit (if a seat was
empty, that person simply rides alone). Same number of boats, so greedily
pairing L with H is always safe.

Complexity
----------
Time:  O(n log n) for the sort; the two-pointer sweep is O(n).
Space: O(1) extra beyond the sort (O(n) if you count Python's sort buffer).
"""

from typing import List


class Solution:
    def numRescueBoats(self, people: List[int], limit: int) -> int:
        people = sorted(people)
        i, j = 0, len(people) - 1
        boats = 0
        while i <= j:
            if people[i] + people[j] <= limit:
                i += 1  # lightest rides along
            j -= 1      # heaviest always leaves on this boat
            boats += 1
        return boats


def brute(people: List[int], limit: int) -> int:
    """Exact minimum via bitmask DP over who has been rescued."""
    n = len(people)
    full = (1 << n) - 1
    INF = float("inf")
    dp = [INF] * (1 << n)
    dp[0] = 0
    for mask in range(1 << n):
        if dp[mask] == INF:
            continue
        free = [k for k in range(n) if not mask >> k & 1]
        if not free:
            continue
        a = free[0]  # someone must take the first free person
        dp[mask | 1 << a] = min(dp[mask | 1 << a], dp[mask] + 1)
        for b in free[1:]:
            if people[a] + people[b] <= limit:
                m2 = mask | 1 << a | 1 << b
                dp[m2] = min(dp[m2], dp[mask] + 1)
    return dp[full]


if __name__ == "__main__":
    s = Solution()
    cases = [
        ([1, 2], 3, 1),
        ([3, 2, 2, 1], 3, 3),
        ([3, 5, 3, 4], 5, 4),
        ([5, 1, 4, 2], 6, 2),
        ([2], 5, 1),
    ]
    for people, limit, want in cases:
        got = s.numRescueBoats(people, limit)
        assert got == want, (people, limit, got, want)
        print(f"numRescueBoats({people}, {limit}) = {got}")

    import random
    random.seed(881)
    for _ in range(300):
        limit = random.randint(1, 10)
        people = [random.randint(1, limit) for _ in range(random.randint(1, 8))]
        assert s.numRescueBoats(people, limit) == brute(people, limit), (people, limit)
    print("random cross-check vs bitmask DP OK")
    print("All tests passed.")
