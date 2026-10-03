"""
LeetCode 23: Merge k Sorted Lists
Difficulty: Hard
Topic: Linked Lists / Heap

Problem
-------
You are given an array of `k` linked-lists `lists`, each linked-list sorted
in ascending order. Merge all the linked-lists into one sorted linked-list
and return it.

Example 1:
  Input:  lists = [[1,4,5],[1,3,4],[2,6]]
  Output: [1,1,2,3,4,4,5,6]

Example 2:
  Input:  lists = []
  Output: []

Example 3:
  Input:  lists = [[]]
  Output: []

Approach (thought process)
--------------------------
1. Merging pairwise left-to-right is O(k · N) comparisons; a min-heap of the
   current heads keeps the global minimum in O(log k) per pop.
2. Seed the heap with `(node.val, list_index, node)` for every non-empty
   list. The list index breaks ties so Python never compares ListNode
   objects.
3. Repeatedly pop the smallest node, append it to the result, and if it has
   a successor push that successor. A dummy head keeps the first append
   uniform.
4. When the heap empties, every node has been emitted in sorted order.
   Total work is O(N log k) for N total nodes across k lists.

Complexity: O(N log k) time, O(k) heap space beyond the output.
"""

from __future__ import annotations

import heapq
from typing import List, Optional, Tuple


class ListNode:
    def __init__(self, val: int = 0, next: Optional["ListNode"] = None) -> None:
        self.val = val
        self.next = next


class Solution:
    def mergeKLists(
        self, lists: List[Optional[ListNode]]
    ) -> Optional[ListNode]:
        """Merge k sorted linked lists into one sorted list."""
        heap: List[Tuple[int, int, ListNode]] = []
        for i, node in enumerate(lists):
            if node is not None:
                heapq.heappush(heap, (node.val, i, node))

        dummy = ListNode(0)
        tail = dummy
        while heap:
            _, i, node = heapq.heappop(heap)
            tail.next = node
            tail = node
            if node.next is not None:
                nxt = node.next
                heapq.heappush(heap, (nxt.val, i, nxt))
        return dummy.next


def _from_list(values: List[int]) -> Optional[ListNode]:
    dummy = ListNode(0)
    cur = dummy
    for v in values:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def _to_list(head: Optional[ListNode]) -> List[int]:
    out: List[int] = []
    while head is not None:
        out.append(head.val)
        head = head.next
    return out


def _demo() -> None:
    sol = Solution()
    cases = [
        ([[1, 4, 5], [1, 3, 4], [2, 6]], [1, 1, 2, 3, 4, 4, 5, 6]),
        ([], []),
        ([[]], []),
        ([[1]], [1]),
        ([[1, 2], [], [3]], [1, 2, 3]),
        ([[-2, -1, 0], [-3], [1, 2]], [-3, -2, -1, 0, 1, 2]),
    ]
    for raw_lists, expected in cases:
        heads = [_from_list(lst) for lst in raw_lists]
        got = _to_list(sol.mergeKLists(heads))
        status = "OK" if got == expected else "FAIL"
        print(f"{status}: mergeKLists({raw_lists}) -> {got} (expected {expected})")
        assert got == expected, (
            f"23 mergeKLists({raw_lists}) returned {got}, expected {expected}"
        )


if __name__ == "__main__":
    _demo()
