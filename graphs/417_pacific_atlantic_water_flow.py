"""
LeetCode 417: Pacific Atlantic Water Flow
Difficulty: Medium
Topic: Graphs / Reverse Multi-source DFS

Problem
-------
An m x n grid `heights` sits between two oceans: the Pacific touches the top
and left edges, the Atlantic touches the bottom and right edges. Rain water
flows from a cell to a 4-directional neighbour whose height is less than or
equal to the current cell's. Return every coordinate [r, c] from which water
can reach BOTH oceans.

Example:
  Input:  heights = [[1,2,2,3,5],
                     [3,2,3,4,4],
                     [2,4,5,3,1],
                     [6,7,1,4,5],
                     [5,1,1,2,4]]
  Output: [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]

Approach (thought process)
--------------------------
1. The obvious idea is to start a search from every cell and see which
   oceans it reaches. That repeats the same work over and over:
   O((m·n)^2) in the worst case.
2. Flip the direction. Instead of asking "where can water from this cell
   go?", ask "which cells can drain INTO this ocean?". Start at the ocean's
   border cells and walk *uphill*: move from a cell to a neighbour whose
   height is >= the current one (the reverse of the downhill rule).
3. Run that search once from all Pacific border cells together (a
   multi-source DFS) and once from all Atlantic border cells. Each search
   marks the set of cells that can reach that ocean.
4. The answer is the intersection of the two sets.

Why it works: water can flow from A down to the ocean along some path
exactly when the ocean can "climb" back up that same path to A, so the
reverse search marks precisely the cells that drain into each ocean.

Complexity: O(m·n) time (each cell visited at most once per ocean),
O(m·n) space for the two visited sets and the stack.
"""

from __future__ import annotations

from typing import List, Set, Tuple

Cell = Tuple[int, int]


class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        """Return cells that can drain into both the Pacific and the Atlantic."""
        if not heights or not heights[0]:
            return []
        rows, cols = len(heights), len(heights[0])

        def climb(starts: List[Cell]) -> Set[Cell]:
            seen: Set[Cell] = set(starts)
            stack = list(starts)  # iterative DFS avoids recursion limits
            while stack:
                r, c = stack.pop()
                for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                    if (
                        0 <= nr < rows
                        and 0 <= nc < cols
                        and (nr, nc) not in seen
                        and heights[nr][nc] >= heights[r][c]
                    ):
                        seen.add((nr, nc))
                        stack.append((nr, nc))
            return seen

        pacific_border = [(0, c) for c in range(cols)] + [(r, 0) for r in range(rows)]
        atlantic_border = [(rows - 1, c) for c in range(cols)] + [(r, cols - 1) for r in range(rows)]

        both = climb(pacific_border) & climb(atlantic_border)
        return [list(cell) for cell in sorted(both)]


def _demo() -> None:
    sol = Solution()
    cases = [
        (
            [[1, 2, 2, 3, 5], [3, 2, 3, 4, 4], [2, 4, 5, 3, 1], [6, 7, 1, 4, 5], [5, 1, 1, 2, 4]],
            [[0, 4], [1, 3], [1, 4], [2, 2], [3, 0], [3, 1], [4, 0]],
        ),
        ([[1]], [[0, 0]]),
        ([[2, 1], [1, 2]], [[0, 0], [0, 1], [1, 0], [1, 1]]),
        ([[1, 2, 3], [8, 9, 4], [7, 6, 5]], [[0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]),
    ]
    for grid, expected in cases:
        got = sol.pacificAtlantic(grid)
        status = "OK" if got == expected else "FAIL"
        print(f"{status}: pacificAtlantic({grid}) -> {got}")
        assert got == expected, f"417 pacificAtlantic({grid}) returned {got}, expected {expected}"


if __name__ == "__main__":
    _demo()
