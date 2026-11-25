"""
LeetCode 648: Replace Words
Difficulty: Medium
Topic: Trie / Shortest Prefix Match

Problem
-------
Given a dictionary of roots and a sentence, replace every word in the
sentence with the SHORTEST root that is a prefix of it (leave the word as-is
if no root matches). Return the rebuilt sentence.

Approach (thought process)
--------------------------
1. Naive: for every word, test every root with startswith -> O(W * R * L).
   The repeated work is comparing the same leading letters again and again.
2. A trie shares prefixes: insert every root once, marking the node where a
   root ends.
3. For each word, walk the trie letter by letter. The FIRST end-marker we hit
   is the shortest root, so stop right there and emit word[:i+1].
4. If a letter has no child, no root can match further -> keep the word.

Why it works: the path from the trie root spelling word[:k] exists iff some
root starts with word[:k]; an end-marker there means word[:k] IS a root.
Scanning k upward and stopping at the first marker yields the shortest one.

Complexity
----------
Time:  O(sum of root lengths + sum of word lengths) -- each letter is
       touched at most once per insert / lookup.
Space: O(sum of root lengths) for the trie.
"""

from typing import List

END = "#"


class Solution:
    def replaceWords(self, dictionary: List[str], sentence: str) -> str:
        trie: dict = {}
        for root in dictionary:
            node = trie
            for ch in root:
                node = node.setdefault(ch, {})
            node[END] = True

        def shortest_root(word: str) -> str:
            node = trie
            for i, ch in enumerate(word):
                if ch not in node:
                    return word
                node = node[ch]
                if END in node:
                    return word[: i + 1]
            return word

        return " ".join(shortest_root(w) for w in sentence.split())


def brute(dictionary: List[str], sentence: str) -> str:
    out = []
    for w in sentence.split():
        matches = [r for r in dictionary if w.startswith(r)]
        out.append(min(matches, key=len) if matches else w)
    return " ".join(out)


if __name__ == "__main__":
    s = Solution()
    cases = [
        (["cat", "bat", "rat"], "the cattle was rattled by the battery",
         "the cat was rat by the bat"),
        (["a", "b", "c"], "aadsfasf absbs bbab cadsfafs", "a a b c"),
        (["catt", "cat", "bat", "rat"], "the cattle was rattled by the battery",
         "the cat was rat by the bat"),
        (["xyz"], "hello world", "hello world"),
    ]
    for d, sent, want in cases:
        got = s.replaceWords(d, sent)
        assert got == want, (d, sent, got, want)
        print(f"{sent!r} -> {got!r}")

    import random
    random.seed(648)
    rw = lambda lo, hi: "".join(random.choice("abc") for _ in range(random.randint(lo, hi)))
    for _ in range(300):
        d = [rw(1, 3) for _ in range(random.randint(1, 5))]
        sent = " ".join(rw(1, 6) for _ in range(random.randint(1, 6)))
        assert s.replaceWords(d, sent) == brute(d, sent), (d, sent)
    print("random cross-check vs brute force OK")
    print("All tests passed.")
