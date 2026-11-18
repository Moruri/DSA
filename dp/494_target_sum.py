"""
LeetCode 494: Target Sum
Difficulty: Medium
Topic: Dynamic Programming (0/1 Knapsack counting)

Problem
-------
Given an integer array nums and an integer target, put a '+' or '-' in front
of every number. Return how many sign assignments make the expression equal
to target.

Approach (thought process)
--------------------------
1. Brute force tries all 2^n sign patterns. Too slow for n = 20 with many
   test cases, and it repeats the same (index, running sum) states.
2. Algebra trick: split nums into P (the '+' group) and N (the '-' group).
       sum(P) - sum(N) = target
       sum(P) + sum(N) = total
   Add them: 2 * sum(P) = target + total, so sum(P) = (target + total) / 2.
   The question becomes "how many subsets of nums sum to S?", a classic
   counting knapsack.
3. Quick rejects: if |target| > total, or (target + total) is odd, no
   subset can work, so return 0.
4. Counting knapsack: ways[s] = number of subsets (of the numbers seen so
   far) summing to s. Start with ways[0] = 1 (the empty subset). For each
   num, loop s from S down to num and do ways[s] += ways[s - num].
   Going downward means each number is used at most once (0/1 knapsack):
   ways[s - num] still holds the value from before this num was added.
5. Zeros work for free: a 0 doubles every count (+0 and -0 are different
   sign choices), and ways[s] += ways[s - 0] does exactly that.

Complexity
----------
Time:  O(n * S), with S = (total + target) / 2 <= 1000 under the constraints.
Space: O(S) for the 1-D ways array.
"""

from typing import List


class Solution:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        total = sum(nums)
        if abs(target) > total or (total + target) % 2:
            return 0
        goal = (total + target) // 2

        ways = [0] * (goal + 1)
        ways[0] = 1
        for num in nums:
            for s in range(goal, num - 1, -1):
                ways[s] += ways[s - num]
        return ways[goal]


def brute(nums: List[int], target: int) -> int:
    from itertools import product

    return sum(
        1
        for signs in product((1, -1), repeat=len(nums))
        if sum(s * x for s, x in zip(signs, nums)) == target
    )


if __name__ == "__main__":
    import random

    sol = Solution()
    assert sol.findTargetSumWays([1, 1, 1, 1, 1], 3) == 5
    assert sol.findTargetSumWays([1], 1) == 1
    assert sol.findTargetSumWays([1], 2) == 0
    assert sol.findTargetSumWays([0, 0, 0, 0, 0, 0, 0, 0, 1], 1) == 256
    assert sol.findTargetSumWays([100], -200) == 0
    assert sol.findTargetSumWays([2, 3], 0) == 0  # odd parity reject
    random.seed(494)
    for _ in range(300):
        nums = [random.randint(0, 6) for _ in range(random.randint(1, 9))]
        target = random.randint(-15, 15)
        assert sol.findTargetSumWays(nums, target) == brute(nums, target)
    print("All tests passed.")
