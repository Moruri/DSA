"""
LeetCode 130: Surrounded Regions
Difficulty: Medium
Topic: Graphs / Boundary DFS (flood fill from the edges)

Problem
-------
Given an m x n board of 'X' and 'O', capture every region of 'O' that is
completely surrounded by 'X' by flipping it to 'X'. A region is a group of
'O' cells connected up/down/left/right. Any region that touches the border
cannot be surrounded, so it survives. Modify the board in place.

Example:
  X X X X        X X X X
  X O O X   ->   X X X X
  X X O X        X X X X
  X O X X        X O X X     (the bottom O touches the border, so it stays)

Approach (thought process)
--------------------------
1. The direct question, "is this region surrounded?", is awkward: you would
   have to explore each region fully and then decide. Flip it around and ask
   the easier question: which O's can escape to the border?
2. An O survives exactly when it is connected to some border O. So start a
   flood fill from every O on the edge of the board and mark everything it
   reaches as safe (temporarily write 'S'). This is the same reverse-search
   trick as Pacific Atlantic Water Flow: search from the goal inward.
3. After that, any O still left could not reach the border, so it is
   captured: flip it to 'X'. Turn every 'S' back into 'O'.
4. Use an explicit stack instead of recursion so a 200 x 200 board full of
   O's doesn't blow Python's recursion limit.

Complexity: O(m * n) time, since each cell is pushed at most a few times and
processed once; O(m * n) worst-case extra space for the stack.
"""

from __future__ import annotations

from typing import List


class Solution:
    def solve(self, board: List[List[str]]) -> None:
        if not board or not board[0]:
            return
        rows, cols = len(board), len(board[0])

        stack = []
        for r in range(rows):
            stack.append((r, 0))
            stack.append((r, cols - 1))
        for c in range(cols):
            stack.append((0, c))
            stack.append((rows - 1, c))

        # Flood fill from the border: every reachable O is safe.
        while stack:
            r, c = stack.pop()
            if 0 <= r < rows and 0 <= c < cols and board[r][c] == "O":
                board[r][c] = "S"
                stack.extend(((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)))

        # Capture the rest, restore the safe cells.
        for r in range(rows):
            for c in range(cols):
                if board[r][c] == "O":
                    board[r][c] = "X"
                elif board[r][c] == "S":
                    board[r][c] = "O"


def brute(board: List[List[str]]) -> List[List[str]]:
    """Explore each region and flip it if it never touches the border."""
    rows, cols = len(board), len(board[0])
    out = [row[:] for row in board]
    seen = set()
    for sr in range(rows):
        for sc in range(cols):
            if board[sr][sc] != "O" or (sr, sc) in seen:
                continue
            region, todo, edge = [], [(sr, sc)], False
            seen.add((sr, sc))
            while todo:
                r, c = todo.pop()
                region.append((r, c))
                if r in (0, rows - 1) or c in (0, cols - 1):
                    edge = True
                for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                    if (0 <= nr < rows and 0 <= nc < cols
                            and board[nr][nc] == "O" and (nr, nc) not in seen):
                        seen.add((nr, nc))
                        todo.append((nr, nc))
            if not edge:
                for r, c in region:
                    out[r][c] = "X"
    return out


if __name__ == "__main__":
    s = Solution()
    board = [list("XXXX"), list("XOOX"), list("XXOX"), list("XOXX")]
    s.solve(board)
    assert board == [list("XXXX"), list("XXXX"), list("XXXX"), list("XOXX")]

    one = [["X"]]
    s.solve(one)
    assert one == [["X"]]

    import random

    for _ in range(400):
        m, n = random.randint(1, 8), random.randint(1, 8)
        b = [[random.choice("XO") for _ in range(n)] for _ in range(m)]
        expected = brute(b)
        s.solve(b)
        assert b == expected
    big = [["O"] * 200 for _ in range(200)]
    s.solve(big)
    assert all(cell == "O" for row in big for cell in row)
    print("All tests passed.")
