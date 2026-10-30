"""
LeetCode 212: Word Search II
Difficulty: Hard
Topic: Trie / Backtracking on a grid

Problem
-------
Given an m x n board of letters and a list of words, return every word that
can be traced on the board by moving between horizontally or vertically
adjacent cells, using each cell at most once per word.

Example:
  board = [["o","a","a","n"],
           ["e","t","a","e"],
           ["i","h","k","r"],
           ["i","f","l","v"]]
  words = ["oath","pea","eat","rain"]  ->  ["eat","oath"]

Approach (thought process)
--------------------------
1. The naive plan runs Word Search I (problem 79) once per word. With
   thousands of words that repeats the same grid walks over and over:
   "oath" and "oat" share the walk o-a-t, yet we'd trace it twice.
2. Flip it around: walk the grid once, and at every step ask "is the path
   I've built so far the prefix of ANY word?" A trie answers that in O(1)
   per letter, because moving one cell deeper = moving one trie node deeper.
3. So: insert every word into a trie, storing the full word at its final
   node. DFS from every cell, carrying the current trie node. If the next
   letter isn't a child of the node, prune immediately; no word starts that
   way, so there's no point exploring further.
4. When we land on a node that holds a word, record it and clear the word
   from the node so the same word isn't reported twice.
5. Mark the cell visited by overwriting it with "#" during the DFS and
   restore it on the way back (classic backtracking, no extra visited set).
6. Pruning trick: after exploring a child, if that child has no word and no
   children left, delete it from its parent. Found words shrink the trie, so
   later searches stop earlier. This is what keeps big inputs fast.

Complexity: building the trie is O(total letters in words). The search is
O(m * n * 4 * 3^(L-1)) in the worst case, where L is the longest word
(4 directions on the first step, at most 3 afterwards because we never step
back). Space is O(total letters) for the trie plus O(L) recursion depth.
"""

from __future__ import annotations

from typing import List


class TrieNode:
    __slots__ = ("children", "word")

    def __init__(self) -> None:
        self.children: dict[str, TrieNode] = {}
        self.word: str | None = None


class Solution:
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        root = TrieNode()
        for w in words:
            node = root
            for ch in w:
                node = node.children.setdefault(ch, TrieNode())
            node.word = w

        rows, cols = len(board), len(board[0])
        found: List[str] = []

        def dfs(r: int, c: int, parent: TrieNode) -> None:
            ch = board[r][c]
            node = parent.children.get(ch)
            if node is None:
                return
            if node.word is not None:
                found.append(node.word)
                node.word = None  # report each word once

            board[r][c] = "#"
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != "#":
                    dfs(nr, nc, node)
            board[r][c] = ch

            # Prune exhausted branches so later searches end sooner.
            if not node.children and node.word is None:
                del parent.children[ch]

        for r in range(rows):
            for c in range(cols):
                dfs(r, c, root)
        return found


if __name__ == "__main__":
    s = Solution()
    cases = [
        (
            [["o", "a", "a", "n"],
             ["e", "t", "a", "e"],
             ["i", "h", "k", "r"],
             ["i", "f", "l", "v"]],
            ["oath", "pea", "eat", "rain"],
            {"eat", "oath"},
        ),
        ([["a", "b"], ["c", "d"]], ["abcb"], set()),
        ([["a"]], ["a", "a"], {"a"}),
        ([["a", "b"], ["c", "d"]], ["abdc", "acdb", "ab", "ba", "dd"], {"abdc", "acdb", "ab", "ba"}),
    ]
    for board, words, expected in cases:
        got = s.findWords([row[:] for row in board], words)
        assert set(got) == expected and len(got) == len(set(got)), (words, got)
        print(f"{words} -> {sorted(got)}")
    print("All tests passed.")
