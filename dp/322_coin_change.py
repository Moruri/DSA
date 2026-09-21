"""
LeetCode 322: Coin Change
Link: https://leetcode.com/problems/coin-change/
Difficulty: Medium
Topic: Dynamic Programming

Problem
-------
You are given an integer array coins representing coins of different
denominations and an integer amount representing a total amount of money.

Return the fewest number of coins that you need to make up that amount. If
it is impossible to make that amount with any combination of the coins,
return -1.

You may assume that you have an infinite number of each kind of coin.

Example 1:
  Input:  coins = [1, 2, 5], amount = 11
  Output: 3
  Explanation: 11 = 5 + 5 + 1

Example 2:
  Input:  coins = [2], amount = 3
  Output: -1

Example 3:
  Input:  coins = [1], amount = 0
  Output: 0

Approach (thought process)
--------------------------
1. Greedy (largest coin first) fails — e.g. coins=[1,3,4], amount=6 wants
   3+3 (2 coins), not 4+1+1 (3). Need exact optimality.
2. Define dp[x] = fewest coins needed to make amount x. Then
     dp[0] = 0
     dp[x] = min(dp[x - coin] + 1) over every coin <= x that is reachable
   Unreachable amounts stay at a sentinel larger than any valid answer
   (amount + 1 works: you never need more than `amount` coins of size 1).
3. Fill bottom-up from 1..amount. For each amount x, try every coin: if
   x - coin is reachable, candidate = dp[x - coin] + 1, keep the min.
4. Unlimited supply is free: the outer loop over amounts means each coin
   can be reused as soon as smaller sub-amounts are solved.
5. After the fill, if dp[amount] is still the sentinel, return -1; else
   return dp[amount].

Complexity: O(amount * len(coins)) time, O(amount) space.
"""

from __future__ import annotations

from typing import List


class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        """Return fewest coins to make amount, or -1 if impossible."""
        if amount == 0:
            return 0

        # Sentinel: more coins than any feasible solution could need.
        unreachable = amount + 1
        dp = [unreachable] * (amount + 1)
        dp[0] = 0

        for x in range(1, amount + 1):
            for coin in coins:
                if coin <= x and dp[x - coin] != unreachable:
                    candidate = dp[x - coin] + 1
                    if candidate < dp[x]:
                        dp[x] = candidate

        return dp[amount] if dp[amount] != unreachable else -1


def _demo() -> None:
    sol = Solution()
    cases = [
        ([1, 2, 5], 11, 3),
        ([2], 3, -1),
        ([1], 0, 0),
        ([1], 1, 1),
        ([1], 2, 2),
        ([1, 3, 4], 6, 2),  # greedy would pick 4+1+1 = 3; optimal is 3+3
        ([2, 5, 10, 1], 27, 4),
        ([2147483647], 2, -1),
        ([1, 2, 5], 100, 20),
    ]
    for coins, amount, expected in cases:
        got = sol.coinChange(coins, amount)
        status = "OK" if got == expected else "FAIL"
        print(
            f"{status}: coins={coins}, amount={amount} -> {got} "
            f"(expected {expected})"
        )
        assert got == expected, (
            f"322 coinChange({coins}, {amount}) returned {got}, "
            f"expected {expected}"
        )


if __name__ == "__main__":
    _demo()
