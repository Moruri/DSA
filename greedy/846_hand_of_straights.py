"""
LeetCode 846: Hand of Straights
Difficulty: Medium
Topic: Greedy / Hashing (smallest card must start a run)

Problem
-------
Alice has cards hand[i]. She wants to rearrange them into groups of size
groupSize where each group is groupSize consecutive values. Return True if
she can, otherwise False.

Example 1: hand = [1,2,3,6,2,3,4,7,8], groupSize = 3 -> True
           ([1,2,3], [2,3,4], [6,7,8])
Example 2: hand = [1,2,3,4,5], groupSize = 4 -> False

Approach (thought process)
--------------------------
1. Quick reject: if len(hand) isn't divisible by groupSize, it's impossible.
2. Look at the smallest card value x that still has copies left. Nothing
   smaller exists, so x cannot be the middle or end of any run. It MUST be
   the start of a run x, x+1, ..., x+groupSize-1. There is no choice to
   make, which is why greedy is safe here.
3. Even better, all count[x] copies of x must each start their own run, so
   we can peel off count[x] runs at once: subtract count[x] from each of
   x..x+groupSize-1. If any of those has fewer copies than needed, fail.
4. Walk the distinct values in sorted order; a value whose count is already
   0 (fully used by earlier runs) is skipped. Negative counts can't happen
   because we fail before going below zero.

Why it works: the forced move in step 2 never rules out a valid answer,
since every valid grouping must contain those same runs starting at x.
Repeating the forced move either uses up every card or proves failure.

Complexity: O(n + k log k) time where k = number of distinct values
(the sort), times groupSize for the inner subtraction in the worst case:
O(n log n + k * groupSize). O(k) extra space for the counter.
"""

from __future__ import annotations

from collections import Counter
from typing import List


class Solution:
    def isNStraightHand(self, hand: List[int], groupSize: int) -> bool:
        if len(hand) % groupSize:
            return False
        count = Counter(hand)
        for x in sorted(count):
            need = count[x]
            if need == 0:
                continue
            for v in range(x, x + groupSize):
                if count[v] < need:
                    return False
                count[v] -= need
        return True


if __name__ == "__main__":
    s = Solution()
    cases = [
        ([1, 2, 3, 6, 2, 3, 4, 7, 8], 3, True),
        ([1, 2, 3, 4, 5], 4, False),
        ([1], 1, True),
        ([1, 1, 2, 2, 3, 3], 3, True),
        ([1, 2, 4, 5, 6, 7], 3, False),
        ([8, 10, 12], 3, False),
    ]
    for hand, k, expected in cases:
        got = s.isNStraightHand(hand, k)
        assert got == expected, (hand, k, got, expected)
        print(f"{hand}, groupSize={k} -> {got}")
    print("All tests passed.")
