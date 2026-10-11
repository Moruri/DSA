"""
LeetCode 981: Time Based Key-Value Store
Difficulty: Medium
Topic: Binary Search / Design

Problem
-------
Design a TimeMap that stores multiple values for the same key at different
timestamps:
  - set(key, value, timestamp): store value for key at that timestamp.
  - get(key, timestamp): return the value set with the largest
    timestamp_prev <= timestamp, or "" if there is none.
All set() calls arrive with strictly increasing timestamps.

Example:
  set("foo", "bar", 1); get("foo", 1) -> "bar"; get("foo", 3) -> "bar"
  set("foo", "bar2", 4); get("foo", 4) -> "bar2"; get("foo", 5) -> "bar2"

Approach (thought process)
--------------------------
1. Group history per key: a dict from key to a list of (timestamp, value).
2. Because timestamps only ever increase, appending keeps each list sorted
   for free. No sorting, no balanced tree needed.
3. get() is "find the last timestamp <= t" in a sorted list, which is the
   classic upper-bound binary search: bisect_right(timestamps, t) gives the
   first index with timestamp > t, so the answer sits one slot to its left.
   If that index is 0, nothing was set at or before t, so return "".
4. Keep timestamps and values in parallel lists so bisect works directly on
   plain integers.

Why it works: the sorted invariant plus bisect_right's definition means the
element just before the insertion point is exactly the latest version at or
before the requested time.

Complexity: set is O(1) amortised; get is O(log m) where m is the number of
versions stored for that key. Space is O(total set calls).
"""

from bisect import bisect_right
from collections import defaultdict


class TimeMap:
    def __init__(self) -> None:
        self._times = defaultdict(list)
        self._values = defaultdict(list)

    def set(self, key: str, value: str, timestamp: int) -> None:
        self._times[key].append(timestamp)
        self._values[key].append(value)

    def get(self, key: str, timestamp: int) -> str:
        times = self._times.get(key)
        if not times:
            return ""
        i = bisect_right(times, timestamp)
        return self._values[key][i - 1] if i else ""


if __name__ == "__main__":
    tm = TimeMap()
    tm.set("foo", "bar", 1)
    assert tm.get("foo", 1) == "bar"
    assert tm.get("foo", 3) == "bar"
    tm.set("foo", "bar2", 4)
    assert tm.get("foo", 4) == "bar2"
    assert tm.get("foo", 5) == "bar2"
    assert tm.get("foo", 0) == ""
    assert tm.get("missing", 10) == ""
    print("981 Time Based Key-Value Store: all tests passed")
