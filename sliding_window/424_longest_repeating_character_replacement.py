"""
LeetCode 424: Longest Repeating Character Replacement
Link: https://leetcode.com/problems/longest-repeating-character-replacement/
Difficulty: Medium
Topic: Sliding Window

Problem
-------
You are given a string s and an integer k. You can choose any character of the
string and change it to any other uppercase English character. You can perform
this operation at most k times.

Return the length of the longest substring containing the same letter you can
achieve after performing the above operations.

Example 1:
  Input:  s = "ABAB", k = 2
  Output: 4
  Explanation: Replace the two 'A's with two 'B's (or vice versa).

Example 2:
  Input:  s = "AABABBA", k = 1
  Output: 4
  Explanation: Replace the middle 'A' so one window becomes "AABBBB" or
  "AAAABA" — longest same-letter run of length 4.

Approach (thought process)
--------------------------
1. Brute force: try every substring and check whether it can become uniform
   with ≤ k replacements. That is O(n²) windows times O(n) to count — too slow.
2. Observation: inside a window of length L, the cheapest way to make every
   character the same is to keep the most frequent character and rewrite the
   rest. So the window is valid iff L - max_freq ≤ k.
3. Grow a sliding window [left, right]. Maintain a frequency map of characters
   inside the window and track the highest frequency seen so far in it.
4. When the window becomes invalid (right - left + 1 - max_freq > k), advance
   left and decrement the count of the character that leaves. We never need to
   shrink max_freq aggressively: an outdated (slightly high) max_freq only
   makes the validity check stricter, and the true maximum is refreshed as
   soon as a denser character appears while expanding.
5. After each expansion the window is either valid or we just repaired it, so
   update the answer with the current length. Each index enters and leaves at
   most once.

Complexity: O(n) time (alphabet is fixed at 26), O(1) extra space for the
frequency map of uppercase English letters.
"""

from __future__ import annotations


class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        """Return longest same-letter substring length after at most k replacements."""
        counts = [0] * 26
        left = 0
        max_freq = 0
        best = 0

        for right, ch in enumerate(s):
            idx = ord(ch) - ord("A")
            counts[idx] += 1
            max_freq = max(max_freq, counts[idx])

            # Window length minus the dominant character = replacements needed.
            while (right - left + 1) - max_freq > k:
                counts[ord(s[left]) - ord("A")] -= 1
                left += 1

            best = max(best, right - left + 1)

        return best


def _demo() -> None:
    sol = Solution()
    cases = [
        ("ABAB", 2, 4),
        ("AABABBA", 1, 4),
        ("AAAA", 2, 4),
        ("ABCD", 0, 1),
        ("ABCD", 3, 4),
        ("A", 0, 1),
        ("ABBB", 2, 4),
        ("BAAAB", 2, 5),
        ("ABCDE", 1, 2),
        ("AAAB", 0, 3),
    ]
    for s, k, expected in cases:
        got = sol.characterReplacement(s, k)
        status = "OK" if got == expected else "FAIL"
        print(f"{status}: s={s!r}, k={k} -> {got} (expected {expected})")
        assert got == expected, (
            f"424 characterReplacement({s!r}, {k}) returned {got}, "
            f"expected {expected}"
        )


if __name__ == "__main__":
    _demo()
