"""
LeetCode 137: Single Number II
Difficulty: Medium
Topic: Bit Manipulation / Per-bit Counting (mod-3 state machine)

Problem
-------
Given an integer array nums where every element appears exactly three times
except for one element which appears exactly once, find that single element.
You must run in linear time and use only constant extra space.
Constraints: 1 <= len(nums) <= 3 * 10^4, -2^31 <= nums[i] <= 2^31 - 1.

Example 1:
  Input:  nums = [2, 2, 3, 2]
  Output: 3

Example 2:
  Input:  nums = [0, 1, 0, 1, 0, 1, 99]
  Output: 99

Approach (thought process)
--------------------------
1. The famous cousin (LeetCode 136, everything appears twice) is solved by
   XOR-ing everything: pairs cancel because x ^ x = 0. Here triples don't
   cancel under XOR (x ^ x ^ x = x), so we need a different "cancel" rule.
2. Look at one bit position at a time. For bit k, count how many numbers
   have that bit set. Every tripled number contributes 0 or 3 to that count,
   so count % 3 is exactly bit k of the lone number. That alone gives an
   easy O(32 n) solution: rebuild the answer bit by bit.
3. Can we do all 32 bit positions at once? A counter that goes 0 -> 1 -> 2
   -> 0 needs two bits of state per position. Keep two integers:
     ones = positions whose count is currently 1 (mod 3)
     twos = positions whose count is currently 2 (mod 3)
   Every integer holds the state of all 32 positions in parallel.
4. Processing a number x (its set bits are the positions that tick):
     ones = (ones ^ x) & ~twos
     twos = (twos ^ x) & ~ones      # uses the NEW ones
   Check a single position that ticks:
     state 0 (ones=0, twos=0): ones becomes 1, twos stays 0  -> state 1
     state 1 (ones=1, twos=0): ones flips to 0, twos becomes 1 -> state 2
     state 2 (ones=0, twos=1): ones blocked by twos (stays 0),
                               twos flips to 0              -> state 0
   Positions where x has a 0 bit are untouched. So it's a mod-3 counter.
5. After all numbers, every tripled value has wrapped back to state 0, and
   the lone value left its bits in state 1, so the answer is `ones`.
6. Python wrinkle: ints are unbounded, but the state-machine trick still
   works because negative numbers just behave like infinitely many leading
   1 bits ticking together. The per-bit counting version needs an explicit
   32-bit sign fix-up, shown in `singleNumberBitCount` for comparison.

Why it works: the operations treat every bit position independently, and
each position runs a correct counter modulo 3; counts that are multiples of
3 end at 0, and the lone number's bits end at 1.

Complexity: O(n) time, O(1) extra space (two integers).
"""

from __future__ import annotations

from typing import List


class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        """Two-integer mod-3 counter running on all bit positions at once."""
        ones = twos = 0
        for x in nums:
            ones = (ones ^ x) & ~twos
            twos = (twos ^ x) & ~ones
        return ones

    def singleNumberBitCount(self, nums: List[int]) -> int:
        """Easier-to-derive version: count each of the 32 bits modulo 3."""
        result = 0
        for k in range(32):
            count = sum((x >> k) & 1 for x in nums)
            if count % 3:
                result |= 1 << k
        # Bit 31 set means the answer is negative in 32-bit two's complement.
        if result >= 1 << 31:
            result -= 1 << 32
        return result


def _demo() -> None:
    import random

    sol = Solution()
    cases = [
        ([2, 2, 3, 2], 3),
        ([0, 1, 0, 1, 0, 1, 99], 99),
        ([-2, -2, 1, 1, 4, 1, 4, 4, -4, -2], -4),
        ([7], 7),
        ([-(2**31), 5, 5, 5], -(2**31)),
        ([2**31 - 1, -1, -1, -1], 2**31 - 1),
    ]
    for nums, expected in cases:
        for name, fn in (("state machine", sol.singleNumber), ("bit count", sol.singleNumberBitCount)):
            got = fn(nums)
            status = "OK" if got == expected else "FAIL"
            print(f"{status}: {name} {nums} -> {got} (expected {expected})")
            assert got == expected, f"137 {name} returned {got} for {nums}, expected {expected}"

    rng = random.Random(137)
    for _ in range(300):
        pool = rng.sample(range(-(2**31), 2**31), rng.randint(1, 12))
        lone, triples = pool[0], pool[1:]
        nums = [lone] + triples * 3
        rng.shuffle(nums)
        assert sol.singleNumber(nums) == lone
        assert sol.singleNumberBitCount(nums) == lone
    print("OK: 300 random arrays agree on both approaches")


if __name__ == "__main__":
    _demo()
