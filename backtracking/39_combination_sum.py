"""
LeetCode 39: Combination Sum
Link: https://leetcode.com/problems/combination-sum/
Difficulty: Medium
Topic: Backtracking

Problem
-------
Given an array of distinct integers candidates and a target integer target,
return a list of all unique combinations of candidates where the chosen
numbers sum to target. You may reuse the same number unlimited times.

Two combinations are unique if the frequency of at least one of the chosen
numbers differs. The combinations may be returned in any order.

Example 1:
  Input:  candidates = [2, 3, 6, 7], target = 7
  Output: [[2, 2, 3], [7]]

Example 2:
  Input:  candidates = [2, 3, 5], target = 8
  Output: [[2, 2, 2, 2], [2, 3, 3], [3, 5]]

Example 3:
  Input:  candidates = [2], target = 1
  Output: []

Approach (thought process)
--------------------------
1. Exhaustive search over multisets that sum to target is natural
   backtracking: at each step pick a candidate, subtract it from the
   remaining target, and recurse.
2. To avoid duplicate combinations like [2, 3] and [3, 2], only consider
   candidates at or after the current start index (combinations, not
   permutations). Reusing the same value is allowed by recursing with the
   same index rather than index + 1.
3. Sort first so we can prune: once candidates[i] > remaining, later
   (larger) values cannot help either.
4. When remaining hits 0, snapshot the path into the answer. When it goes
   negative, backtrack. Always pop after exploring a branch.

Complexity: O(n^{T/m}) time in the worst case (n candidates, T = target,
m = smallest candidate), O(T/m) recursion depth beyond the output.
"""

from __future__ import annotations

from typing import List


class Solution:
    def combinationSum(
        self, candidates: List[int], target: int
    ) -> List[List[int]]:
        """Return all unique combinations that sum to target (reuse allowed)."""
        candidates = sorted(candidates)
        answer: List[List[int]] = []
        path: List[int] = []

        def dfs(start: int, remaining: int) -> None:
            if remaining == 0:
                answer.append(path[:])
                return
            for i in range(start, len(candidates)):
                coin = candidates[i]
                if coin > remaining:
                    break
                path.append(coin)
                dfs(i, remaining - coin)
                path.pop()

        dfs(0, target)
        return answer


def _normalize(combos: List[List[int]]) -> List[tuple]:
    return sorted(tuple(sorted(c)) for c in combos)


def _demo() -> None:
    sol = Solution()
    cases = [
        ([2, 3, 6, 7], 7, [[2, 2, 3], [7]]),
        ([2, 3, 5], 8, [[2, 2, 2, 2], [2, 3, 3], [3, 5]]),
        ([2], 1, []),
        ([1], 1, [[1]]),
        ([1], 2, [[1, 1]]),
        ([2, 3], 5, [[2, 3]]),
        ([8, 7, 4, 3], 11, [[3, 4, 4], [3, 8], [4, 7]]),
    ]
    for candidates, target, expected in cases:
        got = sol.combinationSum(candidates, target)
        ok = _normalize(got) == _normalize(expected)
        status = "OK" if ok else "FAIL"
        print(
            f"{status}: candidates={candidates}, target={target} -> {got} "
            f"(expected any order of {expected})"
        )
        assert ok, (
            f"39 combinationSum({candidates}, {target}) returned {got}, "
            f"expected {expected}"
        )


if __name__ == "__main__":
    _demo()
