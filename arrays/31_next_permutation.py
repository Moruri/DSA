"""
LeetCode 31: Next Permutation
Difficulty: Medium
Topic: Arrays / In-place Permutation

Problem
-------
Rearrange nums into the lexicographically next greater permutation, in
place with O(1) extra memory. If nums is already the largest ordering
(fully descending), rearrange it into the smallest (ascending).

Approach (thought process)
--------------------------
1. Think of the array like an odometer. To get the very next value you
   want to change the rightmost digit you can, and bump it by as little
   as possible.
2. Scan from the right while the sequence is non-increasing. That
   descending suffix is already at its maximum, so no rearrangement
   inside it can make a bigger number. The first index i with
   nums[i] < nums[i + 1] is the "pivot": the rightmost spot that can grow.
3. If no pivot exists, the whole array is descending (the last
   permutation), so reverse it to get the first one.
4. Otherwise, find the rightmost element in the suffix that is strictly
   greater than nums[i]. Because the suffix is descending, that is the
   smallest value larger than the pivot. Swap them.
5. After the swap, the suffix is still descending. Reverse it so it
   becomes ascending, i.e. the smallest possible tail.

Why it works: positions left of the pivot stay the same (changing them
would jump too far), the pivot increases by the minimum possible amount,
and the tail becomes as small as possible. That is exactly the next
permutation.

Complexity:
  - Time: O(n), at most a few linear scans.
  - Space: O(1).
"""

from itertools import permutations
from typing import List


class Solution:
    def nextPermutation(self, nums: List[int]) -> None:
        n = len(nums)
        i = n - 2
        while i >= 0 and nums[i] >= nums[i + 1]:
            i -= 1
        if i >= 0:
            j = n - 1
            while nums[j] <= nums[i]:
                j -= 1
            nums[i], nums[j] = nums[j], nums[i]
        left, right = i + 1, n - 1
        while left < right:
            nums[left], nums[right] = nums[right], nums[left]
            left += 1
            right -= 1


if __name__ == "__main__":
    s = Solution()
    for arr, want in [([1, 2, 3], [1, 3, 2]), ([3, 2, 1], [1, 2, 3]),
                      ([1, 1, 5], [1, 5, 1]), ([1], [1])]:
        s.nextPermutation(arr)
        assert arr == want, (arr, want)

    # Brute-force check: walking next permutations visits all orderings in order.
    base = [1, 2, 2, 3]
    ordered = sorted(set(permutations(base)))
    cur = sorted(base)
    for expected in ordered[1:] + ordered[:1]:
        s.nextPermutation(cur)
        assert tuple(cur) == expected, (cur, expected)
    print("All tests passed for 31 Next Permutation.")
