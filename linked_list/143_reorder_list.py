"""
LeetCode 143: Reorder List
Difficulty: Medium
Topic: Linked Lists / Fast-Slow Pointers / In-place Reversal

Problem
-------
You are given the head of a singly linked list L0 -> L1 -> ... -> Ln-1 -> Ln.
Reorder it in place to L0 -> Ln -> L1 -> Ln-1 -> L2 -> Ln-2 -> ...
You may not change node values, only the links.

Example 1:
  Input:  1 -> 2 -> 3 -> 4
  Output: 1 -> 4 -> 2 -> 3

Example 2:
  Input:  1 -> 2 -> 3 -> 4 -> 5
  Output: 1 -> 5 -> 2 -> 4 -> 3

Approach (thought process)
--------------------------
1. The easy version copies nodes into an array and walks two indices inward.
   That works, but costs O(n) extra space. The interesting question is how to
   do it with O(1) space, since a singly linked list can't walk backwards.
2. Look at the target order: it alternates one node from the front with one
   node from the back. "From the back, moving toward the middle" is just the
   second half of the list read in reverse. So the problem splits into three
   classic linked-list moves:
     a. Find the middle with slow/fast pointers (fast moves 2, slow moves 1;
        when fast runs out, slow sits at the end of the first half).
     b. Cut the list there and reverse the second half in place.
     c. Weave the two halves together: take one from the first, one from the
        reversed second, and repeat.
3. Picking the middle: start slow and fast both at head and loop while
   fast.next and fast.next.next exist. For 1-2-3-4 slow stops at 2, so the
   halves are [1,2] and [3,4]; for 1-2-3-4-5 slow stops at 3, giving [1,2,3]
   and [4,5]. The first half is always the same length or one longer, which
   is exactly what the weave needs (the extra middle node ends up last).
4. Weaving: save first.next and second.next before rewiring, point
   first -> second -> (old first.next), then advance both. Stop when the
   second half runs out; the first half's tail is already correct because we
   cut the list at the middle (slow.next = None).

Why it works: after the cut and the reversal, the first half lists L0, L1, ...
in order and the reversed second half lists Ln, Ln-1, ... in order. Taking
them alternately produces exactly L0, Ln, L1, Ln-1, ...

Complexity: O(n) time (three linear passes), O(1) extra space.
"""

from __future__ import annotations

from typing import List, Optional


class ListNode:
    def __init__(self, val: int = 0, next: Optional["ListNode"] = None) -> None:
        self.val = val
        self.next = next


class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        """Reorder the list in place; returns nothing, like the LeetCode signature."""
        if head is None or head.next is None:
            return

        # a. Find the end of the first half.
        slow = fast = head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next

        # b. Cut, then reverse the second half.
        second = slow.next
        slow.next = None
        prev: Optional[ListNode] = None
        while second:
            nxt = second.next
            second.next = prev
            prev = second
            second = nxt
        second = prev

        # c. Weave the halves together.
        first = head
        while second:
            first_next, second_next = first.next, second.next
            first.next = second
            second.next = first_next
            first, second = first_next, second_next


def _build(values: List[int]) -> Optional[ListNode]:
    dummy = ListNode()
    tail = dummy
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def _to_list(head: Optional[ListNode]) -> List[int]:
    out: List[int] = []
    while head:
        out.append(head.val)
        head = head.next
    return out


def _reference(values: List[int]) -> List[int]:
    out: List[int] = []
    i, j = 0, len(values) - 1
    while i <= j:
        out.append(values[i])
        if i != j:
            out.append(values[j])
        i += 1
        j -= 1
    return out


def _demo() -> None:
    sol = Solution()
    cases = [
        ([1, 2, 3, 4], [1, 4, 2, 3]),
        ([1, 2, 3, 4, 5], [1, 5, 2, 4, 3]),
        ([1], [1]),
        ([1, 2], [1, 2]),
        ([1, 2, 3], [1, 3, 2]),
    ]
    for values, expected in cases:
        head = _build(values)
        sol.reorderList(head)
        got = _to_list(head)
        status = "OK" if got == expected else "FAIL"
        print(f"{status}: reorderList({values}) -> {got} (expected {expected})")
        assert got == expected, f"143 returned {got} for {values}, expected {expected}"

    for n in range(0, 30):
        values = list(range(n))
        head = _build(values)
        sol.reorderList(head)
        assert _to_list(head) == _reference(values), n
    print("OK: lengths 0..29 match the two-index reference")


if __name__ == "__main__":
    _demo()
