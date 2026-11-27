"""
LeetCode 909 -- Snakes and Ladders (Medium)
https://leetcode.com/problems/snakes-and-ladders/

Problem
-------
An n x n board is numbered 1..n^2 in boustrophedon order starting from the
bottom-left (rows alternate left->right and right->left). From square cur you
roll a die and move to any of cur+1..cur+6; if that square has a snake or
ladder (board value != -1) you must take it to its destination. Return the
fewest moves to reach n^2, or -1 if impossible.

Thought process
---------------
1. Every roll costs exactly one move, so "fewest moves" = shortest path in an
   unweighted graph whose nodes are squares 1..n^2. That is plain BFS.
2. The only fiddly part is mapping a square number to (row, col):
     q, r = divmod(square - 1, n)
     row  = n - 1 - q                (counting from the bottom)
     col  = r if q is even else n - 1 - r   (zig-zag)
3. From each square try the 6 dice targets, follow at most one snake/ladder
   (you don't chain them), and enqueue unseen destinations with dist + 1.
4. The first time we pop n^2 we have the answer.

Why it works: BFS explores squares in order of number of moves, so the first
visit of any square is via a minimum-move path.

Complexity
----------
Time:  O(n^2) -- each square is enqueued once and has 6 outgoing edges.
Space: O(n^2) for the visited set / queue.
"""

from collections import deque
from typing import List


class Solution:
    def snakesAndLadders(self, board: List[List[int]]) -> int:
        n = len(board)
        target = n * n

        def cell(square: int) -> int:
            q, r = divmod(square - 1, n)
            row = n - 1 - q
            col = r if q % 2 == 0 else n - 1 - r
            return board[row][col]

        seen = {1}
        queue = deque([(1, 0)])
        while queue:
            square, moves = queue.popleft()
            if square == target:
                return moves
            for nxt in range(square + 1, min(square + 6, target) + 1):
                jump = cell(nxt)
                dest = jump if jump != -1 else nxt
                if dest not in seen:
                    seen.add(dest)
                    queue.append((dest, moves + 1))
        return -1


if __name__ == "__main__":
    s = Solution()
    board = [
        [-1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1],
        [-1, 35, -1, -1, 13, -1],
        [-1, -1, -1, -1, -1, -1],
        [-1, 15, -1, -1, -1, -1],
    ]
    assert s.snakesAndLadders(board) == 4
    assert s.snakesAndLadders([[-1, -1], [-1, 3]]) == 1
    assert s.snakesAndLadders([[-1, -1, -1], [-1, 9, 8], [-1, 8, 9]]) == 1
    print("909 Snakes and Ladders: all tests passed")
