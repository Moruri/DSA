"""
LeetCode 207: Course Schedule
Link: https://leetcode.com/problems/course-schedule/
Difficulty: Medium
Topic: Graphs / Topological Sort

Problem
-------
There are a total of `numCourses` courses labeled from 0 to numCourses - 1.
You are given an array `prerequisites` where prerequisites[i] = [a_i, b_i]
indicates that you must take course b_i before course a_i.

Return true if you can finish all courses. Otherwise return false.

Example 1:
  Input:  numCourses = 2, prerequisites = [[1, 0]]
  Output: true
  Explanation: Take course 0, then course 1.

Example 2:
  Input:  numCourses = 2, prerequisites = [[1, 0], [0, 1]]
  Output: false
  Explanation: A cycle — neither course can come first.

Approach (thought process)
--------------------------
1. "Can you finish every course?" is exactly: does the prerequisite graph
   admit a valid ordering? That is a topological-sort / cycle-detection job.
2. Model an edge b -> a for each pair [a, b] ("b unlocks a"). Build adjacency
   lists and an indegree array: indegree[a] counts how many prereqs a still
   needs.
3. Kahn's algorithm: seed a queue with every course whose indegree is 0
   (no remaining prereqs). While the queue is non-empty, "take" a course,
   decrement indegrees of its neighbors, and enqueue any neighbor that
   drops to 0.
4. Count how many courses you took. If that equals numCourses, every node
   was reachable in topological order — no cycle. If some courses remain
   with positive indegree, they sit in a cycle and cannot be finished.
5. Iterative BFS avoids recursion-depth issues and makes the "ready set"
   explicit.

Complexity: O(V + E) time and space (V = numCourses, E = |prerequisites|).
"""

from __future__ import annotations

from collections import deque
from typing import List


class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        """Return True iff the prerequisite graph is a DAG (no cycles)."""
        graph: List[List[int]] = [[] for _ in range(numCourses)]
        indegree = [0] * numCourses

        for course, prereq in prerequisites:
            graph[prereq].append(course)
            indegree[course] += 1

        queue: deque[int] = deque(
            course for course in range(numCourses) if indegree[course] == 0
        )
        taken = 0

        while queue:
            course = queue.popleft()
            taken += 1
            for nxt in graph[course]:
                indegree[nxt] -= 1
                if indegree[nxt] == 0:
                    queue.append(nxt)

        return taken == numCourses


def _demo() -> None:
    sol = Solution()
    cases = [
        (2, [[1, 0]], True),
        (2, [[1, 0], [0, 1]], False),
        (1, [], True),
        (3, [[1, 0], [2, 1]], True),
        (3, [[1, 0], [2, 1], [0, 2]], False),
        (4, [[1, 0], [2, 0], [3, 1], [3, 2]], True),
        (5, [], True),
        # Diamond DAG — still acyclic.
        (4, [[1, 0], [2, 0], [3, 1], [3, 2]], True),
        # Self-loop is a cycle.
        (1, [[0, 0]], False),
    ]
    for num_courses, prereqs, expected in cases:
        got = sol.canFinish(num_courses, [row[:] for row in prereqs])
        status = "OK" if got == expected else "FAIL"
        print(
            f"{status}: numCourses={num_courses}, "
            f"prereqs={prereqs} -> {got} (expected {expected})"
        )
        assert got == expected, (
            f"207 canFinish({num_courses}, {prereqs}) returned {got}, "
            f"expected {expected}"
        )


if __name__ == "__main__":
    _demo()
