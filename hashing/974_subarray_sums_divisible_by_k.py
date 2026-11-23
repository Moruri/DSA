"""
LeetCode 974: Subarray Sums Divisible by K
Difficulty: Medium
Topic: Hashing / Prefix Sum (modular)

Problem
-------
Given an integer array nums and an integer k, return the number of non-empty
contiguous subarrays whose sum is divisible by k.

Approach (thought process)
--------------------------
1. Brute force checks all O(n^2) subarrays. n is up to 3 * 10^4, so we want
   one pass.
2. Prefix sums turn "sum of a subarray" into "difference of two prefixes":
   sum(nums[i:j]) = P[j] - P[i].
3. That difference is divisible by k exactly when P[j] and P[i] leave the
   same remainder mod k. So the question becomes: how many pairs of prefixes
   share a remainder?
4. Walk left to right keeping count[r] = how many prefixes seen so far have
   remainder r. At each new prefix with remainder r, every earlier prefix
   with remainder r closes a valid subarray ending here: add count[r], then
   bump count[r].
5. Seed count[0] = 1 for the empty prefix P[0] = 0, so subarrays starting at
   index 0 get counted.
6. Negative numbers: in Python, x % k is always in [0, k), so -1 % 5 == 4 and
   remainders line up. (In Java/C++ you'd need ((x % k) + k) % k.)

Why it works: each subarray corresponds to exactly one pair (i < j) of
prefix positions, and it's divisible by k iff the two remainders match. The
running count adds each matching pair once, at its right end. Same skeleton
as 560 Subarray Sum Equals K and 525 Contiguous Array -- only the hash key
changes (prefix - k there, prefix mod k here).

Complexity
----------
Time:  O(n), one pass.
Space: O(min(n, k)) for the remainder counts (a list of size k works too).
"""

from typing import List


class Solution:
    def subarraysDivByK(self, nums: List[int], k: int) -> int:
        count = [0] * k
        count[0] = 1  # empty prefix
        prefix = 0
        total = 0
        for x in nums:
            prefix = (prefix + x) % k  # Python % keeps it in [0, k)
            total += count[prefix]
            count[prefix] += 1
        return total


def brute(nums: List[int], k: int) -> int:
    n = len(nums)
    return sum(
        1
        for i in range(n)
        for j in range(i + 1, n + 1)
        if sum(nums[i:j]) % k == 0
    )


if __name__ == "__main__":
    s = Solution()
    cases = [
        ([4, 5, 0, -2, -3, 1], 5, 7),
        ([5], 9, 0),
        ([0, 0, 0], 3, 6),
        ([-1, 2, 9], 2, 2),
        ([2, -2, 2, -4], 6, 2),
    ]
    for nums, k, want in cases:
        got = s.subarraysDivByK(nums, k)
        assert got == want, (nums, k, got, want)
        print(f"subarraysDivByK({nums}, {k}) = {got}")

    import random
    random.seed(974)
    for _ in range(300):
        nums = [random.randint(-10, 10) for _ in range(random.randint(1, 12))]
        k = random.randint(2, 7)
        assert s.subarraysDivByK(nums, k) == brute(nums, k), (nums, k)
    print("random cross-check vs brute force OK")
    print("All tests passed.")
