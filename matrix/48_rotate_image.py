"""
LeetCode 48: Rotate Image
Link: https://leetcode.com/problems/rotate-image/
Difficulty: Medium
Topic: Matrix / In-place

Problem
-------
You are given an n x n 2D matrix representing an image. Rotate the image by
90 degrees clockwise.

You must rotate the image in-place — modify the input 2D matrix directly.
Do not allocate another 2D matrix for the rotation.

Example 1:
  Input:  matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
  Output: [[7, 4, 1], [8, 5, 2], [9, 6, 3]]

Example 2:
  Input:  matrix = [[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]]
  Output: [[15, 13, 2, 5], [14, 3, 4, 1], [12, 6, 8, 9], [16, 7, 10, 11]]

Approach (thought process)
--------------------------
1. A fresh matrix with `result[c][n - 1 - r] = matrix[r][c]` is correct but
   uses O(n²) extra space — the problem forbids that.
2. Observe that a 90° clockwise rotation equals: transpose, then reverse
   each row. Both steps are easy in place.
3. Transpose: swap `matrix[r][c]` with `matrix[c][r]` for all `c > r`
   (upper triangle). The diagonal stays put.
4. Reverse each row: for every row, swap left/right until the pointers meet.
5. Equivalent layer-cycle approach (four-way swaps on each ring) also works;
   transpose + reverse is shorter and just as O(1) extra space.

Complexity: O(n²) time, O(1) extra space.
"""

from __future__ import annotations

from typing import List


class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        """Rotate the n x n matrix 90 degrees clockwise in place."""
        n = len(matrix)
        # Transpose across the main diagonal.
        for r in range(n):
            for c in range(r + 1, n):
                matrix[r][c], matrix[c][r] = matrix[c][r], matrix[r][c]
        # Reverse each row.
        for row in matrix:
            row.reverse()


def _demo() -> None:
    sol = Solution()
    cases = [
        (
            [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            [[7, 4, 1], [8, 5, 2], [9, 6, 3]],
        ),
        (
            [
                [5, 1, 9, 11],
                [2, 4, 8, 10],
                [13, 3, 6, 7],
                [15, 14, 12, 16],
            ],
            [
                [15, 13, 2, 5],
                [14, 3, 4, 1],
                [12, 6, 8, 9],
                [16, 7, 10, 11],
            ],
        ),
        ([[1]], [[1]]),
        ([[1, 2], [3, 4]], [[3, 1], [4, 2]]),
    ]
    for matrix, expected in cases:
        working = [row[:] for row in matrix]
        sol.rotate(working)
        status = "OK" if working == expected else "FAIL"
        print(f"{status}: matrix={matrix} -> {working} (expected {expected})")
        assert working == expected, (
            f"48 rotate({matrix}) produced {working}, expected {expected}"
        )


if __name__ == "__main__":
    _demo()
