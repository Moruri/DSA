"""
LeetCode 5: Longest Palindromic Substring
Difficulty: Medium
Topic: Strings / Two Pointers (expand around center)

Problem
-------
Given a string s, return the longest substring of s that reads the same
forwards and backwards.

Example 1:
  Input:  s = "babad"
  Output: "bab"   ("aba" is also valid)

Example 2:
  Input:  s = "cbbd"
  Output: "bb"

Approach (thought process)
--------------------------
1. Brute force: check all O(n^2) substrings, each check costs O(n), so O(n^3).
   Far too slow for n = 1000 in the worst case.
2. Flip the question around. Instead of asking "is this substring a
   palindrome?", ask "where is the palindrome's center?" Every palindrome is
   a mirror around its middle, and there are only 2n - 1 possible middles:
   n single characters (odd length, like "aba") and n - 1 gaps between
   neighbours (even length, like "abba").
3. From each center, put a left pointer and a right pointer on it and walk
   them outward while s[left] == s[right]. The moment they disagree (or fall
   off the string), the window just inside is the longest palindrome with
   that center.
4. Keep the best (start, length) seen across all centers.

Why it works: any palindrome s[i..j] has a center, and expanding from that
center will grow at least as far as j because every mirrored pair inside it
matches. So the scan never misses the longest one.

Alternative: a DP table dp[i][j] = s[i] == s[j] and dp[i+1][j-1] is also
O(n^2) time but O(n^2) space. Manacher's algorithm reaches O(n), but expand
around center is the interview sweet spot.

Complexity: O(n^2) time in the worst case (e.g. "aaaa...a"), O(1) extra space.
"""

from __future__ import annotations


class Solution:
    def longestPalindrome(self, s: str) -> str:
        if len(s) < 2:
            return s

        best_start, best_len = 0, 1

        def expand(left: int, right: int) -> None:
            nonlocal best_start, best_len
            while left >= 0 and right < len(s) and s[left] == s[right]:
                left -= 1
                right += 1
            # The palindrome is s[left + 1 : right].
            length = right - left - 1
            if length > best_len:
                best_start, best_len = left + 1, length

        for center in range(len(s)):
            expand(center, center)      # odd length, one middle character
            expand(center, center + 1)  # even length, middle is a gap

        return s[best_start : best_start + best_len]


def _brute(s: str) -> int:
    best = 0
    for i in range(len(s)):
        for j in range(i, len(s)):
            sub = s[i : j + 1]
            if sub == sub[::-1]:
                best = max(best, len(sub))
    return best


def _demo() -> None:
    sol = Solution()
    cases = [
        ("babad", {"bab", "aba"}),
        ("cbbd", {"bb"}),
        ("a", {"a"}),
        ("forgeeksskeegfor", {"geeksskeeg"}),
        ("abacdfgdcaba", {"aba", "aca"}),
    ]
    for s, valid in cases:
        got = sol.longestPalindrome(s)
        status = "OK" if got in valid else "FAIL"
        print(f"{status}: longestPalindrome({s!r}) -> {got!r}")
        assert got in valid, f"5 returned {got!r} for {s!r}"

    import random

    rng = random.Random(5)
    for _ in range(300):
        s = "".join(rng.choice("ab") for _ in range(rng.randint(1, 14)))
        got = sol.longestPalindrome(s)
        assert got == got[::-1] and got in s and len(got) == _brute(s), s
    print("OK: 300 random strings match the brute force length")


if __name__ == "__main__":
    _demo()
