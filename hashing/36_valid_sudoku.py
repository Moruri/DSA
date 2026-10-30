"""
LeetCode 36: Valid Sudoku
Difficulty: Medium
Topic: Hashing / Sets

Problem
-------
Decide whether a partially filled 9x9 Sudoku board is valid. Only the
filled cells need to obey the rules: no digit repeats within a row, a
column, or any of the nine 3x3 boxes. The board does NOT need to be
solvable.

Approach (thought process)
--------------------------
1. Read the rules literally: every filled cell belongs to exactly three
   groups (its row, its column, its box), and each group must hold distinct
   digits. "Have I seen this before in this group?" is a hash-set question.
2. Keep 9 sets for rows, 9 for columns and 9 for boxes. Scan each cell once;
   if its digit is already in any of its three sets, the board is invalid.
   Otherwise add it to all three.
3. The only real trick is the box index. Rows 0-2 / 3-5 / 6-8 map to box
   row r // 3, and columns map the same way to c // 3. Flatten that pair to
   one index: box = (r // 3) * 3 + c // 3, which gives 0..8 left-to-right,
   top-to-bottom.
4. Empty cells (".") are skipped, since the rules only apply to filled ones.
5. We don't need to try solving the puzzle; validity here is purely about
   duplicates, so one pass is enough.

Complexity: O(81) = O(1) time and space for a fixed 9x9 board. For a
general n x n board it's O(n^2) time and O(n^2) space.
"""

from __future__ import annotations

from typing import List


class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        rows = [set() for _ in range(9)]
        cols = [set() for _ in range(9)]
        boxes = [set() for _ in range(9)]
        for r in range(9):
            for c in range(9):
                d = board[r][c]
                if d == ".":
                    continue
                b = (r // 3) * 3 + c // 3
                if d in rows[r] or d in cols[c] or d in boxes[b]:
                    return False
                rows[r].add(d)
                cols[c].add(d)
                boxes[b].add(d)
        return True


if __name__ == "__main__":
    valid = [
        ["5", "3", ".", ".", "7", ".", ".", ".", "."],
        ["6", ".", ".", "1", "9", "5", ".", ".", "."],
        [".", "9", "8", ".", ".", ".", ".", "6", "."],
        ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
        ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
        ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
        [".", "6", ".", ".", ".", ".", "2", "8", "."],
        [".", ".", ".", "4", "1", "9", ".", ".", "5"],
        [".", ".", ".", ".", "8", ".", ".", "7", "9"],
    ]
    box_clash = [row[:] for row in valid]
    box_clash[0][0] = "8"  # 8 repeats in column 0 and in the top-left box
    row_clash = [row[:] for row in valid]
    row_clash[0][8] = "5"  # 5 repeats in row 0
    only_box = [["."] * 9 for _ in range(9)]
    only_box[0][0] = "1"
    only_box[2][2] = "1"  # different row and column, same box

    s = Solution()
    for name, board, expected in [
        ("valid", valid, True),
        ("column/box clash", box_clash, False),
        ("row clash", row_clash, False),
        ("box-only clash", only_box, False),
        ("empty", [["."] * 9 for _ in range(9)], True),
    ]:
        got = s.isValidSudoku(board)
        assert got == expected, (name, got)
        print(f"{name:18} -> {got}")
    print("All tests passed.")
