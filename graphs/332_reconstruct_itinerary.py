"""
LeetCode 332: Reconstruct Itinerary
Difficulty: Hard
Topic: Graphs / Eulerian Path (Hierholzer's algorithm)

Problem
-------
You get a list of airline tickets [from, to]. Use every ticket exactly once
to build an itinerary that starts at "JFK". If several valid itineraries
exist, return the one that is smallest in lexical order. At least one valid
itinerary is guaranteed.

Example:
  [["MUC","LHR"],["JFK","MUC"],["SFO","SJC"],["LHR","SFO"]]
  -> ["JFK","MUC","LHR","SFO","SJC"]

Approach (thought process)
--------------------------
1. "Use every edge exactly once" is the definition of an Eulerian path, so
   this is not a shortest-path or plain DFS problem. Cities are nodes,
   tickets are directed edges (duplicates allowed).
2. The greedy idea "always fly to the smallest next city" almost works but
   can strand you: you might take a dead-end edge early while other tickets
   are still unused. Example: JFK->KUL, JFK->NRT, NRT->JFK. Greedy goes to
   KUL first and gets stuck.
3. Hierholzer's fix: do the greedy DFS anyway, but add a city to the answer
   only after all of its outgoing tickets are used up (post-order). A dead
   end like KUL finishes first, so it lands at the end of the route, which
   is exactly where a dead end belongs. Reverse the post-order list at the
   end to get the itinerary.
4. To make "smallest next city" cheap, sort each adjacency list in reverse
   and pop from the end, so each pop gives the lexically smallest remaining
   destination in O(1).
5. An explicit stack replaces recursion: peek at the top city; if it still
   has tickets, fly one; if not, pop it into the route.

Complexity: O(E log E) time for the sort, O(E) for the walk itself;
O(E) space for the graph, stack and route.
"""

from __future__ import annotations

from collections import defaultdict
from typing import List


class Solution:
    def findItinerary(self, tickets: List[List[str]]) -> List[str]:
        graph: dict[str, list[str]] = defaultdict(list)
        for src, dst in sorted(tickets, reverse=True):
            graph[src].append(dst)  # reverse-sorted, so pop() gives smallest

        route: list[str] = []
        stack = ["JFK"]
        while stack:
            city = stack[-1]
            if graph[city]:
                stack.append(graph[city].pop())
            else:
                route.append(stack.pop())  # all tickets out of city used
        return route[::-1]


if __name__ == "__main__":
    s = Solution()
    cases = [
        ([["MUC", "LHR"], ["JFK", "MUC"], ["SFO", "SJC"], ["LHR", "SFO"]],
         ["JFK", "MUC", "LHR", "SFO", "SJC"]),
        ([["JFK", "SFO"], ["JFK", "ATL"], ["SFO", "ATL"], ["ATL", "JFK"], ["ATL", "SFO"]],
         ["JFK", "ATL", "JFK", "SFO", "ATL", "SFO"]),
        ([["JFK", "KUL"], ["JFK", "NRT"], ["NRT", "JFK"]],
         ["JFK", "NRT", "JFK", "KUL"]),
    ]
    for tickets, expected in cases:
        got = s.findItinerary(tickets)
        assert got == expected, (tickets, got, expected)
        print(got)
    print("All tests passed.")
