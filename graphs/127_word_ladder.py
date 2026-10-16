"""
LeetCode 127: Word Ladder
Difficulty: Hard
Topic: Graphs / BFS on an Implicit Graph (wildcard buckets)

Problem
-------
Given beginWord, endWord and a wordList, return the number of words in the
shortest transformation sequence from beginWord to endWord, where each step
changes exactly one letter and every intermediate word (and endWord) must be
in wordList. Return 0 if no such sequence exists.

Example:
  beginWord = "hit", endWord = "cog",
  wordList = ["hot","dot","dog","lot","log","cog"]
  -> 5   ("hit" -> "hot" -> "dot" -> "dog" -> "cog")

Approach (thought process)
--------------------------
1. Picture every word as a node, with an edge between two words that differ
   in exactly one position. "Shortest sequence" on an unweighted graph is a
   textbook BFS: the first time we pop endWord, the level count is the answer.
2. The catch is building edges. Comparing every pair is O(N^2 * L). Instead,
   use wildcard buckets: for "hot" generate the patterns "*ot", "h*t", "ho*".
   Two words are neighbours exactly when they share a pattern, so a dict
   pattern -> [words] gives every neighbour in O(L) lookups.
3. BFS level by level from beginWord. For each word, for each of its L
   patterns, visit every unvisited word in that bucket. After a bucket has
   been expanded once, clear it: anything in it is now visited or queued, so
   re-scanning it later is wasted work. That keeps the total work bounded.
4. Bidirectional BFS (grow from both ends, always expanding the smaller
   frontier) is a common speed-up; the one-sided version below is already
   O(N * L^2) and is the clearest to reason about.

Why it works: BFS explores nodes in order of distance from the start, so the
first time endWord is reached it is via a shortest path. The wildcard
buckets are just an exact, cheap encoding of the "differs by one letter"
edges.

Complexity:
  - Time: O(N * L^2), N words of length L: L patterns per word, each pattern
    built in O(L).
  - Space: O(N * L^2) for the bucket map (N * L patterns of length L).
"""

from collections import defaultdict, deque
from typing import List


class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        words = set(wordList)
        if endWord not in words:
            return 0

        L = len(beginWord)
        buckets = defaultdict(list)
        for w in words:
            for i in range(L):
                buckets[w[:i] + "*" + w[i + 1:]].append(w)

        visited = {beginWord}
        queue = deque([beginWord])
        steps = 1
        while queue:
            for _ in range(len(queue)):
                word = queue.popleft()
                if word == endWord:
                    return steps
                for i in range(L):
                    pattern = word[:i] + "*" + word[i + 1:]
                    for nxt in buckets.get(pattern, ()):
                        if nxt not in visited:
                            visited.add(nxt)
                            queue.append(nxt)
                    buckets[pattern] = []  # fully expanded; never rescan
            steps += 1
        return 0


def _brute(begin: str, end: str, word_list: List[str]) -> int:
    """Plain BFS comparing letters pairwise, for cross-checking."""
    words = set(word_list)
    if end not in words:
        return 0
    seen = {begin}
    q = deque([(begin, 1)])
    while q:
        w, d = q.popleft()
        if w == end:
            return d
        for c in words:
            if c not in seen and sum(a != b for a, b in zip(w, c)) == 1:
                seen.add(c)
                q.append((c, d + 1))
    return 0


if __name__ == "__main__":
    s = Solution()
    assert s.ladderLength("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]) == 5
    assert s.ladderLength("hit", "cog", ["hot", "dot", "dog", "lot", "log"]) == 0
    assert s.ladderLength("a", "c", ["a", "b", "c"]) == 2
    assert s.ladderLength("hot", "dog", ["hot", "dog"]) == 0
    assert s.ladderLength("hot", "hot", ["hot"]) == 1

    import random

    for _ in range(2000):
        L = random.randint(1, 3)
        pool = ["".join(random.choice("abc") for _ in range(L)) for _ in range(random.randint(1, 12))]
        begin = "".join(random.choice("abc") for _ in range(L))
        end = random.choice(pool)
        assert s.ladderLength(begin, end, pool) == _brute(begin, end, pool), (begin, end, pool)
    print("All tests passed.")
