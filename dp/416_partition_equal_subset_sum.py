"""
LeetCode 416: Partition Equal Subset Sum
Difficulty: Medium
Topic: Dynamic Programming / 0-1 Knapsack (subset sum)

Problem
-------
Given a non-empty array nums of positive integers, return True if you can
split it into two subsets whose sums are equal.

Example:
  Input:  nums = [1, 5, 11, 5]
  Output: True   ([1, 5, 5] and [11])

Approach (thought process)
--------------------------
1. If the two halves are equal, each one sums to total / 2. So an odd total
   is an instant False, and otherwise the question becomes: "is there a
   subset that sums to target = total // 2?" The other half is automatically
   whatever is left over. That's the classic subset-sum problem.
2. Brute force tries all 2^n subsets. But we don't care *which* subset hits
   a sum, only *whether* some sum is reachable, and sums are bounded by
   target. That small, bounded state space is the cue for DP.
3. Let reachable[s] mean "some subset of the numbers seen so far sums to s".
   Start with reachable[0] = True (the empty subset). For each number x,
   any already-reachable sum s gives a new reachable sum s + x.
4. Each number can be used at most once (0-1 knapsack), so sweep s from
   target DOWN to x. Going downward means reachable[s - x] still reflects
   the state *before* x was added, so x can't be counted twice. (Sweeping
   upward would turn this into the unbounded "use x many times" version.)
5. Return reachable[target]. We can stop early the moment it flips True.

Why it works: after processing the first i numbers, reachable holds exactly
the set of subset sums of those i numbers capped at target, by induction:
every subset either skips x (old value kept) or includes it (s - x was
reachable before).

Complexity: O(n * target) time, O(target) space, where target = sum / 2.

Bonus one-liner: the same DP fits in a Python int used as a bitset:
bits |= bits << x, then test bit `target`. Same idea, much faster in practice.
"""

from typing import List


class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        total = sum(nums)
        if total % 2:
            return False
        target = total // 2

        reachable = [False] * (target + 1)
        reachable[0] = True
        for x in nums:
            for s in range(target, x - 1, -1):  # downward: use x at most once
                if reachable[s - x]:
                    reachable[s] = True
            if reachable[target]:
                return True
        return reachable[target]

    def canPartitionBitset(self, nums: List[int]) -> bool:
        total = sum(nums)
        if total % 2:
            return False
        bits = 1  # bit s set  <=>  sum s is reachable
        for x in nums:
            bits |= bits << x
        return bool((bits >> (total // 2)) & 1)


if __name__ == "__main__":
    s = Solution()
    cases = [
        ([1, 5, 11, 5], True),
        ([1, 2, 3, 5], False),  # total 11 is odd
        ([2, 2, 3, 5], False),  # even total 12, but no subset hits 6
        ([1, 1], True),
        ([100], False),
        ([3, 3, 3, 4, 5], True),  # 3+3+3 vs 4+5
    ]
    for nums, expected in cases:
        assert s.canPartition(nums) == expected, nums
        assert s.canPartitionBitset(nums) == expected, nums
    print("416 Partition Equal Subset Sum: all tests passed")
