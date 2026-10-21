"""
LeetCode 138: Copy List with Random Pointer
Difficulty: Medium
Topic: Linked Lists / Interleaving (hash map alternative)

Problem
-------
Each node in a linked list has a `next` pointer and a `random` pointer that
can point to any node in the list or to None. Return a deep copy: brand-new
nodes whose next and random pointers mirror the original structure, with no
pointer into the original list.

Example:
  Input:  [[7,null],[13,0],[11,4],[10,2],[1,0]]   ([val, random_index])
  Output: the same shape, built from new nodes.

Approach (thought process)
--------------------------
1. The hard part is `random`: when we copy node A, the node its random points
   to may not have a copy yet. So we need a way to go from "original node" to
   "its copy" at any moment.
2. Easiest version: a hash map old -> new. Pass 1 creates every copy; pass 2
   wires copy.next = map[old.next] and copy.random = map[old.random].
   O(n) time, O(n) extra space.
3. O(1)-space trick: store the mapping inside the list itself. Weave each copy
   right after its original: A -> A' -> B -> B' -> ...
   Now "copy of X" is simply X.next.
   - Pass 1: insert A' after every A.
   - Pass 2: A'.random = A.random.next (the copy sitting after A's target).
   - Pass 3: unzip the two lists, restoring the original's next pointers.
4. Restoring the original matters: the problem says don't modify the input
   (in spirit), and the tests below check that.

Complexity: O(n) time, O(1) extra space (beyond the output list).
"""

from __future__ import annotations

from typing import List, Optional


class Node:
    def __init__(self, x: int, next: "Node | None" = None,
                 random: "Node | None" = None):
        self.val = int(x)
        self.next = next
        self.random = random


class Solution:
    def copyRandomList(self, head: Optional[Node]) -> Optional[Node]:
        if head is None:
            return None

        # Pass 1: weave copies in. A -> A' -> B -> B' ...
        cur = head
        while cur:
            cur.next = Node(cur.val, cur.next)
            cur = cur.next.next

        # Pass 2: copy random pointers via the "copy is next" rule.
        cur = head
        while cur:
            if cur.random:
                cur.next.random = cur.random.next
            cur = cur.next.next

        # Pass 3: unzip into original and copy.
        new_head = head.next
        cur = head
        while cur:
            copy = cur.next
            cur.next = copy.next
            copy.next = copy.next.next if copy.next else None
            cur = cur.next
        return new_head


def build(spec: List[List[Optional[int]]]) -> Optional[Node]:
    nodes = [Node(v) for v, _ in spec]
    for i, (_, r) in enumerate(spec):
        if i + 1 < len(nodes):
            nodes[i].next = nodes[i + 1]
        nodes[i].random = nodes[r] if r is not None else None
    return nodes[0] if nodes else None


def dump(head: Optional[Node]) -> List[List[Optional[int]]]:
    nodes = []
    cur = head
    while cur:
        nodes.append(cur)
        cur = cur.next
    index = {id(n): i for i, n in enumerate(nodes)}
    return [[n.val, index[id(n.random)] if n.random else None] for n in nodes]


def _ids(head: Optional[Node]) -> set:
    out = set()
    while head:
        out.add(id(head))
        head = head.next
    return out


if __name__ == "__main__":
    s = Solution()
    cases = [
        [[7, None], [13, 0], [11, 4], [10, 2], [1, 0]],
        [[1, 1], [2, 1]],
        [[3, None], [3, 0], [3, None]],
        [],
    ]

    import random

    for _ in range(300):
        n = random.randint(0, 12)
        cases.append([[random.randint(-50, 50),
                       random.choice([None] + list(range(n)))]
                      for _ in range(n)])

    for spec in cases:
        head = build(spec)
        copy = s.copyRandomList(head)
        assert dump(copy) == spec, spec
        assert dump(head) == spec, "original list was not restored"
        assert not (_ids(head) & _ids(copy)), "copy shares nodes"
    print("All tests passed.")
