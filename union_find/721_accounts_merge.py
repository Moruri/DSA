"""
LeetCode 721: Accounts Merge
Difficulty: Medium
Topic: Union-Find / Grouping by Shared Keys

Problem
-------
Each account is [name, email1, email2, ...]. Two accounts belong to the same
person if they share at least one email (same name alone is NOT enough).
Merge them and return each person as [name, *sorted emails].

Example:
  [["John","a@x","b@x"], ["John","c@x","a@x"], ["Mary","m@x"], ["John","j@x"]]
  -> [["John","a@x","b@x","c@x"], ["Mary","m@x"], ["John","j@x"]]

Approach (thought process)
--------------------------
1. "Share at least one email" is a connectivity relation, and it is
   transitive through chains: A shares with B, B shares with C, so A and C
   are one person even if they share nothing directly. Chains of "same group"
   are exactly what union-find answers cheaply.
2. Make the accounts the nodes (indices 0..n-1). Walk every email and remember
   the first account that owned it. When a later account owns the same email,
   union the two accounts. Each email causes at most one union.
3. After all unions, every account's root names its person. Pour each
   account's emails into a set keyed by root, then sort the set and prefix
   the name (all accounts in a group share the name, so take the root's).
4. Path compression plus union by size keep every find nearly O(1).

Why it works: two accounts end up with the same root exactly when a chain of
shared emails connects them, which is the problem's definition of one person.

Complexity (E = total emails, n = accounts):
  - Time: O(E * alpha(n)) for unions + O(E log E) for sorting the output.
  - Space: O(E + n) for the email-owner map and the groups.
"""

from collections import defaultdict
from typing import List


class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        n = len(accounts)
        parent = list(range(n))
        size = [1] * n

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]  # path halving
                x = parent[x]
            return x

        def union(a: int, b: int) -> None:
            ra, rb = find(a), find(b)
            if ra == rb:
                return
            if size[ra] < size[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            size[ra] += size[rb]

        owner = {}  # email -> first account index seen with it
        for i, acct in enumerate(accounts):
            for email in acct[1:]:
                if email in owner:
                    union(i, owner[email])
                else:
                    owner[email] = i

        groups = defaultdict(set)
        for email, i in owner.items():
            groups[find(i)].add(email)

        return [[accounts[root][0], *sorted(emails)] for root, emails in groups.items()]


def _demo() -> None:
    sol = Solution()
    cases = [
        (
            [
                ["John", "johnsmith@mail.com", "john_newyork@mail.com"],
                ["John", "johnsmith@mail.com", "john00@mail.com"],
                ["Mary", "mary@mail.com"],
                ["John", "johnnybravo@mail.com"],
            ],
            [
                ["John", "john00@mail.com", "john_newyork@mail.com", "johnsmith@mail.com"],
                ["Mary", "mary@mail.com"],
                ["John", "johnnybravo@mail.com"],
            ],
        ),
        # Chain: A-B share x, B-C share y, so all three merge.
        (
            [["Ann", "a", "x"], ["Ann", "x", "y"], ["Ann", "y", "c"]],
            [["Ann", "a", "c", "x", "y"]],
        ),
        # Same name, no shared email: stay separate.
        ([["Bo", "p"], ["Bo", "q"]], [["Bo", "p"], ["Bo", "q"]]),
    ]
    for accounts, expected in cases:
        got = sol.accountsMerge(accounts)
        ok = sorted(got) == sorted(expected)
        print(f"{'OK' if ok else 'FAIL'}: {got}")
        assert ok, f"721 accountsMerge returned {got}, expected {expected}"


if __name__ == "__main__":
    _demo()
