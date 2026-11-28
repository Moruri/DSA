"""LeetCode 907 - Sum of Subarray Minimums (Medium)

Thought process:
1. Brute force enumerates all O(n^2) subarrays and their minimums. Flip the view:
   instead of asking "what is the min of each subarray?", ask "for how many
   subarrays is arr[i] the minimum?" -- then answer = sum(arr[i] * count_i).
2. arr[i] is the min of every subarray that starts after the previous smaller
   element and ends before the next smaller element. If left = i - prev_less and
   right = next_less - i, arr[i] owns left * right subarrays.
3. Ties: break them asymmetrically (strictly-less on one side, less-or-equal on
   the other) so a subarray with duplicate minimums is counted exactly once.
4. A monotonic increasing stack finds both boundaries in one pass: when a value
   is popped, the element doing the popping is its next-smaller-or-equal, and
   the element now on top of the stack is its previous-strictly-smaller.

Complexity: O(n) time (each index pushed/popped once), O(n) space.
"""
from typing import List

MOD = 10**9 + 7


def sum_subarray_mins(arr: List[int]) -> int:
    total = 0
    stack: List[int] = []  # indices with increasing values
    # One extra step past the end (value -inf) flushes the stack.
    for i in range(len(arr) + 1):
        cur = arr[i] if i < len(arr) else float("-inf")
        while stack and arr[stack[-1]] >= cur:
            mid = stack.pop()
            left = mid - (stack[-1] if stack else -1)
            right = i - mid
            total += arr[mid] * left * right
        stack.append(i)
    return total % MOD


def _brute(arr: List[int]) -> int:
    return sum(min(arr[i : j + 1]) for i in range(len(arr)) for j in range(i, len(arr))) % MOD


if __name__ == "__main__":
    import random

    assert sum_subarray_mins([3, 1, 2, 4]) == 17
    assert sum_subarray_mins([11, 81, 94, 43, 3]) == 444
    assert sum_subarray_mins([2, 2, 2]) == 12
    for _ in range(300):
        a = [random.randint(1, 6) for _ in range(random.randint(1, 9))]
        assert sum_subarray_mins(a) == _brute(a), a
    print("907 Sum of Subarray Minimums: all tests passed")
