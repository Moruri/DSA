"""
LeetCode 221: Maximal Square
Difficulty: Medium
Topic: Dynamic Programming / Matrix

Problem
-------
Given an m x n binary matrix filled with '0' and '1', find the largest
square containing only '1's and return its area.

Examples:
  [["1","0","1","0","0"],
   ["1","0","1","1","1"],
   ["1","1","1","1","1"],
   ["1","0","0","1","0"]]  ->  4     # the 2x2 block of 1s

  [["0","1"],
   ["1","0"]]              ->  1

  [["0"]]                  ->  0

Approach (thought process)
--------------------------
1. Brute force tries every cell as the top-left of a candidate square and
   expands the side until a 0 appears. That is O(m n * min(m, n)^2) and
   repeats a lot of the same "is this region all 1s?" work.
2. The reusable question is: if I stand on cell (i, j) and it is a '1',
   what is the side of the largest square whose bottom-right corner is
   right here? Call that dp[i][j].
3. A k x k square ending at (i, j) is a '1' at (i, j) plus three
   overlapping (k-1) x (k-1) squares:
     - one ending just above      (i-1, j)
     - one ending just to the left (i, j-1)
     - one ending on the diagonal  (i-1, j-1)
   If any of those three is smaller than k-1, a 0 is hiding in that
   direction and we cannot grow to k. So:
     dp[i][j] = 0                                 if matrix[i][j] == '0'
     dp[i][j] = min(above, left, diag) + 1        if matrix[i][j] == '1'
4. Pad dp with an extra first row and column of zeros so the top/left
   border needs no special case — those zeros mean "no square lives
   outside the grid". Track the best side and return best * best.
5. Why area, not side? The problem asks for area, and a square's area
   is side². The max area square is always the one with the max side
   (squares don't have the "wide but short" tradeoff rectangles do).

Why it works: every possible square has a unique bottom-right corner, so
scanning every cell enumerates every candidate. The recurrence is exact
because a square is rigid — the shortest of the three neighboring squares
is the true bottleneck. Cells that are '0' correctly start a side of 0,
which poisons any larger square that would have needed them.

Complexity:
  - Time: O(m n) — constant work per cell.
  - Space: O(m n) for the table (can drop to O(n) with two rolling rows,
    since we only read the previous row and the current row's left cell).
"""

from typing import List


class Solution:
    def maximalSquare(self, matrix: List[List[str]]) -> int:
        if not matrix or not matrix[0]:
            return 0

        rows, cols = len(matrix), len(matrix[0])
        # dp[i][j] = max side of a square whose bottom-right is matrix[i-1][j-1]
        dp = [[0] * (cols + 1) for _ in range(rows + 1)]
        best = 0

        for i in range(1, rows + 1):
            for j in range(1, cols + 1):
                if matrix[i - 1][j - 1] == "1":
                    dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1
                    if dp[i][j] > best:
                        best = dp[i][j]

        return best * best


if __name__ == "__main__":
    sol = Solution()
    cases = [
        (
            [
                ["1", "0", "1", "0", "0"],
                ["1", "0", "1", "1", "1"],
                ["1", "1", "1", "1", "1"],
                ["1", "0", "0", "1", "0"],
            ],
            4,
        ),
        ([["0", "1"], ["1", "0"]], 1),
        ([["0"]], 0),
        ([["1"]], 1),
        ([["1", "1"], ["1", "1"]], 4),
        (
            [
                ["1", "1", "1"],
                ["1", "1", "1"],
                ["1", "1", "1"],
            ],
            9,
        ),
        (
            [
                ["1", "1", "1"],
                ["1", "0", "1"],
                ["1", "1", "1"],
            ],
            1,
        ),
        ([["0", "0"], ["0", "0"]], 0),
        (
            [
                ["1", "0", "1", "1", "1"],
                ["1", "0", "1", "1", "1"],
                ["1", "1", "1", "1", "1"],
                ["1", "0", "0", "1", "0"],
            ],
            9,
        ),
    ]
    for matrix, want in cases:
        got = sol.maximalSquare(matrix)
        assert got == want, (matrix, got, want)
        print(f"area={got}  (want {want})")
    print("all tests passed")
