"""
LeetCode 74: Search a 2D Matrix
Difficulty: Medium
Topic: Binary Search (Virtual Flattening)

Problem
-------
You are given an m x n integer matrix where each row is sorted ascending and
the first integer of each row is greater than the last integer of the
previous row. Return True if `target` is in the matrix, else False.
Required: O(log(m * n)) time.

Example:
  matrix = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], target = 3 -> True
  same matrix, target = 13 -> False

Approach (thought process)
--------------------------
1. The two guarantees (rows sorted, each row starts above the previous row's
   end) mean that reading the matrix row by row gives ONE sorted list of
   m * n numbers. The grid is just a sorted array folded into rows.
2. So don't search a grid at all: binary search the imaginary flat array of
   indices 0 .. m*n - 1, and translate an index back to a cell only when we
   need to read it: row = idx // n, col = idx % n.
3. Standard binary search: compare the middle value to target, discard the
   half that can't contain it, stop when found or the range is empty.
4. (Alternative: binary search the first column to pick the row, then binary
   search inside that row. Same O(log m + log n) = O(log(mn)), just two loops.)

Why it works: divmod is a bijection between flat indices and cells that
preserves the row-major order, and row-major order is sorted by the
problem's guarantees, so binary search's invariant holds on the flat view.

Complexity:
  - Time: O(log(m * n)).
  - Space: O(1); nothing is actually flattened.
"""

from typing import List


class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        if not matrix or not matrix[0]:
            return False
        m, n = len(matrix), len(matrix[0])
        lo, hi = 0, m * n - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            value = matrix[mid // n][mid % n]
            if value == target:
                return True
            if value < target:
                lo = mid + 1
            else:
                hi = mid - 1
        return False


if __name__ == "__main__":
    s = Solution()
    grid = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
    assert s.searchMatrix(grid, 3) is True
    assert s.searchMatrix(grid, 13) is False
    assert s.searchMatrix(grid, 60) is True
    assert s.searchMatrix(grid, 1) is True
    assert s.searchMatrix(grid, 0) is False
    assert s.searchMatrix([[1]], 2) is False
    assert s.searchMatrix([[1, 3]], 3) is True
    print("All tests passed for 74. Search a 2D Matrix")
