"""
LeetCode 735: Asteroid Collision
Difficulty: Medium
Topic: Stack

Problem
-------
We are given an array asteroids of integers representing asteroids in a row.
For each asteroid, the absolute value is its size, and the sign is its
direction (positive = right, negative = left). All asteroids move at the
same speed.

When two asteroids meet:
  - the smaller one explodes
  - if equal size, both explode
  - same-direction asteroids never meet

Find out the state of the asteroids after all collisions.

Examples:
  [5, 10, -5]  ->  [5, 10]     # 10 and -5 collide; 10 wins
  [8, -8]      ->  []          # equal size; both gone
  [10, 2, -5]  ->  [10]        # 2 then -5 die against 10
  [-2, -1, 1, 2] -> [-2, -1, 1, 2]  # no head-ons (lefties flee left, righties flee right)

Approach (thought process)
--------------------------
1. Collisions only happen when a right-mover is followed (eventually) by a
   left-mover — i.e. they are heading toward each other. Two right-movers
   drift apart forever relative to each other; two left-movers likewise.
   So the only "dangerous" pattern is a positive sitting on the stack when
   a negative arrives.
2. That suggests a stack of survivors so far, scanned left to right. When
   the next asteroid is not a left-mover crashing into a right-mover on top,
   just push it. Otherwise fight.
3. The fight can chain: a big negative may smash several smaller right-movers
   that had piled up. So while the stack top is positive and the new rock is
   negative, compare sizes:
     - |new| > top  -> pop top (top dies), keep fighting with new
     - |new| < top  -> new dies; stop (do not push)
     - equal        -> pop top and kill new; stop
4. Only push the new asteroid if it survived every duel (or never had one).
5. At the end the stack is exactly the remaining asteroids, left to right.

Why it works: every head-on pair is examined in the order they would meet —
the leftmost unresolved right-mover meets the incoming left-mover first.
Same-direction rocks stay stacked in their original relative order, and
asteroids that never face an opponent (all-negative prefix, all-positive
suffix, or survivors that out-massed every challenger) are left untouched.
Because we only ever pop a rock that lost a collision, nothing that should
survive is discarded.

Complexity:
  - Time: O(n) — each asteroid is pushed at most once and popped at most once.
  - Space: O(n) for the stack of survivors in the worst case (no collisions).
"""


class Solution:
    def asteroidCollision(self, asteroids: list[int]) -> list[int]:
        stack: list[int] = []
        for a in asteroids:
            alive = True
            # Only collide when a left-mover meets a right-mover on top.
            while alive and stack and stack[-1] > 0 and a < 0:
                top = stack[-1]
                if top < -a:
                    stack.pop()  # top dies; keep fighting with a
                elif top == -a:
                    stack.pop()  # both die
                    alive = False
                else:
                    alive = False  # a dies; top stays
            if alive:
                stack.append(a)
        return stack


if __name__ == "__main__":
    sol = Solution()
    cases = [
        ([5, 10, -5], [5, 10]),
        ([8, -8], []),
        ([10, 2, -5], [10]),
        ([-2, -1, 1, 2], [-2, -1, 1, 2]),
        ([1, -2, -2, -2], [-2, -2, -2]),
        ([-2, -2, 1, -2], [-2, -2, -2]),
        ([5, -5], []),
        ([1, 2, 3, -3, -2, -1], []),
        ([1, 2, 3, -1], [1, 2, 3]),
        ([-5, 10], [-5, 10]),
    ]
    for asteroids, want in cases:
        got = sol.asteroidCollision(list(asteroids))
        assert got == want, (asteroids, got, want)
        print(f"{asteroids!r:>24} -> {got!r}")
    print("all tests passed")
