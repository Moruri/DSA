"""
LeetCode 78: Subsets
Difficulty: Medium
Topic: Backtracking

Problem
-------
Given an integer array nums of unique elements, return all possible subsets
(the power set). The solution set must not contain duplicate subsets. Return
the subsets in any order.

Example 1:
  Input:  nums = [1, 2, 3]
  Output: [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]
  (order may vary)

Example 2:
  Input:  nums = [0]
  Output: [[], [0]]

Approach (thought process)
--------------------------
1. The power set of n distinct elements has exactly 2^n members. Generating
   them by iterating a bitmask 0..(2^n - 1) works, but the recursive
   "include / skip" tree is the standard interview framing and generalizes
   cleanly to combinations / permutations.
2. Backtracking: at index i decide whether to include nums[i] in the current
   path. Recurse to i+1 either way. When i == n, the path is a complete
   subset — copy it into the answer.
3. Equivalently, for each start index, append nums[start], recurse from
   start+1 (only later elements, so no duplicates), then pop. That "choose
   next element from the suffix" form is used here.
4. Always snapshot `path[:]` when recording a subset; mutating the shared
   path later would corrupt earlier results.

Complexity: O(n · 2^n) time (copy each subset), O(n) recursion depth /
extra space beyond the output.
"""

from __future__ import annotations

from typing import List


class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        """Return the power set of nums (unique elements, any order)."""
        answer: List[List[int]] = []
        path: List[int] = []

        def dfs(start: int) -> None:
            answer.append(path[:])
            for i in range(start, len(nums)):
                path.append(nums[i])
                dfs(i + 1)
                path.pop()

        dfs(0)
        return answer


def _normalize(sets: List[List[int]]) -> List[tuple]:
    return sorted(tuple(sorted(s)) for s in sets)


def _demo() -> None:
    sol = Solution()
    cases = [
        ([1, 2, 3], [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]),
        ([0], [[], [0]]),
        ([1], [[], [1]]),
    ]
    for nums, expected in cases:
        got = sol.subsets(nums)
        ok = _normalize(got) == _normalize(expected)
        status = "OK" if ok else "FAIL"
        print(f"{status}: nums={nums} -> {got} (expected any order of {expected})")
        assert ok, f"78 subsets({nums}) returned {got}, expected {expected}"
        assert len(got) == 2 ** len(nums)


if __name__ == "__main__":
    _demo()
