"""
LeetCode 621: Task Scheduler
Difficulty: Medium
Topic: Greedy / Heap

Problem
-------
You are given an array of CPU tasks `tasks`, where each letter represents a
different task. Tasks may be done in any order. Each task takes one unit of
time. Between two identical tasks there must be at least `n` units of idle
time (cooldown). Return the least number of units of time the CPU needs to
finish all tasks.

Example 1:
  Input:  tasks = ["A","A","A","B","B","B"], n = 2
  Output: 8
  Explanation: A -> B -> idle -> A -> B -> idle -> A -> B

Example 2:
  Input:  tasks = ["A","C","A","B","D","B"], n = 1
  Output: 6

Example 3:
  Input:  tasks = ["A","A","A","B","B","B"], n = 0
  Output: 6

Approach (thought process)
--------------------------
1. The bottleneck is the most frequent task: if it appears `f` times, you need
   at least `(f - 1)` full cool-down gaps of length `n` between its occurrences,
   plus the final occurrence itself — that frames `(f - 1) * (n + 1) + 1` slots.
2. When several tasks share the same max frequency `f`, each of them also
   occupies one of the "last row" slots, so add `count_of_max` instead of 1:
   `(f - 1) * (n + 1) + count_of_max`.
3. That formula is a lower bound from scheduling pressure, but you can never
   finish faster than simply running every task once — so the answer is
   `max(formula, len(tasks))`. When the cool-down is small or the alphabet is
   diverse, the raw task count wins.
4. Counting frequencies is O(number of tasks); the rest is O(1) over a fixed
   alphabet (26 uppercase letters). No heap simulation needed for the length.

Complexity: O(T) time (T = len(tasks)), O(1) extra space for 26 counters.
"""

from __future__ import annotations

from collections import Counter
from typing import List


class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        """Return the minimum CPU intervals to finish all tasks with cooldown n."""
        if n == 0:
            return len(tasks)

        freq = Counter(tasks)
        max_freq = max(freq.values())
        count_of_max = sum(1 for v in freq.values() if v == max_freq)
        framed = (max_freq - 1) * (n + 1) + count_of_max
        return max(framed, len(tasks))


def _demo() -> None:
    sol = Solution()
    cases = [
        (["A", "A", "A", "B", "B", "B"], 2, 8),
        (["A", "C", "A", "B", "D", "B"], 1, 6),
        (["A", "A", "A", "B", "B", "B"], 0, 6),
        (["A", "A", "A", "A", "B", "B", "B", "C", "C", "D"], 2, 10),
        (["A"], 2, 1),
        (["A", "A"], 2, 4),
        (["A", "B"], 2, 2),
    ]
    for tasks, n, expected in cases:
        got = sol.leastInterval(tasks, n)
        status = "OK" if got == expected else "FAIL"
        print(f"{status}: leastInterval({tasks}, {n}) -> {got} (expected {expected})")
        assert got == expected, (
            f"621 leastInterval({tasks}, {n}) returned {got}, expected {expected}"
        )


if __name__ == "__main__":
    _demo()
