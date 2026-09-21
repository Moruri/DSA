"""
LeetCode 994: Rotting Oranges
Link: https://leetcode.com/problems/rotting-oranges/
Difficulty: Medium
Topic: Graphs / Multi-source BFS

Problem
-------
You are given an m x n grid where each cell can have one of three values:
  0 — empty cell
  1 — fresh orange
  2 — rotten orange

Every minute, any fresh orange that is 4-directionally adjacent to a rotten
orange becomes rotten.

Return the minimum number of minutes that must elapse until no cell has a
fresh orange. If this is impossible, return -1.

Example 1:
  Input:  grid = [[2,1,1],[1,1,0],[0,1,1]]
  Output: 4

Example 2:
  Input:  grid = [[2,1,1],[0,1,1],[1,0,1]]
  Output: -1
  Explanation: The orange in the bottom-left never gets touched.

Example 3:
  Input:  grid = [[0,2]]
  Output: 0
  Explanation: Already no fresh oranges.

Approach (thought process)
--------------------------
1. Fresh oranges only rot when a rotten neighbour "reaches" them, and every
   rotten orange spreads at the same time each minute. That is simultaneous
   multi-source expansion on a grid graph — classic multi-source BFS.
2. Seed a queue with every initially rotten cell and count how many fresh
   oranges exist. If the fresh count is already 0, answer is 0.
3. BFS level by level: each level is one minute. For every rotten cell in
   the current frontier, infect any in-bounds fresh neighbour (flip to 2,
   enqueue it, decrement fresh). After draining the level, minutes += 1.
4. When the queue empties, if any fresh oranges remain they were unreachable
   (isolated by empties or walls of already-rotten cells with no path), so
   return -1; otherwise return the minutes counted.
5. Each cell is enqueued at most once, so the scan is linear in the grid.

Complexity: O(m * n) time, O(m * n) space for the queue in the worst case.
"""

from __future__ import annotations

from collections import deque
from typing import List


class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        """Return minutes until all fresh oranges rot, or -1 if impossible."""
        if not grid or not grid[0]:
            return 0

        rows, cols = len(grid), len(grid[0])
        queue: deque[tuple[int, int]] = deque()
        fresh = 0

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 2:
                    queue.append((r, c))
                elif grid[r][c] == 1:
                    fresh += 1

        if fresh == 0:
            return 0

        minutes = 0
        directions = ((-1, 0), (1, 0), (0, -1), (0, 1))

        while queue and fresh > 0:
            for _ in range(len(queue)):
                r, c = queue.popleft()
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                        grid[nr][nc] = 2
                        fresh -= 1
                        queue.append((nr, nc))
            minutes += 1

        return minutes if fresh == 0 else -1


def _demo() -> None:
    sol = Solution()
    cases = [
        ([[2, 1, 1], [1, 1, 0], [0, 1, 1]], 4),
        ([[2, 1, 1], [0, 1, 1], [1, 0, 1]], -1),
        ([[0, 2]], 0),
        ([[0]], 0),
        ([[1]], -1),
        ([[2]], 0),
        ([[1, 2]], 1),
        ([[2, 2, 2], [2, 1, 2], [2, 2, 2]], 1),
        # Already all rotten / empty — no minutes needed.
        ([[2, 0, 2], [0, 0, 0], [2, 0, 2]], 0),
    ]
    for grid, expected in cases:
        # orangesRotting mutates the grid; copy so cases stay printable.
        got = sol.orangesRotting([row[:] for row in grid])
        status = "OK" if got == expected else "FAIL"
        print(f"{status}: grid={grid} -> {got} (expected {expected})")
        assert got == expected, (
            f"994 orangesRotting({grid}) returned {got}, expected {expected}"
        )


if __name__ == "__main__":
    _demo()
