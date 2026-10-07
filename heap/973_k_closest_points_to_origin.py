"""
LeetCode 973: K Closest Points to Origin
Difficulty: Medium
Topic: Heap / Top-K (with a Quickselect alternative)

Problem
-------
Given an array of points where points[i] = [xi, yi] and an integer k, return
the k points closest to the origin (0, 0) by Euclidean distance. The answer
may be returned in any order and is guaranteed to be unique.

Example 1:
  Input:  points = [[1,3],[-2,2]], k = 1
  Output: [[-2,2]]        (distances^2: 10 vs 8)

Example 2:
  Input:  points = [[3,3],[5,-1],[-2,4]], k = 2
  Output: [[3,3],[-2,4]]  (distances^2: 18, 26, 20)

Approach (thought process)
--------------------------
1. Skip the square root. sqrt is monotonic, so comparing x^2 + y^2 ranks the
   points exactly like the true distance, with no floating-point noise.
2. Simplest correct answer: sort by squared distance and take the first k.
   That's O(n log n). It's fine, but we sort far more than we need to: we
   only care which k points win, not the order of the other n - k.
3. Size-k max-heap: keep the k best points seen so far, with the *worst* of
   them on top so it's cheap to kick out. For each new point, push it; if
   the heap grows past k, pop the farthest. At the end the heap holds exactly
   the k closest. Python's heapq is a min-heap, so store the negated distance
   to get max-heap behaviour. Each push/pop costs O(log k), so the total is
   O(n log k), and memory is O(k). This is the same "keep a bouncer at the
   door" pattern as Kth Largest (215) and Top K Frequent (347), and it works
   even if points arrive as a stream.
4. Alternative, quickselect: partition points around a random pivot distance
   (like quicksort, but recurse into only one side) until the first k slots
   hold the k smallest. Average O(n), worst case O(n^2), and it rearranges
   the input. Included below as `kClosestQuickselect` for comparison.

Why the heap version is correct: invariant after processing each point, the
heap contains the k closest points among those seen so far. Pushing a new
point and popping the max keeps the invariant, because the popped point is
farther than (or tied with) every point that remains.

Complexity: heap O(n log k) time, O(k) space; quickselect O(n) average time
(O(n^2) worst case), O(n) space here only because it copies the input.
"""

from __future__ import annotations

import heapq
import random
from typing import List


def _dist2(p: List[int]) -> int:
    return p[0] * p[0] + p[1] * p[1]


class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        """Size-k max-heap (via negated distances)."""
        heap: List[tuple[int, int]] = []  # (-dist2, index)
        for i, p in enumerate(points):
            heapq.heappush(heap, (-_dist2(p), i))
            if len(heap) > k:
                heapq.heappop(heap)  # drop the farthest of the k + 1
        return [points[i] for _, i in heap]

    def kClosestQuickselect(self, points: List[List[int]], k: int) -> List[List[int]]:
        """Average O(n) alternative: partition until the first k are the closest."""
        pts = points[:]  # don't mutate the caller's list
        lo, hi = 0, len(pts) - 1
        while lo < hi:
            pivot_idx = random.randint(lo, hi)
            pts[pivot_idx], pts[hi] = pts[hi], pts[pivot_idx]
            pivot = _dist2(pts[hi])
            store = lo
            for j in range(lo, hi):
                if _dist2(pts[j]) < pivot:
                    pts[store], pts[j] = pts[j], pts[store]
                    store += 1
            pts[store], pts[hi] = pts[hi], pts[store]
            if store == k - 1 or store == k:
                break
            if store < k:
                lo = store + 1
            else:
                hi = store - 1
        return pts[:k]


def _canon(points: List[List[int]]) -> List[tuple[int, int]]:
    return sorted(tuple(p) for p in points)


def _demo() -> None:
    sol = Solution()
    cases = [
        ([[1, 3], [-2, 2]], 1, [[-2, 2]]),
        ([[3, 3], [5, -1], [-2, 4]], 2, [[3, 3], [-2, 4]]),
        ([[0, 1], [1, 0]], 2, [[0, 1], [1, 0]]),
        ([[1, 1]], 1, [[1, 1]]),
    ]
    for points, k, expected in cases:
        for name, fn in (("heap", sol.kClosest), ("quickselect", sol.kClosestQuickselect)):
            got = fn(points, k)
            ok = _canon(got) == _canon(expected)
            print(f"{'OK' if ok else 'FAIL'}: {name} k={k} {points} -> {got}")
            assert ok, f"973 {name} returned {got}, expected {expected}"

    rng = random.Random(973)
    for _ in range(300):
        n = rng.randint(1, 40)
        # distinct distances so the answer is unique, as LeetCode guarantees
        seen: set[int] = set()
        points: List[List[int]] = []
        while len(points) < n:
            p = [rng.randint(-50, 50), rng.randint(-50, 50)]
            if _dist2(p) not in seen:
                seen.add(_dist2(p))
                points.append(p)
        k = rng.randint(1, n)
        expected = sorted(points, key=_dist2)[:k]
        assert _canon(sol.kClosest(points, k)) == _canon(expected)
        assert _canon(sol.kClosestQuickselect(points, k)) == _canon(expected)
    print("OK: 300 random cases match sort-by-distance for both methods")


if __name__ == "__main__":
    _demo()
