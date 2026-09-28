"""
LeetCode 19: Remove Nth Node From End of List
Difficulty: Medium
Topic: Linked Lists / Two Pointers

Problem
-------
Given the head of a linked list, remove the nth node from the end of the
list and return its head.

Example 1:
  Input:  head = [1, 2, 3, 4, 5], n = 2
  Output: [1, 2, 3, 5]

Example 2:
  Input:  head = [1], n = 1
  Output: []

Example 3:
  Input:  head = [1, 2], n = 1
  Output: [1]

Approach (thought process)
--------------------------
1. A first pass that counts length, then a second that walks to
   (length - n) works, but two pointer passes are unnecessary when a
   fixed gap can locate the victim in one traversal.
2. Keep two pointers with a gap of n nodes between them. Advance `fast`
   n steps first. Then advance `slow` and `fast` together until `fast`
   reaches the end — `slow` now sits just before the node to delete.
3. A dummy head in front of the real list lets the same unlink logic
   handle removing the original head (when n equals the list length):
   `slow` starts on the dummy, and we return `dummy.next`.
4. After the joint walk, `slow.next` is the nth-from-end node; skip it
   with `slow.next = slow.next.next`.

Complexity: O(L) time (one pass), O(1) extra space (L = list length).
"""

from __future__ import annotations

from typing import List, Optional


class ListNode:
    def __init__(self, val: int = 0, next: Optional["ListNode"] = None) -> None:
        self.val = val
        self.next = next


class Solution:
    def removeNthFromEnd(
        self, head: Optional[ListNode], n: int
    ) -> Optional[ListNode]:
        """Remove the nth node from the end; return the new head."""
        dummy = ListNode(0, head)
        slow: ListNode = dummy
        fast: Optional[ListNode] = dummy

        for _ in range(n):
            assert fast is not None
            fast = fast.next

        while fast is not None and fast.next is not None:
            assert slow.next is not None
            slow = slow.next
            fast = fast.next

        assert slow.next is not None
        slow.next = slow.next.next
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
        ([1, 2, 3, 4, 5], 2, [1, 2, 3, 5]),
        ([1], 1, []),
        ([1, 2], 1, [1]),
        ([1, 2], 2, [2]),
        ([1, 2, 3], 3, [2, 3]),
        ([1, 2, 3, 4, 5], 1, [1, 2, 3, 4]),
        ([1, 2, 3, 4, 5], 5, [2, 3, 4, 5]),
    ]
    for values, n, expected in cases:
        got = _to_list(sol.removeNthFromEnd(_from_list(values), n))
        status = "OK" if got == expected else "FAIL"
        print(f"{status}: removeNthFromEnd({values}, {n}) -> {got} (expected {expected})")
        assert got == expected, (
            f"19 removeNthFromEnd({values}, {n}) returned {got}, expected {expected}"
        )


if __name__ == "__main__":
    _demo()
