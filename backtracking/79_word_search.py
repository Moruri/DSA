"""
LeetCode 79: Word Search
Difficulty: Medium
Topic: Backtracking / DFS on Grid

Problem
-------
Given an m x n grid of characters board and a string word, return true if
word exists in the grid.

The word can be constructed from letters of sequentially adjacent cells,
where adjacent cells are horizontally or vertically neighboring. The same
letter cell may not be used more than once.

Example 1:
  Input:  board = [["A","B","C","E"],
                   ["S","F","C","S"],
                   ["A","D","E","E"]],
          word = "ABCCED"
  Output: true

Example 2:
  Input:  board = [["A","B","C","E"],
                   ["S","F","C","S"],
                   ["A","D","E","E"]],
          word = "SEE"
  Output: true

Example 3:
  Input:  board = [["A","B","C","E"],
                   ["S","F","C","S"],
                   ["A","D","E","E"]],
          word = "ABCB"
  Output: false

Approach (thought process)
--------------------------
1. Every cell is a potential start. If board[r][c] matches word[0], launch
   a DFS that tries to match the rest of the word from that cell.
2. From the current cell, recurse into the four orthogonal neighbors that
   still match the next character. Bounds checks and a letter mismatch
   prune a branch immediately.
3. Mark the current cell as visited (overwrite with '#') before exploring
   neighbors so the path cannot reuse it; restore the original letter on
   the way back so sibling branches see a clean board. That mark/unmark
   pair is the classic backtracking undo.
4. When the matched index reaches len(word), the full word has been found
   — return True up the call stack. If no start cell succeeds, return False.

Complexity: O(m · n · 4^L) time in the worst case (m·n starts, branching
factor ≤ 4, L = word length), O(L) recursion depth / extra space.
"""

from __future__ import annotations

from typing import List


class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        """Return True if word can be formed by adjacent cells (no reuse)."""
        if not board or not board[0] or not word:
            return False

        rows, cols = len(board), len(board[0])

        def dfs(r: int, c: int, idx: int) -> bool:
            if idx == len(word):
                return True
            if (
                r < 0
                or r >= rows
                or c < 0
                or c >= cols
                or board[r][c] != word[idx]
            ):
                return False

            saved = board[r][c]
            board[r][c] = "#"
            found = (
                dfs(r + 1, c, idx + 1)
                or dfs(r - 1, c, idx + 1)
                or dfs(r, c + 1, idx + 1)
                or dfs(r, c - 1, idx + 1)
            )
            board[r][c] = saved
            return found

        for i in range(rows):
            for j in range(cols):
                if board[i][j] == word[0] and dfs(i, j, 0):
                    return True
        return False


def _demo() -> None:
    sol = Solution()
    board_a = [
        ["A", "B", "C", "E"],
        ["S", "F", "C", "S"],
        ["A", "D", "E", "E"],
    ]
    cases = [
        ([row[:] for row in board_a], "ABCCED", True),
        ([row[:] for row in board_a], "SEE", True),
        ([row[:] for row in board_a], "ABCB", False),
        ([["A"]], "A", True),
        ([["A"]], "B", False),
        ([["A", "B"], ["C", "D"]], "ACDB", True),
        ([["A", "B"], ["C", "D"]], "ABDC", True),
        ([["A", "B"], ["C", "D"]], "ABCD", False),
    ]
    for board, word, expected in cases:
        # Fresh board copy so mutations do not leak across cases
        grid = [row[:] for row in board]
        got = sol.exist(grid, word)
        status = "OK" if got == expected else "FAIL"
        print(f"{status}: exist(board, {word!r}) -> {got} (expected {expected})")
        assert got == expected, (
            f"79 exist(..., {word!r}) returned {got}, expected {expected}"
        )
        # Board must be fully restored after search
        assert grid == board, "board was not restored after DFS"


if __name__ == "__main__":
    _demo()
