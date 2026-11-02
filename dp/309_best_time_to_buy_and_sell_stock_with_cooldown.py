"""
LeetCode 309: Best Time to Buy and Sell Stock with Cooldown
Difficulty: Medium
Topic: Dynamic Programming / State Machine

Problem
-------
prices[i] is a stock's price on day i. Make as many buy/sell transactions as
you like, but you can hold at most one share at a time, and after you sell
you must wait one day (cooldown) before buying again. Return the maximum
profit.

Examples:
  prices = [1,2,3,0,2]  ->  3   (buy, sell, cooldown, buy, sell)
  prices = [1]          ->  0

Approach (thought process)
--------------------------
1. On any day you are in exactly one of three states:
     - hold: you own a share
     - sold: you sold today, so tomorrow is a forced cooldown
     - rest: you own nothing and are free to buy tomorrow
2. Write how each state can be reached from yesterday's states:
     hold_today = max(hold_yesterday,              # keep holding
                      rest_yesterday - price)      # buy (only from rest)
     sold_today = hold_yesterday + price           # sell what we held
     rest_today = max(rest_yesterday, sold_yesterday)  # idle or cooling down
   The cooldown rule lives in one place: you can only buy from "rest",
   and "sold" has to pass through "rest" first.
3. Start with hold = -inf (can't hold before buying), sold = -inf,
   rest = 0. The answer is max(sold, rest) at the end; ending while
   holding is never better.

Why it works: the three states cover every legal situation, and each
transition uses only the previous day, so the best value for each state is
built from the best values of the states it can come from.

Complexity:
  - Time: O(n), one pass.
  - Space: O(1), three rolling variables.
"""

from typing import List


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        hold, sold, rest = float("-inf"), float("-inf"), 0
        for p in prices:
            hold, sold, rest = max(hold, rest - p), hold + p, max(rest, sold)
        return int(max(sold, rest))


if __name__ == "__main__":
    s = Solution()
    cases = [
        ([1, 2, 3, 0, 2], 3),
        ([1], 0),
        ([5, 4, 3, 2, 1], 0),
        ([1, 2, 4], 3),
        ([6, 1, 6, 4, 3, 0, 2], 7),
    ]
    for prices, expected in cases:
        got = s.maxProfit(prices)
        assert got == expected, (prices, got, expected)
        print(f"{prices} -> {got}")
    print("All tests passed.")
