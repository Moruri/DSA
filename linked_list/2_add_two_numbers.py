"""
LeetCode 2: Add Two Numbers
Difficulty: Medium
Topic: Linked Lists

Problem
-------
You are given two non-empty linked lists representing two non-negative
integers. Digits are stored in reverse order, and each node contains a
single digit. Add the two numbers and return the sum as a linked list
(also in reverse order).

You may assume the two numbers do not contain any leading zero, except
the number 0 itself.

Example 1:
  Input:  l1 = [2,4,3], l2 = [5,6,4]
  Output: [7,0,8]
  Explanation: 342 + 465 = 807.

Example 2:
  Input:  l1 = [0], l2 = [0]
  Output: [0]

Example 3:
  Input:  l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]
  Output: [8,9,9,9,0,0,0,1]

Approach (thought process)
--------------------------
1. Converting both lists to integers, adding, then rebuilding a list works
   but blows up on very long inputs (up to 100 digits) and fights the
   "linked list" framing of the problem.
2. Because digits are already least-significant-first, walk both lists in
   lockstep. At each position add the two digits plus any carry from the
   previous column, emit (sum % 10), and keep (sum // 10) as the next carry.
3. When one list ends, keep walking the other with a zero digit. After both
   are exhausted, if a carry remains, append one more node.
4. Use a dummy head so the first real digit is just another append — no
   special case for an empty result. Return dummy.next.

Complexity: O(max(m, n)) time, O(1) extra space beyond the output list
(m, n = lengths of the two inputs).
"""

from __future__ import annotations

from typing import List, Optional


class ListNode:
    def __init__(self, val: int = 0, next: Optional["ListNode"] = None) -> None:
        self.val = val
        self.next = next


class Solution:
    def addTwoNumbers(
        self, l1: Optional[ListNode], l2: Optional[ListNode]
    ) -> Optional[ListNode]:
        """Add two reverse-order digit lists; return the sum as a list."""
        dummy = ListNode(0)
        tail = dummy
        carry = 0

        while l1 is not None or l2 is not None or carry:
            v1 = l1.val if l1 is not None else 0
            v2 = l2.val if l2 is not None else 0
            total = v1 + v2 + carry
            carry = total // 10
            tail.next = ListNode(total % 10)
            tail = tail.next
            if l1 is not None:
                l1 = l1.next
            if l2 is not None:
                l2 = l2.next

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
        ([2, 4, 3], [5, 6, 4], [7, 0, 8]),
        ([0], [0], [0]),
        ([9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 9], [8, 9, 9, 9, 0, 0, 0, 1]),
        ([1], [9, 9], [0, 0, 1]),
        ([5], [5], [0, 1]),
    ]
    for a, b, expected in cases:
        got = _to_list(sol.addTwoNumbers(_from_list(a), _from_list(b)))
        status = "OK" if got == expected else "FAIL"
        print(f"{status}: {a} + {b} -> {got} (expected {expected})")
        assert got == expected, f"2 addTwoNumbers({a}, {b}) returned {got}, expected {expected}"


if __name__ == "__main__":
    _demo()
