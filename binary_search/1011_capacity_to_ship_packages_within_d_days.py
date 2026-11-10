"""
LeetCode 1011: Capacity To Ship Packages Within D Days
Difficulty: Medium
Topic: Binary Search / Search on the Answer

Problem
-------
A conveyor belt holds packages with weights[i], which must ship in the given
order. Each day the ship is loaded with consecutive packages up to its
capacity. Return the smallest capacity that ships everything within `days`.

Approach (thought process)
--------------------------
1. We are not searching inside the array; we are searching for a number,
   the capacity. Ask: if I fix a capacity C, can I check it quickly?
   Yes: greedily fill each day until the next package would overflow, then
   start a new day. Greedy is optimal because putting a package on an
   earlier day never makes a later day worse. That check is O(n).
2. The check is monotone: if capacity C works, every C' > C also works
   (you can follow the same loading plan). A monotone yes/no predicate
   over a range of integers is exactly what binary search finds the
   boundary of.
3. Bounds: the ship must carry the heaviest package, so lo = max(weights).
   Carrying everything in one day always works, so hi = sum(weights).
4. Standard "first True" binary search: if mid works, the answer is mid or
   smaller (hi = mid); otherwise it must be bigger (lo = mid + 1).

Complexity
----------
Time:  O(n log(sum(weights)))  -- one O(n) greedy check per halving step.
Space: O(1).
"""

from typing import List


class Solution:
    def shipWithinDays(self, weights: List[int], days: int) -> int:
        def fits(capacity: int) -> bool:
            used_days, load = 1, 0
            for w in weights:
                if load + w > capacity:
                    used_days += 1
                    load = 0
                load += w
            return used_days <= days

        lo, hi = max(weights), sum(weights)
        while lo < hi:
            mid = (lo + hi) // 2
            if fits(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo


if __name__ == "__main__":
    s = Solution()
    cases = [
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5, 15),
        ([3, 2, 2, 4, 1, 4], 3, 6),
        ([1, 2, 3, 1, 1], 4, 3),
        ([10], 1, 10),
        ([5, 5, 5], 3, 5),
    ]
    for weights, days, expected in cases:
        got = s.shipWithinDays(weights, days)
        assert got == expected, (weights, days, got, expected)
        print(f"weights={weights}, days={days} -> {got}")
    print("All tests passed.")
