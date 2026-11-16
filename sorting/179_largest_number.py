"""
LeetCode 179: Largest Number
Difficulty: Medium
Topic: Sorting / Custom Comparator (Greedy)

Problem
-------
Given non-negative integers nums, arrange them so they form the largest
number. Return it as a string.

Approach (thought process)
--------------------------
1. Sorting by numeric value fails ([3, 30] -> "303" < "330"), and plain
   descending string sorting fails too: "30" > "3" as strings, so it puts
   "30" first and builds "303" again. We need the right "who goes first"
   rule.
2. Key idea: for two strings a and b, only two orders matter locally:
   a+b or b+a. Put a first exactly when a+b > b+a.
3. This rule is a valid total order (it is transitive), so sorting with it
   gives an arrangement where no adjacent swap helps, and that is the
   global maximum. That is the greedy "exchange argument".
4. Edge case: [0, 0] would give "00". If the first piece after sorting is
   "0", every piece is "0", so return "0".

Complexity
----------
Time:  O(n log n * k), where k is the max digit count (each comparison
       builds strings of length up to 2k).
Space: O(n * k) for the string copies.
"""

from functools import cmp_to_key
from typing import List


class Solution:
    def largestNumber(self, nums: List[int]) -> str:
        strs = [str(x) for x in nums]

        def compare(a: str, b: str) -> int:
            if a + b > b + a:
                return -1  # a goes first
            if a + b < b + a:
                return 1
            return 0

        strs.sort(key=cmp_to_key(compare))
        if strs[0] == "0":
            return "0"
        return "".join(strs)


if __name__ == "__main__":
    sol = Solution()
    assert sol.largestNumber([10, 2]) == "210"
    assert sol.largestNumber([3, 30, 34, 5, 9]) == "9534330"
    assert sol.largestNumber([0, 0]) == "0"
    assert sol.largestNumber([1]) == "1"
    assert sol.largestNumber([432, 43243]) == "43243432"
    print("All tests passed.")
