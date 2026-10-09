"""
LeetCode 297: Serialize and Deserialize Binary Tree
Difficulty: Hard
Topic: Trees / DFS (preorder with null markers)

Problem
-------
Design an algorithm to turn a binary tree into a string (serialize) and turn
that string back into the identical tree (deserialize). The format is up to
you; it only has to round-trip.

Example:
  Input tree:      1
                  / \
                 2   3
                    / \
                   4   5
  serialize   -> "1,2,#,#,3,4,#,#,5,#,#"
  deserialize -> the same tree

Approach (thought process)
--------------------------
1. Why a plain traversal isn't enough: preorder [1, 2, 3] alone could be a
   left chain, a right chain, or a balanced tree. That's why problem 105
   needed both preorder and inorder. The missing information is "where are
   the empty children?"
2. So write the empty children down too. Do a preorder DFS and emit a marker
   ("#") every time we hit None. Now the string describes the shape exactly:
   every node is followed by its full left subtree, then its full right
   subtree, and each subtree ends at its "#" leaves.
3. Deserializing mirrors serializing. Read tokens left to right with an
   iterator. Take a token: if it's "#", return None. Otherwise make a node,
   then recursively build its left child from the next tokens, then its
   right child. The recursion consumes exactly the tokens the serializer
   produced for that subtree, so it lines up automatically with no indices.
4. Values can be negative or multi-digit, so join with commas rather than
   gluing characters together.

Why it works: a preorder walk with explicit null markers is a unique
encoding. A tree with k nodes produces k values and k + 1 markers, and the
decoder replays the same recursive decisions in the same order.

Implementation note: deep, skinny trees (up to 10^4 nodes) can blow past
Python's default recursion limit, so both directions below use an explicit
stack instead of recursion. The logic is identical to the recursive version.

Complexity: O(n) time and O(n) space for both serialize and deserialize.
"""

from __future__ import annotations

from typing import List, Optional


class TreeNode:
    def __init__(self, x: int) -> None:
        self.val = x
        self.left: Optional["TreeNode"] = None
        self.right: Optional["TreeNode"] = None


class Codec:
    NULL = "#"

    def serialize(self, root: Optional[TreeNode]) -> str:
        out: List[str] = []
        stack: List[Optional[TreeNode]] = [root]
        while stack:
            node = stack.pop()
            if node is None:
                out.append(self.NULL)
                continue
            out.append(str(node.val))
            # Push right first so left is processed first (preorder).
            stack.append(node.right)
            stack.append(node.left)
        return ",".join(out)

    def deserialize(self, data: str) -> Optional[TreeNode]:
        tokens = data.split(",")
        if not tokens or tokens[0] == self.NULL:
            return None
        root = TreeNode(int(tokens[0]))
        # Each stack entry is a node still waiting for a child; the flag says
        # whether its left child has already been filled in.
        stack: List[List] = [[root, False]]
        for tok in tokens[1:]:
            node = None if tok == self.NULL else TreeNode(int(tok))
            parent = stack[-1]
            if not parent[1]:
                parent[0].left = node
                parent[1] = True
            else:
                parent[0].right = node
                stack.pop()  # both children assigned
            if node is not None:
                stack.append([node, False])
        return root


def _from_level(values: List[Optional[int]]) -> Optional[TreeNode]:
    if not values or values[0] is None:
        return None
    nodes = [None if v is None else TreeNode(v) for v in values]
    kids = iter(nodes[1:])
    for node in nodes:
        if node is None:
            continue
        node.left = next(kids, None)
        node.right = next(kids, None)
    return nodes[0]


def _same(a: Optional[TreeNode], b: Optional[TreeNode]) -> bool:
    stack = [(a, b)]
    while stack:
        x, y = stack.pop()
        if x is None and y is None:
            continue
        if x is None or y is None or x.val != y.val:
            return False
        stack.append((x.left, y.left))
        stack.append((x.right, y.right))
    return True


def _demo() -> None:
    codec = Codec()
    samples = [
        [1, 2, 3, None, None, 4, 5],
        [],
        [-10],
        [1, None, 2, None, 3],
        [5, 4, 7, 3, None, 2, None, -1, None, 9],
    ]
    for values in samples:
        root = _from_level(values)
        data = codec.serialize(root)
        back = codec.deserialize(data)
        ok = _same(root, back)
        print(f"{'OK' if ok else 'FAIL'}: {values} -> {data!r}")
        assert ok

    assert codec.serialize(_from_level([1, 2, 3, None, None, 4, 5])) == "1,2,#,#,3,4,#,#,5,#,#"

    # A 10,000-node right-leaning chain: no recursion-limit crash.
    root = cur = TreeNode(0)
    for i in range(1, 10_000):
        cur.right = TreeNode(i)
        cur = cur.right
    assert _same(root, codec.deserialize(codec.serialize(root)))
    print("OK: 10,000-node skinny tree round-trips")

    import random

    rng = random.Random(297)
    for _ in range(200):
        n = rng.randint(0, 30)
        values = [rng.choice([None, rng.randint(-1000, 1000)]) if i else rng.randint(-5, 5) for i in range(n)]
        root = _from_level(values)
        assert _same(root, codec.deserialize(codec.serialize(root)))
    print("OK: 200 random trees round-trip")


if __name__ == "__main__":
    _demo()
