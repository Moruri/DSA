"""
LeetCode 295: Find Median from Data Stream
Difficulty: Hard
Topic: Heap / Two Heaps

Problem
-------
Design a MedianFinder that supports:
  - addNum(num): add an integer from the stream.
  - findMedian(): return the median of everything added so far (the average
    of the two middle values when the count is even).

Example:
  addNum(1), addNum(2) -> findMedian() = 1.5
  addNum(3)            -> findMedian() = 2.0

Approach (thought process)
--------------------------
1. The median only cares about the middle of the sorted order. We never need
   the full sorted list, just "the biggest of the small half" and "the
   smallest of the big half".
2. That is exactly what two heaps give us:
     - `low`  is a max-heap holding the smaller half (Python only has a
       min-heap, so store negatives).
     - `high` is a min-heap holding the larger half.
3. Keep two invariants after every insert:
     a. Ordering: every value in `low` <= every value in `high`.
     b. Balance: len(low) == len(high) or len(low) == len(high) + 1.
4. Insert trick that maintains both with no case analysis: push the new
   number into `low`, then move low's largest over to `high` (this fixes the
   ordering), and if `high` is now bigger, move its smallest back to `low`
   (this fixes the balance).
5. Median: if `low` has the extra element, it is -low[0]; otherwise average
   the two tops.

Why it works: the ordering invariant means the two heap tops sit right next
to each other in sorted order, and the balance invariant means they are the
middle element(s). Each insert does a constant number of heap moves, so the
invariants are cheap to restore.

Complexity:
  - addNum: O(log n) (at most three heap pushes/pops).
  - findMedian: O(1) (peek at the tops).
  - Space: O(n) for all stored numbers.

Follow-ups: if every number is in [0, 100], a 101-slot count array lets you
walk to the median in O(100). If 99% are in that range, keep counts for the
range plus small overflow lists for outliers.
"""

import heapq


class MedianFinder:
    def __init__(self) -> None:
        self.low = []   # max-heap via negatives: the smaller half
        self.high = []  # min-heap: the larger half

    def addNum(self, num: int) -> None:
        heapq.heappush(self.low, -num)
        # Move the largest of the small half across to keep ordering.
        heapq.heappush(self.high, -heapq.heappop(self.low))
        # Rebalance so low is never smaller than high.
        if len(self.high) > len(self.low):
            heapq.heappush(self.low, -heapq.heappop(self.high))

    def findMedian(self) -> float:
        if len(self.low) > len(self.high):
            return float(-self.low[0])
        return (-self.low[0] + self.high[0]) / 2.0


if __name__ == "__main__":
    import random
    import statistics

    mf = MedianFinder()
    mf.addNum(1)
    mf.addNum(2)
    assert mf.findMedian() == 1.5
    mf.addNum(3)
    assert mf.findMedian() == 2.0

    # Randomized check against the brute-force median.
    for _ in range(200):
        mf = MedianFinder()
        seen = []
        for _ in range(random.randint(1, 60)):
            x = random.randint(-1000, 1000)
            mf.addNum(x)
            seen.append(x)
            assert mf.findMedian() == statistics.median(seen)
    print("All tests passed for 295.")
