"""
LeetCode 1146: Snapshot Array
Difficulty: Medium
Topic: Design / Binary Search

Problem
-------
Build a SnapshotArray(length) with three operations:
  set(index, val)     -- write val at index
  snap() -> snap_id   -- freeze the current array, return 0, 1, 2, ...
  get(index, snap_id) -- the value at index when snap_id was taken
Up to 5 * 10^4 calls in total, and length can be 5 * 10^4 too.

Approach (thought process)
--------------------------
1. Naive idea: copy the whole array on every snap(). That's O(length) per
   snap, and 5 * 10^4 snaps of a 5 * 10^4 array is 2.5 * 10^9 cells. Too much.
2. Notice that most cells don't change between snaps. Instead of storing
   whole arrays, store each cell's *history*: a list of (snap_id, value)
   pairs, one entry per time that cell was written. Every cell starts as
   [(0, 0)].
3. set(index, val) writes into the current snap generation. If the last
   history entry for that cell already belongs to the current snap_id,
   overwrite it (only the last write before a snap matters). Otherwise
   append (snap_id, val).
4. snap() just bumps a counter and returns the old value. O(1).
5. get(index, snap_id): we need the latest write to that cell made at or
   before snap_id. The cell's history is sorted by snap_id (we only ever
   append increasing ids), so binary search for the rightmost entry with
   id <= snap_id. bisect_right on (snap_id, +inf) lands just past it.

Why it works: the value of a cell at snapshot s is, by definition, the last
value written to it before snap number s was taken -- exactly the entry we
binary-search for. This is the "versioned / persistent value" trick, the same
idea as 981 Time Based Key-Value Store, applied per array cell.

Complexity
----------
set:  O(1) amortized.
snap: O(1).
get:  O(log w), where w = number of writes to that cell.
Space: O(length + total sets) -- only real changes are stored.
"""

from bisect import bisect_right


class SnapshotArray:
    def __init__(self, length: int):
        self.snap_id = 0
        # history[i] = list of [snap_id, value], snap_ids strictly increasing
        self.history = [[[0, 0]] for _ in range(length)]

    def set(self, index: int, val: int) -> None:
        cell = self.history[index]
        if cell[-1][0] == self.snap_id:
            cell[-1][1] = val  # same generation: overwrite
        else:
            cell.append([self.snap_id, val])

    def snap(self) -> int:
        self.snap_id += 1
        return self.snap_id - 1

    def get(self, index: int, snap_id: int) -> int:
        cell = self.history[index]
        # rightmost entry whose id <= snap_id
        pos = bisect_right(cell, [snap_id, float("inf")]) - 1
        return cell[pos][1]


if __name__ == "__main__":
    # LeetCode example 1
    arr = SnapshotArray(3)
    arr.set(0, 5)
    assert arr.snap() == 0
    arr.set(0, 6)
    assert arr.get(0, 0) == 5
    print("example 1: get(0, 0) = 5")

    # overwrites within one generation, untouched cells, many snaps
    arr = SnapshotArray(4)
    arr.set(1, 7)
    arr.set(1, 9)              # overwrites 7 in snap 0
    assert arr.snap() == 0
    assert arr.snap() == 1     # nothing changed in snap 1
    arr.set(1, 4)
    arr.set(3, 2)
    assert arr.snap() == 2
    assert arr.get(1, 0) == 9
    assert arr.get(1, 1) == 9
    assert arr.get(1, 2) == 4
    assert arr.get(3, 1) == 0
    assert arr.get(3, 2) == 2
    assert arr.get(0, 2) == 0
    print("custom case: overwrites, quiet snaps, untouched cells OK")

    # brute-force cross-check against full copies
    import random
    random.seed(1146)
    n = 6
    fast, frozen, live = SnapshotArray(n), [], [0] * n
    for _ in range(400):
        op = random.random()
        if op < 0.5:
            i, v = random.randrange(n), random.randrange(100)
            fast.set(i, v)
            live[i] = v
        elif op < 0.7:
            assert fast.snap() == len(frozen)
            frozen.append(live[:])
        elif frozen:
            s, i = random.randrange(len(frozen)), random.randrange(n)
            assert fast.get(i, s) == frozen[s][i]
    print("random cross-check vs full copies OK")
    print("All tests passed.")
