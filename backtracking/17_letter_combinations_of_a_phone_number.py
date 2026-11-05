"""
LeetCode 17: Letter Combinations of a Phone Number
Difficulty: Medium
Topic: Backtracking / Strings

Problem
-------
Given a string containing digits from 2–9 inclusive, return all possible
letter combinations that the number could represent. Return the answer in
any order.

The mapping of digits to letters (telephone keypad) is:

  2 → a b c
  3 → d e f
  4 → g h i
  5 → j k l
  6 → m n o
  7 → p q r s
  8 → t u v
  9 → w x y z

Example 1:
  Input:  digits = "23"
  Output: ["ad","ae","af","bd","be","bf","cd","ce","cf"]

Example 2:
  Input:  digits = ""
  Output: []

Example 3:
  Input:  digits = "2"
  Output: ["a","b","c"]

Approach (thought process)
--------------------------
1. Each digit expands into 3 or 4 letters. A combination is one letter
   chosen from each digit, in order — so the answer size is the product of
   the letter counts (at most 4^n for n digits). Generating them is a
   classic decision tree: at position i, try every letter for digits[i],
   then move to i+1.
2. Backtracking / DFS: keep a mutable `path` of the letters chosen so far.
   When the path length equals the number of digits, we have a complete
   combination — snapshot `"".join(path)` into the answer and return.
   Otherwise, for each letter of the current digit, append it, recurse to
   the next index, then pop (the undo step that makes backtracking work).
3. Empty input is a special case: there are no digits to choose from, so
   the answer is []. Do not emit the empty string — the problem asks for
   combinations of the given digits, and "no digits" means no combinations.
4. A digit→letters map (dict or array indexed by digit char) keeps the
   expansion table out of the recursive body so the DFS stays readable.

Why it works: every root-to-leaf path in the decision tree picks exactly
one letter per digit, and every possible pick sequence appears as some
path. The undo step restores the path so sibling branches start clean.

Complexity:
  - Time: O(4^n · n) worst case — up to 4^n combinations, each costing
    O(n) to build/copy the string.
  - Space: O(n) recursion depth and path, plus O(4^n · n) for the output.
"""

from __future__ import annotations

from typing import List


class Solution:
    KEYPAD = {
        "2": "abc",
        "3": "def",
        "4": "ghi",
        "5": "jkl",
        "6": "mno",
        "7": "pqrs",
        "8": "tuv",
        "9": "wxyz",
    }

    def letterCombinations(self, digits: str) -> List[str]:
        if not digits:
            return []

        ans: List[str] = []
        path: List[str] = []

        def dfs(i: int) -> None:
            if i == len(digits):
                ans.append("".join(path))
                return
            for ch in self.KEYPAD[digits[i]]:
                path.append(ch)
                dfs(i + 1)
                path.pop()

        dfs(0)
        return ans


def _demo() -> None:
    sol = Solution()
    cases = [
        ("23", ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]),
        ("", []),
        ("2", ["a", "b", "c"]),
        ("7", ["p", "q", "r", "s"]),
        ("9", ["w", "x", "y", "z"]),
    ]
    for digits, expected in cases:
        got = sol.letterCombinations(digits)
        # Order is not required by the problem; compare as multisets.
        ok = sorted(got) == sorted(expected)
        print(f"{'OK' if ok else 'FAIL'}: {digits!r} -> {got} (expected {expected})")
        assert ok, f"17 letterCombinations({digits!r}) returned {got}, expected {expected}"

    # Spot-check a longer input's size: "234" → 3*3*3 = 27 combinations.
    got234 = sol.letterCombinations("234")
    assert len(got234) == 27 and len(set(got234)) == 27
    print(f"OK: '234' produced {len(got234)} unique combinations")


if __name__ == "__main__":
    _demo()
