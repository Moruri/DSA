"""
LeetCode 73: Set Matrix Zeroes
Difficulty: Medium
Topic: Matrix / In-place Markers

Problem
-------
Given an m x n integer matrix, if an element is 0, set its entire row and
column to 0. Do it in place.

Example:
  Input:  [[1,1,1],
           [1,0,1],
           [1,1,1]]
  Output: [[1,0,1],
           [0,0,0],
           [1,0,1]]

Approach (thought process)
--------------------------
1. The trap: zeroing rows and columns as you scan creates NEW zeros, and
   later cells would mistake them for original zeros and wipe out too much.
   So we must first *record* which rows/cols to clear, then clear them.
2. Easy version: two sets (zero_rows, zero_cols) -> O(m + n) extra space.
   The follow-up asks for O(1) extra space, so we need somewhere free to
   keep those marks.
3. Trick: use the matrix's own first row and first column as the marker
   arrays. If matrix[i][j] == 0, set matrix[i][0] = 0 (row i must clear)
   and matrix[0][j] = 0 (column j must clear). Those cells are going to be
   zeroed anyway, so overwriting them loses nothing we need.
4. One clash: matrix[0][0] sits in both the first row and the first column,
   so it can't mean both. Keep a separate boolean, first_col_zero, for the
   first column and let matrix[0][0] speak for the first row.
5. Clear the inner cells (i >= 1, j >= 1) using the markers. Then clear the
   first row (if matrix[0][0] == 0) and the first column (if first_col_zero)
   LAST, because they're still being read as markers until then.

Why it works: every original zero leaves a mark in its row's first cell and
its column's top cell before anything is overwritten, and the marker row /
column themselves are only cleared after all other cells have read them.

Complexity: O(m * n) time, O(1) extra space.
"""

from typing import List


class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        m, n = len(matrix), len(matrix[0])
        first_col_zero = False

        # Pass 1: record marks in the first row / first column.
        for i in range(m):
            if matrix[i][0] == 0:
                first_col_zero = True
            for j in range(1, n):
                if matrix[i][j] == 0:
                    matrix[i][0] = 0
                    matrix[0][j] = 0

        # Pass 2: clear inner cells from the marks.
        for i in range(1, m):
            for j in range(1, n):
                if matrix[i][0] == 0 or matrix[0][j] == 0:
                    matrix[i][j] = 0

        # Pass 3: clear the marker row and column last.
        if matrix[0][0] == 0:
            for j in range(n):
                matrix[0][j] = 0
        if first_col_zero:
            for i in range(m):
                matrix[i][0] = 0


if __name__ == "__main__":
    s = Solution()
    cases = [
        ([[1, 1, 1], [1, 0, 1], [1, 1, 1]],
         [[1, 0, 1], [0, 0, 0], [1, 0, 1]]),
        ([[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]],
         [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]),
        ([[1, 2], [3, 4]], [[1, 2], [3, 4]]),           # no zeros
        ([[1, 0, 3]], [[0, 0, 0]]),                     # single row
        ([[1], [0], [3]], [[0], [0], [0]]),             # single column
        ([[1, 2, 3], [4, 5, 6], [0, 8, 9]],             # zero only in col 0
         [[0, 2, 3], [0, 5, 6], [0, 0, 0]]),
    ]
    for grid, expected in cases:
        s.setZeroes(grid)
        assert grid == expected, grid
    print("73 Set Matrix Zeroes: all tests passed")
