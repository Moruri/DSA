"""
LeetCode 82: Remove Duplicates from Sorted List II
Difficulty: Medium
Topic: Linked Lists (dummy head + run skipping)

Problem
-------
Given the head of a sorted linked list, delete every node whose value
appears more than once, leaving only values that were unique in the
original list. Return the sorted list.

Approach (thought process)
--------------------------
1. Unlike LeetCode 83 (keep one copy), here a duplicated value must vanish
   entirely, including its first copy. So when we stand on a node we can't
   decide whether to keep it until we've peeked at its neighbour.
2. The head itself may be deleted (e.g. 1->1->2). A dummy sentinel in
   front of the head removes that special case: `prev` always points at
   the last node we have committed to keeping, starting at the dummy.
3. Walk with `cur = prev.next`:
   - If cur.next has the same value, cur starts a duplicate run. Skip
     forward while the value repeats, then splice the whole run out with
     prev.next = (first node after the run). Do NOT advance prev, because
     the node right after the run could start another duplicate run.
   - Otherwise cur is unique: commit it by moving prev = cur.
4. Because the list is sorted, equal values are always adjacent, so one
   left-to-right pass sees every run completely.

Why it works
------------
Invariant: dummy..prev is exactly the answer for the prefix processed so
far, and prev.next is the first unprocessed node. Each step either commits
one unique node or removes one full run, preserving the invariant.

Complexity
----------
Time:  O(n), each node is visited once.
Space: O(1) extra (just pointers).
"""

from typing import List, Optional


class ListNode:
    def __init__(self, val: int = 0, next: "Optional[ListNode]" = None):
        self.val = val
        self.next = next


class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        prev = dummy
        while prev.next:
            cur = prev.next
            if cur.next and cur.next.val == cur.val:
                val = cur.val
                while cur and cur.val == val:
                    cur = cur.next
                prev.next = cur  # splice out the whole run
            else:
                prev = cur  # cur is unique, keep it
        return dummy.next


def build(values: List[int]) -> Optional[ListNode]:
    dummy = ListNode()
    tail = dummy
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def to_list(head: Optional[ListNode]) -> List[int]:
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


if __name__ == "__main__":
    import random
    from collections import Counter

    sol = Solution()
    assert to_list(sol.deleteDuplicates(build([1, 2, 3, 3, 4, 4, 5]))) == [1, 2, 5]
    assert to_list(sol.deleteDuplicates(build([1, 1, 1, 2, 3]))) == [2, 3]
    assert to_list(sol.deleteDuplicates(build([]))) == []
    assert to_list(sol.deleteDuplicates(build([1, 1]))) == []
    assert to_list(sol.deleteDuplicates(build([1, 2, 2]))) == [1]
    random.seed(82)
    for _ in range(300):
        vals = sorted(random.randint(-5, 5) for _ in range(random.randint(0, 12)))
        c = Counter(vals)
        expected = [v for v in vals if c[v] == 1]
        assert to_list(sol.deleteDuplicates(build(vals))) == expected
    print("All tests passed.")
