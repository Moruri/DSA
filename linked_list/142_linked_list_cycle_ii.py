"""
LeetCode 142: Linked List Cycle II
Difficulty: Medium
Topic: Linked Lists / Floyd's Tortoise and Hare

Problem
-------
Given the head of a linked list, return the node where the cycle begins, or
None if there is no cycle. Do not modify the list; aim for O(1) extra memory.

Approach (thought process)
--------------------------
1. The easy answer is a set of visited nodes: the first node seen twice is
   the cycle start. That's O(n) memory, and the follow-up asks for O(1).
2. Phase 1, detect: move `slow` one step and `fast` two steps. If there is no
   cycle, `fast` falls off the end. If there is one, `fast` gains one node per
   step inside the loop, so it must land on `slow` eventually.
3. Phase 2, locate: let a = distance from head to cycle start, b = distance
   from cycle start to the meeting point, L = cycle length. When they meet,
   fast has walked twice as far as slow: 2(a + b) = a + b + kL, so
   a + b = kL, which means a = kL - b. Walking `a` steps from the meeting
   point brings you to the cycle start (kL - b steps around the loop from
   b lands on 0).
4. So reset one pointer to head and step both one node at a time. After
   exactly `a` steps they meet, and that node is the cycle entrance.

Complexity
----------
Time:  O(n)  -- each phase walks at most a constant number of laps.
Space: O(1)  -- two pointers, no visited set.
"""

from typing import List, Optional


class ListNode:
    def __init__(self, val: int = 0, next: "Optional[ListNode]" = None):
        self.val = val
        self.next = next


class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                # Phase 2: a = kL - b, so equal-speed walkers meet at the entrance.
                finder = head
                while finder is not slow:
                    finder = finder.next
                    slow = slow.next
                return finder
        return None


def build(values: List[int], pos: int) -> Optional[ListNode]:
    """Build a list; tail links back to index `pos` (-1 means no cycle)."""
    if not values:
        return None
    nodes = [ListNode(v) for v in values]
    for x, y in zip(nodes, nodes[1:]):
        x.next = y
    if pos >= 0:
        nodes[-1].next = nodes[pos]
    return nodes[0]


def index_of(head: Optional[ListNode], target: Optional[ListNode]) -> int:
    if target is None:
        return -1
    i, node = 0, head
    while node is not target:
        node, i = node.next, i + 1
    return i


if __name__ == "__main__":
    s = Solution()
    cases = [
        ([3, 2, 0, -4], 1),
        ([1, 2], 0),
        ([1], -1),
        ([1], 0),
        ([], -1),
        ([1, 2, 3, 4, 5, 6, 7], 3),
        ([1, 2, 3, 4, 5], -1),
    ]
    for values, pos in cases:
        head = build(values, pos)
        got = index_of(head, s.detectCycle(head))
        assert got == pos, (values, pos, got)
        print(f"values={values}, pos={pos} -> cycle starts at index {got}")
    print("All tests passed.")
