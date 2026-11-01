"""
LeetCode 394: Decode String
Difficulty: Medium
Topic: Stack / Nested Parsing

Problem
-------
An encoded string uses the rule k[encoded_string]: the part inside the
brackets repeats exactly k times. Brackets can nest. Return the decoded
string.

Examples:
  "3[a]2[bc]"     ->  "aaabcbc"
  "3[a2[c]]"      ->  "accaccacc"
  "2[abc]3[cd]ef" ->  "abcabccdcdcdef"

Approach (thought process)
--------------------------
1. Nesting is the whole difficulty. When we hit '[' we are starting a new,
   inner piece of text, but we must remember two things to come back to:
   the text built so far at the outer level, and the repeat count that was
   written just before this bracket.
2. That "pause the outer work, do the inner work, then resume" shape is
   exactly what a stack is for. Push (outer_text, k) on '['.
3. Scan left to right with two running values:
     - cur: the text being built at the current depth
     - num: the number being read (counts can be multi-digit, like 12[a])
   On a digit, num = num * 10 + digit. On a letter, append to cur.
   On '[', push (cur, num) and reset both. On ']', pop (prev, k) and set
   cur = prev + cur * k, which folds the finished inner piece back into
   its parent.
4. At the end, cur holds the fully decoded string.

Why it works: every ']' closes the most recently opened '[', and the stack
top is exactly the context saved at that '['. So each inner block is
expanded once, with the right count, and glued onto the right prefix. Inner
blocks finish before outer ones, so by the time an outer block repeats, its
content is already fully decoded.

Complexity:
  - Time: O(output length), since every character of the answer is built
    a bounded number of times by the string joins (in the worst case
    proportional to the final size).
  - Space: O(output length) for the strings, plus O(depth) stack frames.
"""


class Solution:
    def decodeString(self, s: str) -> str:
        stack = []
        cur_parts = []
        num = 0
        for ch in s:
            if ch.isdigit():
                num = num * 10 + int(ch)
            elif ch == "[":
                stack.append(("".join(cur_parts), num))
                cur_parts, num = [], 0
            elif ch == "]":
                prev, k = stack.pop()
                cur_parts = [prev + "".join(cur_parts) * k]
            else:
                cur_parts.append(ch)
        return "".join(cur_parts)


if __name__ == "__main__":
    sol = Solution()
    cases = [
        ("3[a]2[bc]", "aaabcbc"),
        ("3[a2[c]]", "accaccacc"),
        ("2[abc]3[cd]ef", "abcabccdcdcdef"),
        ("10[x]", "x" * 10),
        ("abc", "abc"),
        ("2[a2[b3[c]]]d", "abcccbcccabcccbcccd"),
    ]
    for s, want in cases:
        got = sol.decodeString(s)
        assert got == want, (s, got, want)
        print(f"{s!r:>18} -> {got!r}")
    print("all tests passed")
