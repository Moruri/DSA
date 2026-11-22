"""
LeetCode 1239: Maximum Length of a Concatenated String with Unique Characters
Difficulty: Medium
Topic: Backtracking / Bitmask

Problem
-------
Given a list of lowercase strings arr, choose a subsequence of them whose
concatenation has no repeated letter. Return the maximum possible length.

Approach (thought process)
--------------------------
1. Only "which letters are used" matters, never their order. 26 letters fit
   in one integer, so each word becomes a bitmask (bit i set = letter i used).
2. A word that repeats a letter inside itself ("aa") can never be picked:
   drop it up front. That's the case where the mask has fewer bits than the
   word has characters.
3. Two words can sit together exactly when their masks share no bit:
   a & b == 0. Joining them is a | b, and the length is the popcount.
4. Backtrack over the words in order: at index i, either skip word i or, if
   it doesn't clash with the current mask, take it. Track the best popcount.
   Each word is included or excluded, so it's the subsets template (78)
   with a pruning rule.
5. An equivalent iterative version keeps a list of every reachable mask and
   extends each one with each new word. Same idea, no recursion.

Why it works: every valid choice is a subset of the words with pairwise
disjoint masks, and the search explores exactly those subsets (clashing
branches are cut the moment they clash, since adding more words can't fix a
repeat).

Complexity
----------
Time:  O(2^n) in the worst case (n <= 16 on LeetCode), each step O(1) with
       bit operations. In practice, pruning makes it much smaller.
Space: O(n) recursion depth.
"""

from typing import List


class Solution:
    def maxLength(self, arr: List[str]) -> int:
        masks = []
        for word in arr:
            m = 0
            for ch in word:
                m |= 1 << (ord(ch) - 97)
            if bin(m).count("1") == len(word):  # no repeat inside the word
                masks.append(m)

        best = 0

        def dfs(i: int, used: int) -> None:
            nonlocal best
            best = max(best, bin(used).count("1"))
            for j in range(i, len(masks)):
                if used & masks[j] == 0:
                    dfs(j + 1, used | masks[j])

        dfs(0, 0)
        return best


if __name__ == "__main__":
    s = Solution()
    cases = [
        (["un", "iq", "ue"], 4),
        (["cha", "r", "act", "ers"], 6),
        (["abcdefghijklmnopqrstuvwxyz"], 26),
        (["aa", "bb"], 0),
        (["a", "b", "c", "ab"], 3),
        (["ab", "cd", "cde", "cdef", "efg", "fgh", "abxyz"], 11),
    ]
    for arr, want in cases:
        got = s.maxLength(arr)
        assert got == want, (arr, got, want)
        print(f"maxLength({arr}) = {got}")
    print("All tests passed.")
