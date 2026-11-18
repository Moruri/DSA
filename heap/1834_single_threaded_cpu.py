"""
LeetCode 1834: Single-Threaded CPU
Difficulty: Medium
Topic: Heap / Priority Queue (event simulation)

Problem
-------
tasks[i] = [enqueueTime_i, processingTime_i]. A single-threaded CPU:
  - If idle with no available tasks, it stays idle.
  - If idle with available tasks, it picks the one with the shortest
    processing time; ties go to the smallest index.
  - Once started, a task runs to completion, and the CPU can pick the next
    one immediately.
Return the order in which the CPU processes the tasks.

Approach (thought process)
--------------------------
1. Two questions keep repeating: "which tasks have arrived by now?" and
   "among those, which is shortest (then lowest index)?"
2. The first one is a sweep: sort task indices by enqueue time and keep a
   pointer i. Whenever the clock moves, push every task with
   enqueueTime <= time into the pool.
3. The second one is a min-heap keyed by (processingTime, index). The tuple
   order encodes both the main rule and the tie-break.
4. Main loop:
   - Feed every arrived task into the heap.
   - If the heap is empty, the CPU is idle. Jump the clock straight to the
     next enqueue time instead of ticking one unit at a time (times reach
     1e9).
   - Otherwise pop the best task, record its index, and advance the clock
     by its processing time. No preemption, so the clock moves in one jump.
5. Every task is pushed once and popped once, so the heap work is bounded.

Complexity
----------
Time:  O(n log n) for the sort plus n pushes and n pops.
Space: O(n) for the sorted order and the heap.
"""

import heapq
from typing import List


class Solution:
    def getOrder(self, tasks: List[List[int]]) -> List[int]:
        order = sorted(range(len(tasks)), key=lambda k: tasks[k][0])
        heap: List[tuple] = []
        result: List[int] = []
        time = 0
        i = 0
        n = len(tasks)

        while len(result) < n:
            while i < n and tasks[order[i]][0] <= time:
                idx = order[i]
                heapq.heappush(heap, (tasks[idx][1], idx))
                i += 1
            if not heap:
                time = tasks[order[i]][0]  # idle: jump to the next arrival
                continue
            proc, idx = heapq.heappop(heap)
            result.append(idx)
            time += proc
        return result


def simulate(tasks: List[List[int]]) -> List[int]:
    """Slow reference: scan all waiting tasks at each decision."""
    remaining = set(range(len(tasks)))
    time, out = 0, []
    while remaining:
        ready = [k for k in remaining if tasks[k][0] <= time]
        if not ready:
            time = min(tasks[k][0] for k in remaining)
            continue
        k = min(ready, key=lambda k: (tasks[k][1], k))
        out.append(k)
        remaining.remove(k)
        time += tasks[k][1]
    return out


if __name__ == "__main__":
    import random

    sol = Solution()
    assert sol.getOrder([[1, 2], [2, 4], [3, 2], [4, 1]]) == [0, 2, 3, 1]
    assert sol.getOrder([[7, 10], [7, 12], [7, 5], [7, 4], [7, 2]]) == [4, 3, 2, 0, 1]
    assert sol.getOrder([[5, 2]]) == [0]
    assert sol.getOrder([[1, 1], [100, 1]]) == [0, 1]  # idle gap
    random.seed(1834)
    for _ in range(300):
        tasks = [[random.randint(1, 20), random.randint(1, 6)]
                 for _ in range(random.randint(1, 10))]
        assert sol.getOrder(tasks) == simulate(tasks)
    print("All tests passed.")
