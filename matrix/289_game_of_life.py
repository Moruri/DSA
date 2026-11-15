"""
LeetCode 289: Game of Life
Difficulty: Medium
Topic: Matrix / In-place State Encoding

Problem
-------
Given an m x n board of live (1) and dead (0) cells, compute the next
generation in place. Every cell looks at its 8 neighbours at the same
instant:
  * live with < 2 or > 3 live neighbours -> dies
  * live with 2 or 3 live neighbours     -> lives on
  * dead with exactly 3 live neighbours  -> becomes live

Approach (thought process)
--------------------------
1. The trap: if we overwrite a cell right away, its neighbours later in the
   scan count the *new* value instead of the old one. The easy fix is a copy
   of the board (O(mn) extra space), but the follow-up asks for in-place.
2. Each cell only needs two bits: "what I was" and "what I will be". Keep the
   old state in bit 0 and write the new state into bit 1:
       0b00 dead -> dead      0b01 live -> dead
       0b10 dead -> live      0b11 live -> live
3. Pass 1: for each cell, count neighbours using `board[r][c] & 1` (the old
   state, which is never touched). If the cell should be live next round,
   set bit 1 with `|= 2`.
4. Pass 2: shift every cell right by one (`>>= 1`) so the new state becomes
   the only state.
5. Why it works: pass 1 never changes bit 0, so every neighbour count sees
   the original generation. Pass 2 then swaps all cells at once, just like
   the "same instant" rule asks.

Complexity
----------
Time:  O(m * n * 8) = O(m * n).
Space: O(1) extra, since the extra bit lives inside the board itself.
"""

from typing import List


class Solution:
    def gameOfLife(self, board: List[List[int]]) -> None:
        rows, cols = len(board), len(board[0])
        dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                (0, 1), (1, -1), (1, 0), (1, 1)]

        for r in range(rows):
            for c in range(cols):
                live = 0
                for dr, dc in dirs:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        live += board[nr][nc] & 1
                alive = board[r][c] & 1
                if (alive and live in (2, 3)) or (not alive and live == 3):
                    board[r][c] |= 2  # mark "alive next generation"

        for r in range(rows):
            for c in range(cols):
                board[r][c] >>= 1


if __name__ == "__main__":
    s = Solution()

    b1 = [[0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 0, 0]]
    s.gameOfLife(b1)
    assert b1 == [[0, 0, 0], [1, 0, 1], [0, 1, 1], [0, 1, 0]], b1

    b2 = [[1, 1], [1, 0]]
    s.gameOfLife(b2)
    assert b2 == [[1, 1], [1, 1]], b2

    # Blinker oscillates with period 2.
    blinker = [[0, 0, 0], [1, 1, 1], [0, 0, 0]]
    s.gameOfLife(blinker)
    assert blinker == [[0, 1, 0], [0, 1, 0], [0, 1, 0]], blinker
    s.gameOfLife(blinker)
    assert blinker == [[0, 0, 0], [1, 1, 1], [0, 0, 0]], blinker

    print("289 Game of Life: all tests passed")
