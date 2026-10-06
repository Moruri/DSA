"""
LeetCode 210: Course Schedule II
Difficulty: Medium
Topic: Graphs / Topological Sort (Kahn's algorithm)

Problem
-------
There are `numCourses` courses labelled 0..numCourses-1. Each pair
prerequisites[i] = [a, b] means you must take course b before course a.
Return any order that lets you finish every course, or [] if that's
impossible (the prerequisites contain a cycle).

Example 1:
  Input:  numCourses = 2, prerequisites = [[1, 0]]
  Output: [0, 1]

Example 2:
  Input:  numCourses = 4, prerequisites = [[1, 0], [2, 0], [3, 1], [3, 2]]
  Output: [0, 1, 2, 3]  (or [0, 2, 1, 3])

Approach (thought process)
--------------------------
1. Model courses as nodes and draw an edge b -> a for "b unlocks a". A valid
   study plan is exactly a topological order of that directed graph.
2. 207 (Course Schedule) only asked *whether* such an order exists. Here we
   have to produce it, and Kahn's algorithm gives the order for free.
3. Count each node's in-degree (how many prerequisites it still waits on).
   Every course with in-degree 0 can be taken right now, so queue them.
4. Pop a course, append it to the answer, and "complete" it: decrement the
   in-degree of every course it unlocks. Any that hits 0 joins the queue.
5. If the answer ends up with all numCourses courses, it's a valid order.
   If some are missing, those courses sit on (or behind) a cycle: their
   in-degree never dropped to 0, so no order exists and we return [].

Why it works: a course is only emitted once all its prerequisites have been
emitted, so every edge b -> a has b before a in the output. A cycle can
never be emitted because each node on it always waits on the previous one.

Complexity: O(V + E) time and O(V + E) space for the adjacency lists,
where V = numCourses and E = len(prerequisites).
"""

from __future__ import annotations

from collections import deque
from typing import List


class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        """Return a valid course order, or [] when a cycle blocks it."""
        unlocks: List[List[int]] = [[] for _ in range(numCourses)]
        indegree = [0] * numCourses
        for course, prereq in prerequisites:
            unlocks[prereq].append(course)
            indegree[course] += 1

        ready = deque(c for c in range(numCourses) if indegree[c] == 0)
        order: List[int] = []
        while ready:
            course = ready.popleft()
            order.append(course)
            for nxt in unlocks[course]:
                indegree[nxt] -= 1
                if indegree[nxt] == 0:  # last prerequisite just finished
                    ready.append(nxt)

        return order if len(order) == numCourses else []


def _is_valid(n: int, prereqs: List[List[int]], order: List[int]) -> bool:
    if sorted(order) != list(range(n)):
        return False
    pos = {c: i for i, c in enumerate(order)}
    return all(pos[b] < pos[a] for a, b in prereqs)


def _has_cycle(n: int, prereqs: List[List[int]]) -> bool:
    graph: List[List[int]] = [[] for _ in range(n)]
    for a, b in prereqs:
        graph[b].append(a)
    state = [0] * n  # 0 = new, 1 = on stack, 2 = done

    def dfs(u: int) -> bool:
        state[u] = 1
        for v in graph[u]:
            if state[v] == 1 or (state[v] == 0 and dfs(v)):
                return True
        state[u] = 2
        return False

    return any(state[u] == 0 and dfs(u) for u in range(n))


def _demo() -> None:
    sol = Solution()
    cases = [
        (2, [[1, 0]], True),
        (4, [[1, 0], [2, 0], [3, 1], [3, 2]], True),
        (1, [], True),
        (2, [[1, 0], [0, 1]], False),
        (3, [[0, 1], [1, 2], [2, 0]], False),
        (5, [[1, 0], [2, 1], [4, 3]], True),
    ]
    for n, prereqs, possible in cases:
        got = sol.findOrder(n, prereqs)
        ok = _is_valid(n, prereqs, got) if possible else got == []
        print(f"{'OK' if ok else 'FAIL'}: findOrder({n}, {prereqs}) -> {got}")
        assert ok, f"210 returned {got} for n={n}, prereqs={prereqs}"

    import random

    rng = random.Random(210)
    for _ in range(300):
        n = rng.randint(1, 8)
        pairs = {(rng.randrange(n), rng.randrange(n)) for _ in range(rng.randint(0, 12))}
        prereqs = [[a, b] for a, b in pairs if a != b]
        got = sol.findOrder(n, prereqs)
        if _has_cycle(n, prereqs):
            assert got == [], (n, prereqs, got)
        else:
            assert _is_valid(n, prereqs, got), (n, prereqs, got)
    print("OK: 300 random graphs agree with a DFS cycle check")


if __name__ == "__main__":
    _demo()
