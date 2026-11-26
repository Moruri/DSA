"""
LeetCode 166: Fraction to Recurring Decimal
Difficulty: Medium
Topic: Math / Long Division + Remainder Memo

Problem
-------
Given integers numerator and denominator, return the fraction as a string.
If the fractional part repeats, wrap the repeating part in parentheses,
e.g. 2/3 -> "0.(6)", 4/333 -> "0.(012)".

Approach (thought process)
--------------------------
1. Do grade-school long division. The integer part is |num| // |den|; the
   fractional digits come from repeatedly doing remainder *= 10,
   digit = remainder // den, remainder %= den.
2. The key insight: the next digit depends ONLY on the current remainder.
   So the moment a remainder repeats, every digit after it repeats too --
   that is exactly where the cycle starts.
3. Store remainder -> index of the digit it produced. When we see a
   remainder again, insert "(" at the stored index and append ")".
4. If the remainder hits 0, the decimal terminates.
5. Handle the sign separately (negative iff exactly one operand is
   negative and the numerator is nonzero) and work with absolute values.

Why it terminates: remainders live in [0, den), so by pigeonhole we either
hit 0 or repeat within den steps.

Complexity
----------
Time:  O(den) in the worst case (length of the repeating cycle).
Space: O(den) for the remainder map and digits.
"""


class Solution:
    def fractionToDecimal(self, numerator: int, denominator: int) -> str:
        if numerator == 0:
            return "0"
        sign = "-" if (numerator < 0) != (denominator < 0) else ""
        n, d = abs(numerator), abs(denominator)
        whole, rem = divmod(n, d)
        if rem == 0:
            return f"{sign}{whole}"

        digits = []
        seen = {}                # remainder -> position in digits
        while rem and rem not in seen:
            seen[rem] = len(digits)
            rem *= 10
            q, rem = divmod(rem, d)
            digits.append(str(q))
        if rem:                  # cycle detected
            i = seen[rem]
            frac = "".join(digits[:i]) + "(" + "".join(digits[i:]) + ")"
        else:
            frac = "".join(digits)
        return f"{sign}{whole}.{frac}"


def to_fraction(s: str):
    """Parse our output back into an exact Fraction (for cross-checks)."""
    from fractions import Fraction
    neg = s.startswith("-")
    s = s.lstrip("-")
    if "." not in s:
        val = Fraction(int(s))
    else:
        whole, frac = s.split(".")
        if "(" in frac:
            pre, rep = frac.rstrip(")").split("(")
        else:
            pre, rep = frac, ""
        val = Fraction(int(whole))
        if pre:
            val += Fraction(int(pre), 10 ** len(pre))
        if rep:
            val += Fraction(int(rep), (10 ** len(rep) - 1) * 10 ** len(pre))
    return -val if neg else val


if __name__ == "__main__":
    from fractions import Fraction
    s = Solution()
    cases = [
        (1, 2, "0.5"),
        (2, 1, "2"),
        (4, 333, "0.(012)"),
        (2, 3, "0.(6)"),
        (1, 6, "0.1(6)"),
        (-50, 8, "-6.25"),
        (7, -12, "-0.58(3)"),
        (0, -5, "0"),
        (-2147483648, -1, "2147483648"),
    ]
    for num, den, want in cases:
        got = s.fractionToDecimal(num, den)
        assert got == want, (num, den, got, want)
        print(f"fractionToDecimal({num}, {den}) = {got}")

    import random
    random.seed(166)
    for _ in range(1000):
        num = random.randint(-500, 500)
        den = random.choice([v for v in range(-60, 61) if v != 0])
        out = s.fractionToDecimal(num, den)
        assert to_fraction(out) == Fraction(num, den), (num, den, out)
    print("random round-trip vs fractions.Fraction OK")
    print("All tests passed.")
