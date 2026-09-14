"""
LeetCode 3: Longest Substring Without Repeating Characters
Link: https://leetcode.com/problems/longest-substring-without-repeating-characters/
Difficulty: Medium
Topic: Sliding Window

Problem
-------
Given a string s, find the length of the longest substring without
duplicate characters.

Example 1:
  Input:  s = "abcabcbb"
  Output: 3
  Explanation: The answer is "abc", with a length of 3.

Example 2:
  Input:  s = "bbbbb"
  Output: 1
  Explanation: The answer is "b", with a length of 1.

Example 3:
  Input:  s = "pwwkew"
  Output: 3
  Explanation: The answer is "wke", with a length of 3. Note that "pwke" is
  a subsequence, not a substring.

Approach (thought process)
--------------------------
1. Brute force: check every substring s[i..j] for duplicates. That is O(n^2)
   substrings, each costing O(n) to validate — O(n^3), far too slow.
2. Observation: if s[i..j] has no repeats, then neither does any substring
   inside it. And if s[i..j] *does* contain a repeat, extending j further can
   never fix it — only advancing i can. That monotonic structure is exactly
   what a sliding window exploits.
3. Maintain a window [left, right] that never contains a duplicate. Walk
   right from 0 to n-1. Before adding s[right], if that character is already
   inside the window, jump left to one past its previous position.
4. A hash map last_seen[ch] -> most recent index of ch lets that jump happen
   in O(1). Guard with max(left, ...) so a stale index that is already
   *behind* left can never move the window backwards.
5. After each step the window is valid, so update the answer with
   right - left + 1. Each index enters and leaves the window at most once.

Complexity: O(n) time, O(min(n, alphabet)) extra space.
"""

from __future__ import annotations


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        """Return the length of the longest substring with all-distinct characters."""
        last_seen: dict[str, int] = {}  # character -> most recent index
        left = 0
        best = 0

        for right, ch in enumerate(s):
            if ch in last_seen and last_seen[ch] >= left:
                # ch is already inside the window: shrink from the left so the
                # window starts just past its previous occurrence.
                left = last_seen[ch] + 1
            last_seen[ch] = right
            best = max(best, right - left + 1)

        return best


def _demo() -> None:
    sol = Solution()
    cases = [
        ("abcabcbb", 3),
        ("bbbbb", 1),
        ("pwwkew", 3),
        ("", 0),
        (" ", 1),
        ("au", 2),
        ("dvdf", 3),  # stale index for 'd' must not move the window backwards
        ("abba", 2),
        ("tmmzuxt", 5),
        ("abcdefg", 7),
    ]
    for s, expected in cases:
        got = sol.lengthOfLongestSubstring(s)
        status = "OK" if got == expected else "FAIL"
        print(f"{status}: s={s!r} -> {got} (expected {expected})")
        assert got == expected, (
            f"3 lengthOfLongestSubstring({s!r}) returned {got}, expected {expected}"
        )


if __name__ == "__main__":
    _demo()
