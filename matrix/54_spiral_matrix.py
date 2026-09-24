"""
LeetCode 54: Spiral Matrix
Link: https://leetcode.com/problems/spiral-matrix/
Difficulty: Medium
Topic: Matrix / Simulation

Problem
-------
Given an m x n matrix, return all elements of the matrix in spiral order
(clockwise, starting from the top-left cell).

Example 1:
  Input:  matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
  Output: [1, 2, 3, 6, 9, 8, 7, 4, 5]

Example 2:
  Input:  matrix = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
  Output: [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]

Approach (thought process)
--------------------------
1. Visiting cells with an explicit direction array and a visited set works,
   but layer-by-layer peeling is clearer and uses O(1) extra space beyond
   the output.
2. Maintain four shrinking bounds: top, bottom, left, right. While the
   bounds still enclose a non-empty rectangle, walk the outer ring:
   left→right on the top row, top→bottom on the right column, right→left
   on the bottom row, then bottom→top on the left column.
3. After finishing each side, shrink the corresponding bound (top += 1,
   right -= 1, bottom -= 1, left += 1). Guard the bottom and left legs so
   a single remaining row or column is not traversed twice.
4. Empty input yields []; a 1×n or m×1 matrix is just that row/column.
   Each cell is appended exactly once.

Complexity: O(m · n) time, O(1) extra space beyond the output.
"""

from __future__ import annotations

from typing import List


class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        """Return matrix elements in clockwise spiral order."""
        if not matrix or not matrix[0]:
            return []

        top, bottom = 0, len(matrix) - 1
        left, right = 0, len(matrix[0]) - 1
        result: List[int] = []

        while top <= bottom and left <= right:
            for col in range(left, right + 1):
                result.append(matrix[top][col])
            top += 1

            for row in range(top, bottom + 1):
                result.append(matrix[row][right])
            right -= 1

            if top <= bottom:
                for col in range(right, left - 1, -1):
                    result.append(matrix[bottom][col])
                bottom -= 1

            if left <= right:
                for row in range(bottom, top - 1, -1):
                    result.append(matrix[row][left])
                left += 1

        return result


def _demo() -> None:
    sol = Solution()
    cases = [
        ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [1, 2, 3, 6, 9, 8, 7, 4, 5]),
        (
            [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]],
            [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7],
        ),
        ([[1]], [1]),
        ([[1, 2], [3, 4]], [1, 2, 4, 3]),
        ([[1, 2, 3]], [1, 2, 3]),
        ([[1], [2], [3]], [1, 2, 3]),
        ([], []),
        ([[]], []),
    ]
    for matrix, expected in cases:
        got = sol.spiralOrder(matrix)
        status = "OK" if got == expected else "FAIL"
        print(f"{status}: matrix={matrix} -> {got} (expected {expected})")
        assert got == expected, (
            f"54 spiralOrder({matrix}) returned {got}, expected {expected}"
        )


if __name__ == "__main__":
    _demo()
