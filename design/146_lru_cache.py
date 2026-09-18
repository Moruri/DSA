"""
LeetCode 146: LRU Cache
Link: https://leetcode.com/problems/lru-cache/
Difficulty: Medium
Topic: Design

Problem
-------
Design a data structure that follows the constraints of a Least Recently Used
(LRU) cache.

Implement the LRUCache class:
  - LRUCache(capacity) initialize with positive size capacity
  - get(key) return the value if key exists, else -1
  - put(key, value) update or insert the value; if capacity would be exceeded,
    evict the least recently used key before inserting

Both get and put must run in O(1) average time.

Example:
  LRUCache cache = LRUCache(2)
  cache.put(1, 1)
  cache.put(2, 2)
  cache.get(1)       # returns 1
  cache.put(3, 3)    # evicts key 2
  cache.get(2)       # returns -1
  cache.put(4, 4)    # evicts key 1
  cache.get(1)       # returns -1
  cache.get(3)       # returns 3
  cache.get(4)       # returns 4

Approach (thought process)
--------------------------
1. A plain dict gives O(1) get/put by key but has no notion of recency. A plain
   list/deque can track order but looking up or moving a key is O(n). We need
   both: fast key lookup *and* fast "move to most-recent / drop least-recent".
2. Pair a hash map with a doubly linked list. The map stores key -> node. The
   list orders nodes from least-recent (head side) to most-recent (tail side).
   Dummy head/tail sentinels avoid null checks on every splice.
3. get: if the key is missing return -1; otherwise look up the node, move it
   to the tail (most recent), and return its value. Moving is unlink + append,
   both O(1) with a doubly linked list.
4. put: if the key already exists, update its value and move it to the tail.
   Otherwise create a new node, append it, and record it in the map. If size
   now exceeds capacity, unlink the node after the head (the LRU), delete it
   from the map, and discard it.
5. OrderedDict.move_to_end / popitem(last=False) is the same idea in one
   built-in; the explicit list below makes the O(1) mechanics interview-clear.

Complexity: O(1) time per get/put, O(capacity) space.
"""

from __future__ import annotations

from typing import Dict, Optional


class _Node:
    """Doubly linked list node holding one cache entry."""

    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key: int = 0, value: int = 0) -> None:
        self.key = key
        self.value = value
        self.prev: Optional[_Node] = None
        self.next: Optional[_Node] = None


class LRUCache:
    def __init__(self, capacity: int) -> None:
        """Initialize the cache with a positive capacity."""
        self.capacity = capacity
        self.map: Dict[int, _Node] = {}
        # Sentinels: head <-> ... <-> tail. Real nodes live strictly between them.
        self.head = _Node()
        self.tail = _Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _unlink(self, node: _Node) -> None:
        """Remove node from its current position in the list."""
        prev_n = node.prev
        next_n = node.next
        assert prev_n is not None and next_n is not None
        prev_n.next = next_n
        next_n.prev = prev_n

    def _append(self, node: _Node) -> None:
        """Insert node just before the tail sentinel (most recently used)."""
        prev_n = self.tail.prev
        assert prev_n is not None
        prev_n.next = node
        node.prev = prev_n
        node.next = self.tail
        self.tail.prev = node

    def _move_to_tail(self, node: _Node) -> None:
        """Mark node as most recently used."""
        self._unlink(node)
        self._append(node)

    def get(self, key: int) -> int:
        """Return value for key, or -1 if missing. Hits refresh recency."""
        node = self.map.get(key)
        if node is None:
            return -1
        self._move_to_tail(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        """Insert or update key. Evict the LRU entry if over capacity."""
        node = self.map.get(key)
        if node is not None:
            node.value = value
            self._move_to_tail(node)
            return

        node = _Node(key, value)
        self.map[key] = node
        self._append(node)

        if len(self.map) > self.capacity:
            lru = self.head.next
            assert lru is not None and lru is not self.tail
            self._unlink(lru)
            del self.map[lru.key]


def _demo() -> None:
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == 1, "get(1) after put 1,2"
    cache.put(3, 3)  # evicts key 2
    assert cache.get(2) == -1, "key 2 should be evicted"
    cache.put(4, 4)  # evicts key 1
    assert cache.get(1) == -1, "key 1 should be evicted"
    assert cache.get(3) == 3, "get(3)"
    assert cache.get(4) == 4, "get(4)"
    print("OK: capacity-2 sequence matches LeetCode example")

    # Capacity 1: every new put evicts the previous key.
    tiny = LRUCache(1)
    tiny.put(1, 10)
    assert tiny.get(1) == 10
    tiny.put(2, 20)
    assert tiny.get(1) == -1
    assert tiny.get(2) == 20
    print("OK: capacity-1 eviction")

    # Update existing key should refresh recency without growing size.
    c = LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    c.put(1, 100)  # update + refresh; 2 is now LRU
    c.put(3, 3)  # evicts 2
    assert c.get(2) == -1
    assert c.get(1) == 100
    assert c.get(3) == 3
    print("OK: update refreshes recency")

    # get on missing key
    assert LRUCache(2).get(99) == -1
    print("OK: missing key returns -1")


if __name__ == "__main__":
    _demo()
