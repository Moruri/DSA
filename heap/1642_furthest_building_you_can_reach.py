"""
LeetCode 1642: Furthest Building You Can Reach
Difficulty: Medium
Topic: Heap / Greedy

Problem
-------
You walk along buildings with the given heights, starting at index 0. Moving
from building i to i + 1 is free if the next one is the same height or
lower. If it is taller by d, you must pay with either one ladder (covers any
climb) or d bricks. Given some bricks and ladders, return the furthest index
you can reach using them optimally.

Examples:
  heights = [4,2,7,6,9,14,12], bricks = 5, ladders = 1             ->  4
  heights = [4,12,2,7,3,18,20,3,19], bricks = 10, ladders = 2      ->  7
  heights = [14,3,19,3], bricks = 17, ladders = 0                  ->  3

Approach (thought process)
--------------------------
1. A ladder is worth the same no matter how tall the climb, while bricks
   cost exactly the climb height. So ladders should go on the biggest
   climbs and bricks on the small ones. The catch: we don't know the future
   climbs when we are standing at a building.
2. Trick: decide in hindsight. Walk forward and tentatively put a ladder on
   every climb, keeping those climbs in a min-heap. As long as the heap has
   at most `ladders` climbs, everything is covered by ladders.
3. When the heap grows past `ladders`, one climb must be paid with bricks
   instead. The cheapest choice is the smallest climb we've seen so far that
   is "on a ladder", which is the heap minimum. Pop it and pay that many
   bricks.
4. If bricks go negative, we can't make this step, so the answer is the
   current index i (we reached building i but not i + 1).

Why it works: at every point, the heap holds the `ladders` largest climbs
seen so far, and bricks have paid for all the rest. For any prefix of the
walk, that's the cheapest possible brick spending (an exchange argument:
swapping a ladder from a big climb to a small one can only use more bricks).
So if even this best assignment runs out of bricks, no assignment can get
past this building.

Complexity:
  - Time: O(n log L), where L = ladders (the heap never holds more than
    L + 1 climbs).
  - Space: O(L) for the heap.
"""

import heapq
from typing import List


class Solution:
    def furthestBuilding(self, heights: List[int], bricks: int, ladders: int) -> int:
        ladder_climbs = []  # min-heap of climbs currently covered by ladders
        for i in range(len(heights) - 1):
            climb = heights[i + 1] - heights[i]
            if climb <= 0:
                continue
            heapq.heappush(ladder_climbs, climb)
            if len(ladder_climbs) > ladders:
                bricks -= heapq.heappop(ladder_climbs)
                if bricks < 0:
                    return i
        return len(heights) - 1


if __name__ == "__main__":
    sol = Solution()
    cases = [
        ([4, 2, 7, 6, 9, 14, 12], 5, 1, 4),
        ([4, 12, 2, 7, 3, 18, 20, 3, 19], 10, 2, 7),
        ([14, 3, 19, 3], 17, 0, 3),
        ([1, 2], 0, 0, 0),
        ([5, 4, 3, 2], 0, 0, 3),
        ([1, 5, 1, 2, 3, 4, 10000], 4, 1, 5),
    ]
    for h, b, l, want in cases:
        got = sol.furthestBuilding(h, b, l)
        assert got == want, (h, b, l, got, want)
        print(f"heights={h}, bricks={b}, ladders={l} -> {got}")
    print("all tests passed")
