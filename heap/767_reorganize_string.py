"""
LeetCode 767: Reorganize String
Difficulty: Medium
Topic: Heaps / Greedy Scheduling

Problem
-------
Rearrange the characters of s so no two adjacent characters are the same.
Return any valid arrangement, or "" if none exists.

Approach (thought process)
--------------------------
1. Feasibility first: the most frequent char needs a different char between
   each pair of its copies. With n slots, it can occupy at most ceil(n/2) of
   them (every other position). If max_count > (n + 1) // 2, return "".
2. Greedy rule: at every step, place the character with the most copies left
   that isn't the one we just placed. Spending the biggest pile early keeps it
   from piling up at the end where it would be forced to sit next to itself.
3. Max-heap of (-count, char) gives the biggest pile in O(log k). To forbid
   the just-used char, pop it and hold it aside for one turn; push it back
   after placing the next char. (Same "cooldown" trick as Task Scheduler 621.)
4. Why it works: if feasibility holds, the held-aside char is never the only
   one left with copies remaining unless it's the very last placement, so the
   heap never runs dry early. We still guard: if the heap is empty while a
   held char remains, there's no valid answer.

Complexity
----------
Time:  O(n log k), k = distinct chars (<= 26, so effectively O(n)).
Space: O(k) for the heap plus O(n) for the output.
"""

import heapq
from collections import Counter


class Solution:
    def reorganizeString(self, s: str) -> str:
        counts = Counter(s)
        if counts and max(counts.values()) > (len(s) + 1) // 2:
            return ""
        heap = [(-c, ch) for ch, c in counts.items()]
        heapq.heapify(heap)
        out = []
        held = None  # (neg_count, char) cooling down for one turn
        while heap:
            neg, ch = heapq.heappop(heap)
            out.append(ch)
            if held:
                heapq.heappush(heap, held)
            held = (neg + 1, ch) if neg + 1 < 0 else None
        return "".join(out) if not held else ""


def _valid(original: str, result: str) -> bool:
    if Counter(original) != Counter(result):
        return False
    return all(a != b for a, b in zip(result, result[1:]))


if __name__ == "__main__":
    sol = Solution()
    cases = [
        ("aab", True),
        ("aaab", False),
        ("vvvlo", True),
        ("a", True),
        ("aabbcc", True),
        ("aaabbbccc", True),
        ("aaaabc", False),
    ]
    for s, possible in cases:
        got = sol.reorganizeString(s)
        if possible:
            assert _valid(s, got), (s, got)
        else:
            assert got == "", (s, got)
        print(f"{s!r} -> {got!r}")
    print("All tests passed.")
