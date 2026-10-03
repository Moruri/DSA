"""
LeetCode 76: Minimum Window Substring
Difficulty: Hard
Topic: Sliding Window

Problem
-------
Given two strings `s` and `t`, return the minimum window substring of `s`
such that every character in `t` (including duplicates) is included in the
window. If there is no such window, return the empty string `""`. The test
cases guarantee that the answer is unique when it exists.

Example 1:
  Input:  s = "ADOBECODEBANC", t = "ABC"
  Output: "BANC"

Example 2:
  Input:  s = "a", t = "a"
  Output: "a"

Example 3:
  Input:  s = "a", t = "aa"
  Output: ""

Approach (thought process)
--------------------------
1. Brute force over every substring that covers `t` is O(|s|² · |t|) — too
   slow. A sliding window shrinks whenever the window is already valid.
2. Count required frequencies from `t` (`need`). Grow `right` across `s`,
   tracking how many of those requirements are fully satisfied (`have`).
3. When `have == required` (every distinct char in `t` is covered at its
   needed count), shrink `left` as far as possible while the window stays
   valid, recording the shortest span seen.
4. Character counts that drop below `need` decrement `have`, which forces
   the window to grow again. Each index enters/leaves at most once.

Complexity: O(|s| + |t|) time, O(|Σ|) space for the alphabet.
"""

from __future__ import annotations

from collections import Counter


class Solution:
    def minWindow(self, s: str, t: str) -> str:
        """Return the shortest substring of s that covers every char in t."""
        if not t or not s or len(t) > len(s):
            return ""

        need = Counter(t)
        required = len(need)
        have = 0
        window: Counter[str] = Counter()
        best_len = float("inf")
        best_start = 0
        left = 0

        for right, ch in enumerate(s):
            window[ch] += 1
            if ch in need and window[ch] == need[ch]:
                have += 1

            while have == required and left <= right:
                cur_len = right - left + 1
                if cur_len < best_len:
                    best_len = cur_len
                    best_start = left
                left_ch = s[left]
                window[left_ch] -= 1
                if left_ch in need and window[left_ch] < need[left_ch]:
                    have -= 1
                left += 1

        if best_len == float("inf"):
            return ""
        return s[best_start : best_start + int(best_len)]


def _demo() -> None:
    sol = Solution()
    cases = [
        ("ADOBECODEBANC", "ABC", "BANC"),
        ("a", "a", "a"),
        ("a", "aa", ""),
        ("aa", "aa", "aa"),
        ("bba", "ab", "ba"),
        ("cabwefgewcwaefgcf", "cae", "cwae"),
    ]
    for s, t, expected in cases:
        got = sol.minWindow(s, t)
        status = "OK" if got == expected else "FAIL"
        print(f"{status}: minWindow({s!r}, {t!r}) -> {got!r} (expected {expected!r})")
        assert got == expected, (
            f"76 minWindow({s!r}, {t!r}) returned {got!r}, expected {expected!r}"
        )


if __name__ == "__main__":
    _demo()
