"""
LeetCode 1658: Minimum Operations to Reduce X to Zero
Difficulty: Medium
Topic: Sliding Window / Complement Trick

Problem
-------
Each operation removes the leftmost or rightmost element of nums and
subtracts it from x. Return the minimum number of operations to make x
exactly 0, or -1 if impossible. All nums[i] >= 1.

Approach (thought process)
--------------------------
1. Removing from both ends feels like a two-sided search (take k from the
   left, the rest from the right) -- awkward to explore directly.
2. Flip the view: whatever we remove is a prefix plus a suffix, so what we
   KEEP is one contiguous middle subarray. Its sum must be
   target = sum(nums) - x.
3. Fewest removals <=> longest kept subarray with sum exactly target.
4. Because every value is positive, the window sum grows when the right edge
   moves and shrinks when the left edge moves, so a classic variable-size
   sliding window finds every subarray with sum == target.
5. Answer = n - longest window, or -1 if no window hits target.
   Edge cases: target < 0 -> impossible; target == 0 -> keep nothing,
   remove all n (the empty window has length 0 and is handled naturally).

Why it works: positivity means that for a fixed right edge, the window sum is
strictly decreasing as the left edge advances, so shrinking while
sum > target never skips a valid window.

Complexity
----------
Time:  O(n) -- each index enters and leaves the window at most once.
Space: O(1).
"""

from typing import List


class Solution:
    def minOperations(self, nums: List[int], x: int) -> int:
        target = sum(nums) - x
        if target < 0:
            return -1
        n = len(nums)
        best = -1          # longest kept window with sum == target
        left = 0
        window = 0
        for right, v in enumerate(nums):
            window += v
            while window > target:
                window -= nums[left]
                left += 1
            if window == target:
                best = max(best, right - left + 1)
        if target == 0:
            best = max(best, 0)
        return -1 if best == -1 else n - best


def brute(nums: List[int], x: int) -> int:
    n = len(nums)
    ans = -1
    for l in range(n + 1):          # take l from the left
        for r in range(n - l + 1):  # take r from the right
            if sum(nums[:l]) + sum(nums[n - r:] if r else []) == x:
                if ans == -1 or l + r < ans:
                    ans = l + r
    return ans


if __name__ == "__main__":
    s = Solution()
    cases = [
        ([1, 1, 4, 2, 3], 5, 2),
        ([5, 6, 7, 8, 9], 4, -1),
        ([3, 2, 20, 1, 1, 3], 10, 5),
        ([1, 1], 3, -1),
        ([5], 5, 1),
    ]
    for nums, x, want in cases:
        got = s.minOperations(nums, x)
        assert got == want, (nums, x, got, want)
        print(f"minOperations({nums}, {x}) = {got}")

    import random
    random.seed(1658)
    for _ in range(500):
        nums = [random.randint(1, 6) for _ in range(random.randint(1, 8))]
        x = random.randint(1, 30)
        assert s.minOperations(nums, x) == brute(nums, x), (nums, x)
    print("random cross-check vs brute force OK")
    print("All tests passed.")
