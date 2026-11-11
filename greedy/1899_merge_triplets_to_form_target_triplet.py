"""
LeetCode 1899: Merge Triplets to Form Target Triplet
Difficulty: Medium
Topic: Greedy

Problem
-------
You have a list of triplets and a target [x, y, z]. An operation picks two
triplets i, j and sets triplets[j] = [max(a_i, a_j), max(b_i, b_j),
max(c_i, c_j)]. Return True if some triplet can become exactly the target.

Approach (thought process)
--------------------------
1. Merging only takes element-wise maxima, so values can only go up. Any
   triplet with a coordinate larger than the target's is poison: once it is
   merged in, that coordinate overshoots forever. Throw those away.
2. Every remaining "safe" triplet is <= target in all three positions, so
   merging any of them can never overshoot. Merging is also free to repeat,
   so the best we can do is merge ALL safe triplets together.
3. The merged result equals the target exactly when, for each coordinate,
   at least one safe triplet hits the target value there. So just track
   three booleans (or the running max of safe triplets) and check at the end.
4. Why greedy is correct: including an extra safe triplet never hurts (it
   can't exceed the target) and may help, so "take every safe one" is
   optimal; excluding unsafe ones is forced.

Complexity
----------
Time:  O(n)  -- one pass over the triplets.
Space: O(1).
"""

from typing import List


class Solution:
    def mergeTriplets(self, triplets: List[List[int]], target: List[int]) -> bool:
        best = [0, 0, 0]
        for t in triplets:
            if t[0] <= target[0] and t[1] <= target[1] and t[2] <= target[2]:
                best = [max(best[k], t[k]) for k in range(3)]
        return best == target


if __name__ == "__main__":
    s = Solution()
    cases = [
        ([[2, 5, 3], [1, 8, 4], [1, 7, 5]], [2, 7, 5], True),
        ([[3, 4, 5], [4, 5, 6]], [3, 2, 5], False),
        ([[2, 5, 3], [2, 3, 4], [1, 2, 5], [5, 2, 3]], [5, 5, 5], True),
        ([[1, 1, 1]], [1, 1, 1], True),
        ([[1, 3, 1], [3, 1, 1]], [3, 3, 2], False),
    ]
    for triplets, target, expected in cases:
        got = s.mergeTriplets(triplets, target)
        assert got == expected, (triplets, target, got, expected)
        print(f"triplets={triplets}, target={target} -> {got}")
    print("All tests passed.")
