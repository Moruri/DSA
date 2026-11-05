"""
LeetCode 148: Sort List
Difficulty: Medium
Topic: Linked Lists / Merge Sort

Problem
-------
Given the head of a linked list, return the list sorted in ascending order.
You should sort it in O(n log n) time and (ideally) constant extra space —
though the classic top-down merge sort uses O(log n) recursion depth, which
is accepted here.

Example 1:
  Input:  4 -> 2 -> 1 -> 3
  Output: 1 -> 2 -> 3 -> 4

Example 2:
  Input:  -1 -> 5 -> 3 -> 4 -> 0
  Output: -1 -> 0 -> 3 -> 4 -> 5

Example 3:
  Input:  []
  Output: []

Approach (thought process)
--------------------------
1. Arrays get merge sort "for free" because random access makes splitting
   cheap. A singly linked list has no random access, so the hard part is
   finding the midpoint without scanning from the start every time — that
   is exactly what the slow/fast (tortoise/hare) pair does: fast advances
   two steps, slow one; when fast hits the end, slow sits on the middle.
2. Top-down plan, mirroring classic merge sort:
     a. Base case: empty list or a single node is already sorted.
     b. Find the mid with slow/fast. Cut the list there
        (prev.next = None) so the two halves are independent.
     c. Recursively sort the left half and the right half.
     d. Merge the two sorted halves into one sorted list.
3. Merging two sorted linked lists is the same linear weave used in
   "merge two sorted lists": walk both heads, always take the smaller,
   advance that pointer. A dummy head keeps the first link uniform.
4. Why cut before recursing? Without the cut, the left recursion would
   keep walking into the right half and never terminate. The cut is what
   turns one list into two smaller subproblems.

Why it works: every recursive call halves the list (modulo off-by-one),
so the recursion depth is O(log n). At each depth the merges across all
sublists together touch every node once, so each of the log n levels
costs O(n). That is the textbook merge-sort recurrence.

Complexity:
  - Time: O(n log n) — log n split levels, O(n) merge work per level.
  - Space: O(log n) for the recursion stack (top-down). A bottom-up
    variant can do O(1) extra space; we keep the clearer top-down form.
"""

from __future__ import annotations

from typing import List, Optional


class ListNode:
    def __init__(self, val: int = 0, next: Optional["ListNode"] = None) -> None:
        self.val = val
        self.next = next


class Solution:
    def sortList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None or head.next is None:
            return head

        mid = self._split_mid(head)
        left = self.sortList(head)
        right = self.sortList(mid)
        return self._merge(left, right)

    def _split_mid(self, head: ListNode) -> ListNode:
        """Cut the list in half; return the head of the second half."""
        slow: ListNode = head
        fast: ListNode = head
        prev: Optional[ListNode] = None
        while fast is not None and fast.next is not None:
            prev = slow
            slow = slow.next  # type: ignore[assignment]
            fast = fast.next.next  # type: ignore[assignment]
        # prev is the last node of the first half; slow starts the second.
        assert prev is not None
        prev.next = None
        return slow

    def _merge(
        self, a: Optional[ListNode], b: Optional[ListNode]
    ) -> Optional[ListNode]:
        dummy = ListNode(0)
        tail = dummy
        while a is not None and b is not None:
            if a.val <= b.val:
                tail.next = a
                a = a.next
            else:
                tail.next = b
                b = b.next
            tail = tail.next
        tail.next = a if a is not None else b
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
        ([4, 2, 1, 3], [1, 2, 3, 4]),
        ([-1, 5, 3, 4, 0], [-1, 0, 3, 4, 5]),
        ([], []),
        ([1], [1]),
        ([2, 1], [1, 2]),
        ([5, 4, 3, 2, 1], [1, 2, 3, 4, 5]),
        ([1, 1, 1], [1, 1, 1]),
        ([-5, -1, -3], [-5, -3, -1]),
    ]
    for values, expected in cases:
        got = _to_list(sol.sortList(_from_list(values)))
        print(f"{'OK' if got == expected else 'FAIL'}: {values} -> {got} (expected {expected})")
        assert got == expected, f"148 sortList({values}) returned {got}, expected {expected}"


if __name__ == "__main__":
    _demo()
