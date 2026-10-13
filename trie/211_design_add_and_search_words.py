"""
LeetCode 211: Design Add and Search Words Data Structure
Difficulty: Medium
Topic: Trie / DFS with Wildcards

Problem
-------
Design a WordDictionary that supports:
  - addWord(word): store a word of lowercase letters.
  - search(word): return True if any stored word matches. The query may
    contain '.', which matches any single letter.

Example:
  addWord("bad"); addWord("dad"); addWord("mad")
  search("pad") -> False
  search("bad") -> True
  search(".ad") -> True
  search("b..") -> True

Approach (thought process)
--------------------------
1. A plain set handles exact lookups in O(L), but a '.' query would force a
   scan over every stored word. We want to share work between words that
   share a prefix, which is exactly what a trie does.
2. Trie: each node maps a letter to a child node and has an is_end flag.
   addWord walks down, creating children as needed, and marks the last node.
3. search without wildcards is the same walk: follow one child per letter,
   fail if it's missing, and at the end require is_end (so "ba" doesn't
   match just because "bad" exists).
4. A '.' means "any letter here", so at that position we branch: try every
   child and succeed if any branch matches the rest of the pattern. That is
   a DFS over (node, index in pattern).
5. Short-circuit with any(...) so we stop exploring once one branch succeeds.

Why it works: every stored word is exactly one root-to-node path ending at
an is_end node. The DFS follows the only possible edge for a fixed letter and
tries all edges for '.', so it visits exactly the paths whose letters agree
with the pattern; it returns True iff one of those ends at a word.

Complexity:
  - addWord: O(L) time, O(L) new nodes at most.
  - search with no dots: O(L).
  - search with dots: worst case O(26^d * L) for d dots, bounded by the size
    of the trie (each node visited at most once per pattern position).
  - Space: O(total characters added).
"""

from typing import Dict


class TrieNode:
    __slots__ = ("children", "is_end")

    def __init__(self) -> None:
        self.children: Dict[str, "TrieNode"] = {}
        self.is_end = False


class WordDictionary:
    def __init__(self) -> None:
        self.root = TrieNode()

    def addWord(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.is_end = True

    def search(self, word: str) -> bool:
        def dfs(node: TrieNode, i: int) -> bool:
            if i == len(word):
                return node.is_end
            ch = word[i]
            if ch == ".":
                return any(dfs(child, i + 1) for child in node.children.values())
            child = node.children.get(ch)
            return child is not None and dfs(child, i + 1)

        return dfs(self.root, 0)


if __name__ == "__main__":
    wd = WordDictionary()
    for w in ["bad", "dad", "mad"]:
        wd.addWord(w)
    assert wd.search("pad") is False
    assert wd.search("bad") is True
    assert wd.search(".ad") is True
    assert wd.search("b..") is True
    assert wd.search("ba") is False      # prefix only, not a word
    assert wd.search("...") is True
    assert wd.search("....") is False
    assert wd.search(".") is False

    wd.addWord("a")
    wd.addWord("ab")
    assert wd.search(".") is True
    assert wd.search("a.") is True
    assert wd.search(".b") is True
    assert wd.search("..") is True
    assert wd.search("b.d") is True
    assert wd.search("m.x") is False
    print("All tests passed.")
