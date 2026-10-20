"""
LeetCode 45: Jump Game II
Difficulty: Medium
Topic: Greedy / Implicit BFS

Problem
-------
You start at index 0 of `nums`. From index i you may jump forward to any
index in [i + 1, i + nums[i]]. Return the minimum number of jumps needed to
reach the last index. The input guarantees the last index is reachable.

Example 1:
  Input:  nums = [2, 3, 1, 1, 4]
  Output: 2   (0 -> 1 -> 4)

Example 2:
  Input:  nums = [2, 3, 0, 1, 4]
  Output: 2

Approach (thought process)
--------------------------
1. The obvious DP, "fewest jumps to reach i", looks back over every earlier
   index and costs O(n^2). We can do better by thinking in rounds.
2. Treat it as BFS without building a graph. Round 0 is just index 0. Every
   index reachable with k jumps forms a contiguous block [start, end], because
   if you can land at index j you can also land on anything before it.
3. While scanning the current block, track `farthest`, the furthest index any
   of its positions can reach. That's the right edge of the next block.
4. When the scan hits `end` (the edge of the current block), we're forced to
   spend one more jump, and the new edge becomes `farthest`. Stop as soon as
   the edge covers the last index.
5. Why greedy is safe: we never commit to a specific landing spot, we only
   count how many rounds it takes for the reachable block to cover the end,
   which is exactly the BFS distance.

Complexity: O(n) time, one pass. O(1) extra space.
"""

from __future__ import annotations

from typing import List


class Solution:
    def jump(self, nums: List[int]) -> int:
        jumps = 0
        end = 0        # last index reachable with `jumps` jumps
        farthest = 0   # furthest index reachable with `jumps + 1` jumps
        for i in range(len(nums) - 1):
            farthest = max(farthest, i + nums[i])
            if i == end:
                jumps += 1
                end = farthest
                if end >= len(nums) - 1:
                    break
        return jumps


def _dp(nums: List[int]) -> float:
    n = len(nums)
    best = [float("inf")] * n
    best[0] = 0
    for i in range(n):
        for j in range(i + 1, min(n, i + nums[i] + 1)):
            best[j] = min(best[j], best[i] + 1)
    return best[-1]


if __name__ == "__main__":
    s = Solution()
    assert s.jump([2, 3, 1, 1, 4]) == 2
    assert s.jump([2, 3, 0, 1, 4]) == 2
    assert s.jump([0]) == 0
    assert s.jump([1, 2]) == 1
    assert s.jump([1, 1, 1, 1]) == 3

    import random

    for _ in range(1000):
        n = random.randint(1, 12)
        nums = [random.randint(0, 4) for _ in range(n)]
        expected = _dp(nums)
        if expected == float("inf"):
            continue  # unreachable; problem guarantees reachability
        assert s.jump(nums) == expected, nums
    print("All tests passed.")
