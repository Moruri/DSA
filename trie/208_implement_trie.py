"""
LeetCode 208: Implement Trie (Prefix Tree)
Link: https://leetcode.com/problems/implement-trie-prefix-tree/
Difficulty: Medium
Topic: Trie / Prefix Tree

Problem
-------
A trie (pronounced as "try") or prefix tree is a tree data structure used to
efficiently store and retrieve keys in a dataset of strings. Implement the
Trie class:

  - Trie() initializes the trie object
  - insert(word) inserts the string word into the trie
  - search(word) returns true if word is in the trie (i.e. was inserted before)
  - startsWith(prefix) returns true if there is a previously inserted string
    that has the prefix prefix

Example:
  Trie trie = Trie()
  trie.insert("apple")
  trie.search("apple")    # True
  trie.search("app")      # False
  trie.startsWith("app")  # True
  trie.insert("app")
  trie.search("app")      # True

Approach (thought process)
--------------------------
1. A hash set of whole words gives O(1) search but startsWith still needs a
   linear scan of every word. We want both operations fast by shared prefixes.
2. Store characters on edges of a tree. Each node holds a map child_char →
   child_node, plus a boolean marking whether a complete word ends here.
3. insert: walk (or create) one child per character; mark the final node as
   an end-of-word. Shared prefixes reuse existing nodes.
4. search: walk the characters; if any step is missing, the word is absent.
   At the end, require the end-of-word flag (so "app" is not found after only
   inserting "apple").
5. startsWith: same walk as search, but success only needs reaching the last
   prefix character — no end-of-word check.

Complexity: O(L) time per insert/search/startsWith for a string of length L.
Space is O(total characters inserted) across all words.
"""

from __future__ import annotations

from typing import Dict


class TrieNode:
    """One node in the trie: children keyed by character, plus end marker."""

    __slots__ = ("children", "is_end")

    def __init__(self) -> None:
        self.children: Dict[str, TrieNode] = {}
        self.is_end = False


class Trie:
    def __init__(self) -> None:
        """Initialize an empty trie rooted at a blank sentinel node."""
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """Insert word into the trie, creating nodes as needed."""
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, word: str) -> bool:
        """Return True iff word was previously inserted as a complete word."""
        node = self._walk(word)
        return node is not None and node.is_end

    def startsWith(self, prefix: str) -> bool:
        """Return True iff some inserted word begins with prefix."""
        return self._walk(prefix) is not None

    def _walk(self, s: str) -> TrieNode | None:
        """Follow s from the root; return the final node or None if missing."""
        node = self.root
        for ch in s:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node


def _demo() -> None:
    trie = Trie()
    trie.insert("apple")
    assert trie.search("apple") is True
    assert trie.search("app") is False
    assert trie.startsWith("app") is True
    trie.insert("app")
    assert trie.search("app") is True
    assert trie.startsWith("appl") is True
    assert trie.search("banana") is False
    assert trie.startsWith("ban") is False
    trie.insert("banana")
    assert trie.search("banana") is True
    assert trie.startsWith("ban") is True
    print("OK: Trie insert/search/startsWith demos passed")


if __name__ == "__main__":
    _demo()
