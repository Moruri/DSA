"""
LeetCode 50: Pow(x, n)
Difficulty: Medium
Topic: Math / Fast Exponentiation (Binary Exponentiation)

Problem
-------
Implement pow(x, n), which computes x raised to the power n, where n is a
32-bit signed integer (it can be negative or zero).

Examples:
  x = 2.0,  n = 10  ->  1024.0
  x = 2.1,  n = 3   ->  9.261
  x = 2.0,  n = -2  ->  0.25

Approach (thought process)
--------------------------
1. Multiplying x by itself n times is O(n), and n can be about 2 billion, so
   that times out. We need to cut the work by halving instead of counting.
2. Key identity: x^n = (x^2)^(n/2) when n is even, and x * x^(n-1) when n is
   odd. Each squaring halves the remaining exponent.
3. Read n in binary. For n = 13 = 1101b, x^13 = x^8 * x^4 * x^1. Keep a
   running "base" that goes x, x^2, x^4, x^8, ... by squaring, and multiply it
   into the answer exactly when the current lowest bit of n is 1. Then shift
   n right by one. That is an iterative loop with no recursion.
4. Negative n: x^-n = 1 / x^n, so flip x to 1/x and make n positive. In
   Python ints never overflow, so -(-2^31) is safe (in Java/C++ you would
   widen to a 64-bit long first).
5. n = 0 falls out naturally: the loop never runs and the answer stays 1.

Why it works: every positive integer is a unique sum of powers of two, so
x^n is the product of x^(2^k) for each set bit k. The loop visits each bit
once and has the matching x^(2^k) in hand at that moment.

Complexity:
  - Time: O(log |n|), one squaring per bit.
  - Space: O(1).
"""


class Solution:
    def myPow(self, x: float, n: int) -> float:
        if n < 0:
            x, n = 1 / x, -n
        result, base = 1.0, x
        while n:
            if n & 1:          # this power of two is part of n
                result *= base
            base *= base       # x^(2^k) -> x^(2^(k+1))
            n >>= 1
        return result


if __name__ == "__main__":
    import math
    import random

    sol = Solution()
    assert math.isclose(sol.myPow(2.0, 10), 1024.0)
    assert math.isclose(sol.myPow(2.1, 3), 9.261)
    assert math.isclose(sol.myPow(2.0, -2), 0.25)
    assert sol.myPow(5.0, 0) == 1.0
    assert sol.myPow(1.0, -(2 ** 31)) == 1.0
    assert sol.myPow(-1.0, 2 ** 31 - 1) == -1.0
    assert sol.myPow(2.0, -(2 ** 31)) == 0.0  # underflows to 0 like the real pow

    rng = random.Random(50)
    for _ in range(2000):
        x = rng.uniform(-3, 3) or 1.5
        n = rng.randint(-30, 30)
        assert math.isclose(sol.myPow(x, n), x ** n, rel_tol=1e-9, abs_tol=1e-12), (x, n)
    print("All tests passed for 50.")
