"""
LeetCode 200: Number of Islands
Link: https://leetcode.com/problems/number-of-islands/
Difficulty: Medium
Topic: Graphs / DFS

Problem
-------
Given an m x n 2D binary grid which represents a map of '1's (land) and
'0's (water), return the number of islands.

An island is surrounded by water and is formed by connecting adjacent lands
horizontally or vertically. You may assume all four edges of the grid are
surrounded by water.

Example 1:
  Input:  grid = [
    ["1","1","1","1","0"],
    ["1","1","0","1","0"],
    ["1","1","0","0","0"],
    ["0","0","0","0","0"]
  ]
  Output: 1

Example 2:
  Input:  grid = [
    ["1","1","0","0","0"],
    ["1","1","0","0","0"],
    ["0","0","1","0","0"],
    ["0","0","0","1","1"]
  ]
  Output: 3

Approach (thought process)
--------------------------
1. Model the grid as an implicit graph: each land cell is a vertex, and two
   land cells are joined by an edge when they are 4-directionally adjacent.
   An island is then exactly a connected component of that graph.
2. Counting connected components is a classic traversal job: scan every
   cell; each time we hit an unvisited '1', that is a brand-new island, so
   increment the count and flood-fill the whole component from there.
3. The flood fill is a DFS. From a land cell, visit its up/down/left/right
   neighbours that are in bounds and still '1'. Marking a cell as visited
   can be done by overwriting it with '0' (sinking the island) so no
   separate visited set is needed and each cell is processed once.
4. Use an explicit stack rather than recursion: a 300 x 300 all-land grid
   would recurse ~90,000 levels deep and blow Python's default recursion
   limit. The iterative version has identical semantics.
5. Every cell is pushed at most once (it is sunk when pushed), so the whole
   traversal is linear in the number of cells.

Complexity: O(m * n) time, O(m * n) extra space in the worst case for the
stack (one giant island).
"""

from __future__ import annotations

from typing import List


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        """Return the number of 4-directionally connected groups of '1' cells."""
        if not grid or not grid[0]:
            return 0

        rows, cols = len(grid), len(grid[0])
        count = 0

        def sink(sr: int, sc: int) -> None:
            """Iterative DFS: flip every land cell reachable from (sr, sc) to '0'."""
            stack = [(sr, sc)]
            grid[sr][sc] = "0"
            while stack:
                r, c = stack.pop()
                for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "1":
                        grid[nr][nc] = "0"  # mark visited on push, not on pop
                        stack.append((nr, nc))

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == "1":
                    count += 1
                    sink(r, c)

        return count


def _demo() -> None:
    sol = Solution()
    cases = [
        (
            [
                ["1", "1", "1", "1", "0"],
                ["1", "1", "0", "1", "0"],
                ["1", "1", "0", "0", "0"],
                ["0", "0", "0", "0", "0"],
            ],
            1,
        ),
        (
            [
                ["1", "1", "0", "0", "0"],
                ["1", "1", "0", "0", "0"],
                ["0", "0", "1", "0", "0"],
                ["0", "0", "0", "1", "1"],
            ],
            3,
        ),
        ([], 0),
        ([["0"]], 0),
        ([["1"]], 1),
        ([["0", "0", "0"], ["0", "0", "0"]], 0),
        # Diagonal cells are NOT connected: four corners + centre = five islands.
        ([["1", "0", "1"], ["0", "1", "0"], ["1", "0", "1"]], 5),
        # Ring-shaped island around a lake counts once.
        ([["1", "1", "1"], ["1", "0", "1"], ["1", "1", "1"]], 1),
        # Large all-land grid: exercises the iterative DFS (no recursion limit).
        ([["1"] * 300 for _ in range(300)], 1),
    ]
    for grid, expected in cases:
        # numIslands mutates the grid, so hand it a copy to keep the case printable.
        got = sol.numIslands([row[:] for row in grid])
        shape = f"{len(grid)}x{len(grid[0]) if grid else 0}"
        status = "OK" if got == expected else "FAIL"
        print(f"{status}: grid {shape} -> {got} (expected {expected})")
        assert got == expected, f"200 numIslands({shape} grid) returned {got}, expected {expected}"


if __name__ == "__main__":
    _demo()
