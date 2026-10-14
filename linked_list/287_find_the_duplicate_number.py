"""
LeetCode 287: Find the Duplicate Number
Difficulty: Medium
Topic: Fast-Slow Pointers / Floyd's Cycle Detection

Problem
-------
nums has n + 1 integers, each in the range [1, n]. Exactly one value is
repeated (possibly many times). Return it without modifying nums and using
only O(1) extra space.

Example:
  nums = [1, 3, 4, 2, 2] -> 2
  nums = [3, 1, 3, 4, 2] -> 3

Approach (thought process)
--------------------------
1. The easy answers break a rule: a set uses O(n) space, sorting modifies
   the array. So we need to squeeze the answer out of the values themselves.
2. Reframe the array as a function: treat index i as a node with one
   outgoing edge to nums[i]. Every value is in [1, n], so every edge points
   at a valid index, and following edges from 0 never stops.
3. Index 0 has no incoming edge (no value is 0), so the walk from 0 must
   eventually fall into a cycle. The node where the tail joins the cycle has
   two incoming edges, meaning two indices hold the same value. That entry
   node IS the duplicate.
4. Floyd's tortoise and hare finds a cycle entry in O(1) space:
   - Phase 1: slow moves 1 step, fast moves 2; they meet somewhere inside
     the cycle.
   - Phase 2: restart one pointer at 0 and move both 1 step at a time. They
     meet at the cycle entry.

Why phase 2 works: let the tail length be a and the cycle length be c, and
say they met k steps into the cycle. Slow walked a + k, fast walked
2(a + k), and the extra a + k is a whole number of loops, so a + k is a
multiple of c. From the meeting point, a more steps lands at offset
k + a, which is 0 mod c: the entry. A pointer starting from 0 also needs
exactly a steps to reach the entry, so they collide there.

Complexity:
  - Time: O(n). Each phase takes at most a few passes around the walk.
  - Space: O(1), and nums is never written to.
"""

from typing import List


class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        # Phase 1: both start at index 0 (the tail's head); find a meeting
        # point inside the cycle.
        slow = fast = 0
        while True:
            slow = nums[slow]
            fast = nums[nums[fast]]
            if slow == fast:
                break

        # Phase 2: find the cycle entry, which is the duplicate value.
        finder = 0
        while finder != slow:
            finder = nums[finder]
            slow = nums[slow]
        return finder


if __name__ == "__main__":
    s = Solution()
    cases = [
        ([1, 3, 4, 2, 2], 2),
        ([3, 1, 3, 4, 2], 3),
        ([1, 1], 1),
        ([1, 1, 2], 1),
        ([2, 2, 2, 2, 2], 2),
        ([1, 4, 4, 2, 4], 4),
        ([2, 5, 9, 6, 9, 3, 8, 9, 7, 1], 9),
    ]
    for nums, expected in cases:
        before = list(nums)
        got = s.findDuplicate(nums)
        assert got == expected, (nums, got, expected)
        assert nums == before, "input must not be modified"

    # Randomized check: build valid inputs with a known duplicate.
    import random

    for _ in range(500):
        n = random.randint(1, 30)
        dup = random.randint(1, n)
        others = random.sample(range(1, n + 1), n)
        # Replace a random number of distinct values with dup so it repeats.
        repeats = random.randint(1, n)
        arr = others[:]
        idxs = random.sample(range(n), repeats)
        for i in idxs:
            arr[i] = dup
        arr.append(dup)
        random.shuffle(arr)
        assert s.findDuplicate(arr) == dup
    print("All tests passed.")
