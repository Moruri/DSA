"""
LeetCode 1851: Minimum Interval to Include Each Query
Difficulty: Hard
Topic: Intervals / Offline Sweep + Min-Heap

Problem
-------
You get a list of closed intervals [l, r] (size = r - l + 1) and a list of
query points. For each query q, return the size of the smallest interval
that contains q (l <= q <= r), or -1 if no interval contains it.

Examples:
  intervals = [[1, 4], [2, 4], [3, 6], [4, 4]], queries = [2, 3, 4, 5]
      ->  [3, 3, 1, 4]
  intervals = [[2, 3], [2, 5], [1, 8], [20, 25]], queries = [2, 19, 5, 22]
      ->  [2, -1, 4, 6]

Approach (thought process)
--------------------------
1. Brute force checks every interval for every query: O(n * q), too slow at
   1e5 each. We need to share work between queries.
2. Answer the queries OFFLINE: we don't have to answer them in the order
   given, so sort them ascending (remembering their original index).
   Sort the intervals by left endpoint too.
3. Sweep q from small to large. Before answering q, push every interval whose
   left end is <= q onto a min-heap keyed by (size, right end). Those are all
   the intervals that have "opened" by now.
4. Some opened intervals may already have closed (right end < q). Pop them
   off the top while the top's right end < q. Then the top, if any, is the
   smallest interval that contains q.
5. Lazy deletion is safe: an interval with right end < q is also useless for
   every later (larger) query, so throwing it away forever never loses an
   answer. Intervals buried deeper in the heap that are dead don't matter
   until they surface, and then they get popped.

Why it works: at query q the heap holds exactly the intervals with l <= q
(minus some that ended before q). After popping dead tops, the top has
l <= q <= r and the smallest size among all still-alive candidates, which is
the answer. Sorting queries is what lets each interval be pushed and popped
at most once across the whole sweep.

Complexity:
  - Time: O(n log n + q log q), sorting plus at most one push/pop per interval.
  - Space: O(n + q) for the heap and the answer array.
"""

import heapq
from typing import List


class Solution:
    def minInterval(self, intervals: List[List[int]], queries: List[int]) -> List[int]:
        intervals = sorted(intervals)
        ans = [-1] * len(queries)
        heap: List[tuple] = []  # (size, right end)
        i = 0
        for q, idx in sorted((q, idx) for idx, q in enumerate(queries)):
            # Open every interval that starts at or before q.
            while i < len(intervals) and intervals[i][0] <= q:
                l, r = intervals[i]
                heapq.heappush(heap, (r - l + 1, r))
                i += 1
            # Drop intervals that already ended; they can't help later queries either.
            while heap and heap[0][1] < q:
                heapq.heappop(heap)
            if heap:
                ans[idx] = heap[0][0]
        return ans


def _brute(intervals: List[List[int]], queries: List[int]) -> List[int]:
    out = []
    for q in queries:
        sizes = [r - l + 1 for l, r in intervals if l <= q <= r]
        out.append(min(sizes) if sizes else -1)
    return out


if __name__ == "__main__":
    import random

    sol = Solution()
    assert sol.minInterval([[1, 4], [2, 4], [3, 6], [4, 4]], [2, 3, 4, 5]) == [3, 3, 1, 4]
    assert sol.minInterval([[2, 3], [2, 5], [1, 8], [20, 25]], [2, 19, 5, 22]) == [2, -1, 4, 6]
    assert sol.minInterval([[5, 5]], [4, 5, 6]) == [-1, 1, -1]
    assert sol.minInterval([[1, 10]], [10, 1, 10]) == [10, 10, 10]

    rng = random.Random(1851)
    for _ in range(2000):
        ints = []
        for _ in range(rng.randint(0, 8)):
            a = rng.randint(1, 20)
            ints.append([a, a + rng.randint(0, 6)])
        qs = [rng.randint(0, 28) for _ in range(rng.randint(1, 8))]
        assert sol.minInterval([x[:] for x in ints], qs[:]) == _brute(ints, qs), (ints, qs)
    print("All tests passed for 1851.")
