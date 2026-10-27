"""
LeetCode 25: Reverse Nodes in k-Group
Difficulty: Hard
Topic: Linked Lists / In-place Reversal

Problem
-------
Given the head of a linked list, reverse the nodes k at a time and return the
new head. If the number of nodes left at the end is less than k, leave them
as they are. Only pointers may change, not node values.

Example:
  Input:  1 -> 2 -> 3 -> 4 -> 5, k = 2
  Output: 2 -> 1 -> 4 -> 3 -> 5

Approach (thought process)
--------------------------
1. This is "reverse a linked list" (the three-pointer prev/cur/next dance)
   applied to one window at a time. The hard part is the stitching: each
   reversed group must hook onto the tail of the previous group and onto the
   start of the next one.
2. A dummy node in front of the head removes the "first group is special"
   case. Keep `group_prev`, the node sitting just before the current group.
3. Before reversing, walk k steps from group_prev to find the group's last
   node (`kth`). If we run out of nodes first, the tail is short: stop and
   leave it alone. Checking first is what keeps the short tail untouched.
4. Reverse the k nodes with prev initialised to `kth.next` (the start of the
   next group). That way the old first node, which becomes the group's tail,
   automatically points at the next group when the reversal ends.
5. Stitch: group_prev.next = kth (the new front), and the old first node is
   the new group_prev for the next round.

Why it works: every group is reversed exactly once, and the invariant
"group_prev is the tail of the already-finished prefix" holds after each
round.

Complexity: O(n) time (each node is visited twice: once by the k-step probe,
once by the reversal), O(1) extra space.
"""

from __future__ import annotations

from typing import List, Optional


class ListNode:
    def __init__(self, val: int = 0, next: "ListNode | None" = None):
        self.val = val
        self.next = next


class Solution:
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        group_prev = dummy

        while True:
            # Probe: find the k-th node of this group, or stop if too short.
            kth = group_prev
            for _ in range(k):
                kth = kth.next
                if kth is None:
                    return dummy.next

            group_next = kth.next
            first = group_prev.next

            # Reverse first..kth; prev starts at group_next so the new tail
            # is already linked to the rest of the list.
            prev, cur = group_next, first
            while cur is not group_next:
                nxt = cur.next
                cur.next = prev
                prev, cur = cur, nxt

            # Stitch the reversed group behind the finished prefix.
            group_prev.next = kth
            group_prev = first


def build(vals: List[int]) -> Optional[ListNode]:
    dummy = ListNode()
    cur = dummy
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def to_list(head: Optional[ListNode]) -> List[int]:
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


def brute(vals: List[int], k: int) -> List[int]:
    out = []
    full = len(vals) - len(vals) % k
    for i in range(0, full, k):
        out.extend(reversed(vals[i:i + k]))
    return out + vals[full:]


if __name__ == "__main__":
    s = Solution()
    assert to_list(s.reverseKGroup(build([1, 2, 3, 4, 5]), 2)) == [2, 1, 4, 3, 5]
    assert to_list(s.reverseKGroup(build([1, 2, 3, 4, 5]), 3)) == [3, 2, 1, 4, 5]
    assert to_list(s.reverseKGroup(build([1]), 1)) == [1]

    import random

    for _ in range(500):
        n = random.randint(1, 20)
        k = random.randint(1, n)
        vals = [random.randint(-9, 9) for _ in range(n)]
        assert to_list(s.reverseKGroup(build(vals), k)) == brute(vals, k), (vals, k)
    print("All tests passed.")
