"""LeetCode 40 — Combination Sum II (Medium).

Find all unique combinations of candidates that sum to target. Each number
may be used once, and the input can contain duplicates, but the answer must
not contain duplicate combinations.

Approach: sort, then backtrack. At each depth, skip a value equal to the one
just tried at the same depth (i > start and c[i] == c[i-1]); that stops
duplicate combos at the source without a set. Sorting also lets us break as
soon as a candidate exceeds what's left.
"""
from typing import List


class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        candidates.sort()
        result: List[List[int]] = []
        path: List[int] = []

        def backtrack(start: int, remaining: int) -> None:
            if remaining == 0:
                result.append(path[:])
                return
            for i in range(start, len(candidates)):
                c = candidates[i]
                if i > start and c == candidates[i - 1]:
                    continue          # same value already explored at this depth
                if c > remaining:
                    break             # sorted: everything after is too big too
                path.append(c)
                backtrack(i + 1, remaining - c)   # i + 1: each element used once
                path.pop()

        backtrack(0, target)
        return result


if __name__ == "__main__":
    s = Solution()
    assert s.combinationSum2([10, 1, 2, 7, 6, 1, 5], 8) == [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]
    assert s.combinationSum2([2, 5, 2, 1, 2], 5) == [[1, 2, 2], [5]]
    assert s.combinationSum2([1, 1, 1, 1], 2) == [[1, 1]]
    assert s.combinationSum2([3], 2) == []
    print("40 Combination Sum II: all tests passed")
