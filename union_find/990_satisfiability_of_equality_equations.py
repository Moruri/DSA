"""
LeetCode 990: Satisfiability of Equality Equations
Difficulty: Medium
Topic: Union-Find (Disjoint Set Union)

Problem
-------
Each string in equations looks like "a==b" or "a!=b" with lowercase
variable names. Return True if we can give every variable an integer value
so that all the equations hold.

Approach (thought process)
--------------------------
1. Equality is an equivalence relation (reflexive, symmetric, transitive):
   if a==b and b==c, then a==c. So "==" equations split the variables into
   groups that must all share one value. That is exactly what Union-Find
   builds.
2. Two passes, and the order matters:
   - Pass 1: union the two sides of every "==" equation.
   - Pass 2: for every "!=" equation, if both sides share a root they
     are forced equal, so it is a contradiction. Return False.
   If we checked "!=" while still unioning, a later "==" could merge two
   groups we had already approved as different.
3. If no "!=" is broken, give each group its own distinct number. That
   satisfies every equation, so the answer is True.
4. Note "a!=a" is caught naturally: a variable always shares its own root.

Complexity
----------
Time:  O(n * alpha(26)), basically O(n) with path compression.
Space: O(1), the parent array has 26 slots.
"""

from typing import List


class Solution:
    def equationsPossible(self, equations: List[str]) -> bool:
        parent = list(range(26))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]  # path halving
                x = parent[x]
            return x

        for eq in equations:
            if eq[1] == "=":
                a, b = ord(eq[0]) - 97, ord(eq[3]) - 97
                parent[find(a)] = find(b)

        for eq in equations:
            if eq[1] == "!":
                a, b = ord(eq[0]) - 97, ord(eq[3]) - 97
                if find(a) == find(b):
                    return False
        return True


if __name__ == "__main__":
    sol = Solution()
    assert sol.equationsPossible(["a==b", "b!=a"]) is False
    assert sol.equationsPossible(["b==a", "a==b"]) is True
    assert sol.equationsPossible(["a==b", "b==c", "a==c"]) is True
    assert sol.equationsPossible(["a==b", "b!=c", "c==a"]) is False
    assert sol.equationsPossible(["c==c", "b==d", "x!=z"]) is True
    assert sol.equationsPossible(["a!=a"]) is False
    # "!=" listed before the "==" that breaks it: two-pass order matters.
    assert sol.equationsPossible(["a!=c", "a==b", "b==c"]) is False
    print("All tests passed.")
