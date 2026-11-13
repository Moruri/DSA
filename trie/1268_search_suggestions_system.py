"""
LeetCode 1268: Search Suggestions System
Difficulty: Medium
Topic: Trie / Prefix Search

Problem
-------
Given a list of products and a searchWord, after each character typed return
up to three products (lexicographically smallest) that start with the prefix
typed so far.

Approach (thought process)
--------------------------
1. Every query is "words with this prefix" -> that is exactly what a trie is
   built for: walking one edge per typed char lands us on the node whose
   subtree holds every matching product.
2. We don't want to DFS the subtree on every keystroke. Instead, insert the
   products in *sorted* order and let each node keep a short list of the
   first three words that passed through it. Because insertion is sorted,
   those first three are automatically the three lexicographically smallest.
3. Typing: walk the trie char by char and read the node's cached list. Once a
   char has no child, every longer prefix also has no matches, so the rest of
   the answers are empty lists.
4. Why it works: a word passes through node(prefix) iff it starts with prefix,
   and sorted insertion guarantees the cache holds the smallest three.

(Alternative: sort + binary search with bisect_left for each prefix and peek
at the next 3 entries — same complexity class, no extra structure.)

Complexity
----------
Let L = total characters across products, m = len(searchWord).
Time:  O(n log n * w) to sort + O(L) to build + O(m) to answer.
Space: O(L) trie nodes, each caching at most 3 references.
"""

from typing import List


class TrieNode:
    __slots__ = ("children", "suggestions")

    def __init__(self) -> None:
        self.children: dict = {}
        self.suggestions: List[str] = []


class Solution:
    def suggestedProducts(self, products: List[str], searchWord: str) -> List[List[str]]:
        root = TrieNode()
        for word in sorted(products):
            node = root
            for ch in word:
                node = node.children.setdefault(ch, TrieNode())
                if len(node.suggestions) < 3:
                    node.suggestions.append(word)

        result: List[List[str]] = []
        node = root
        for ch in searchWord:
            node = node.children.get(ch) if node else None
            result.append(list(node.suggestions) if node else [])
        return result


if __name__ == "__main__":
    sol = Solution()
    assert sol.suggestedProducts(
        ["mobile", "mouse", "moneypot", "monitor", "mousepad"], "mouse"
    ) == [
        ["mobile", "moneypot", "monitor"],
        ["mobile", "moneypot", "monitor"],
        ["mouse", "mousepad"],
        ["mouse", "mousepad"],
        ["mouse", "mousepad"],
    ]
    assert sol.suggestedProducts(["havana"], "havana") == [["havana"]] * 6
    assert sol.suggestedProducts(["havana"], "tatiana") == [[]] * 7
    assert sol.suggestedProducts(["bags", "baggage", "banner", "box", "cloths"], "bags") == [
        ["baggage", "bags", "banner"],
        ["baggage", "bags", "banner"],
        ["baggage", "bags"],
        ["bags"],
    ]
    print(sol.suggestedProducts(["mobile", "mouse", "moneypot", "monitor", "mousepad"], "mouse"))
    print("All tests passed.")
