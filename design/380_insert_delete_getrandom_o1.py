"""
LeetCode 380: Insert Delete GetRandom O(1)
Difficulty: Medium
Topic: Design / Hash Map + Array

Problem
-------
Implement RandomizedSet with three operations, each in average O(1):
  - insert(val): add val if it is not already present; return True iff it was new
  - remove(val): delete val if it is present; return True iff it was there
  - getRandom(): return one of the current values, each equally likely

Duplicates are not allowed. getRandom is never called on an empty set.

Approach (thought process)
--------------------------
1. A hash set gives O(1) insert and remove, but not O(1) uniform random
   access — there is no "element at index i". An array gives O(1) random
   (pick a random index) and O(1) append, but finding a value to delete
   is O(n), and deleting from the middle shifts the tail.
2. Keep both: an array `vals` that holds the current elements packed
   densely, plus a map `idx` from value -> its index in `vals`.
     insert: if val is new, append it and record the new index.
     getRandom: return vals[random index] — every slot is live, so this
       is uniform.
     remove: this is the trick. To delete without leaving a hole or
       shifting, swap the target with the last element, then pop the
       tail (which is now the value we wanted gone):
         - look up i = idx[val]
         - move vals[-1] into slot i, and update that element's index
         - pop the tail and delete val from the map
       If val already was last, the swap is a no-op and the pop still
       works. Do the map update before the pop so we don't corrupt the
       index of a singleton.
3. insert/remove return a boolean so the caller can tell whether the
   set actually changed — that is just "was it in the map?"

Why it works: the map makes "where is this value?" O(1), and swap-with-
last keeps the array compact without a linear shift. Because every live
value occupies exactly one index in [0, n), a uniform random index is a
uniform random value. No holes means we never accidentally sample a
deleted item.

Complexity:
  - Time: O(1) average for insert, remove, and getRandom.
  - Space: O(n) for the array and the map.
"""

import random


class RandomizedSet:
    def __init__(self):
        self.vals: list[int] = []
        self.idx: dict[int, int] = {}

    def insert(self, val: int) -> bool:
        if val in self.idx:
            return False
        self.idx[val] = len(self.vals)
        self.vals.append(val)
        return True

    def remove(self, val: int) -> bool:
        if val not in self.idx:
            return False
        i = self.idx[val]
        last = self.vals[-1]
        self.vals[i] = last
        self.idx[last] = i
        self.vals.pop()
        del self.idx[val]
        return True

    def getRandom(self) -> int:
        return self.vals[random.randrange(len(self.vals))]


if __name__ == "__main__":
    rs = RandomizedSet()
    assert rs.insert(1) is True
    assert rs.insert(2) is True
    assert rs.insert(1) is False
    assert rs.remove(1) is True
    assert rs.remove(1) is False
    assert rs.insert(2) is False
    assert rs.getRandom() == 2
    assert rs.insert(3) is True
    assert rs.insert(4) is True
    # Removing a middle element must keep the remaining values intact.
    assert rs.remove(2) is True
    remaining = {rs.getRandom() for _ in range(40)}
    assert remaining == {3, 4}, remaining
    # Swap-with-last on the final element, then refill.
    assert rs.remove(4) is True
    assert rs.remove(3) is True
    assert rs.insert(10) is True
    assert rs.insert(20) is True
    assert rs.insert(30) is True
    seen = {rs.getRandom() for _ in range(200)}
    assert seen == {10, 20, 30}, seen
    print("insert/remove/getRandom checks passed")
    print("sample draws:", [rs.getRandom() for _ in range(8)])
    print("all tests passed")
