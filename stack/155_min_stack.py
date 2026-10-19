"""
LeetCode 155: Min Stack
Difficulty: Medium
Topic: Stack / Design (Auxiliary State per Entry)

Problem
-------
Design a stack that supports push, pop, top, and getMin, each in O(1) time.

Example:
  push(-2), push(0), push(-3)
  getMin() -> -3
  pop()
  top()    -> 0
  getMin() -> -2

Approach (thought process)
--------------------------
1. push/pop/top are free with a Python list. The hard part is getMin: scanning
   the stack is O(n), and a single "current min" variable breaks the moment
   you pop the minimum, because you don't know what the min was before it.
2. Key observation: a stack only ever removes the most recent item, so the
   minimum "as of" any entry never changes while that entry is on the stack.
   Everything below it is frozen.
3. So store the answer alongside each entry: push the pair
   (value, min(value, previous min)). The top pair always carries the minimum
   of the whole stack.
4. Popping simply drops the pair, and the new top already holds the correct
   older minimum. Nothing needs recomputing.
5. (Space tweak: a second stack that only pushes when value <= current min
   saves memory on long runs of large values. The pair version is simpler
   and has the same big-O.)

Why it works: the stack's history is strictly last-in-first-out, so the
snapshot of "min so far" taken at push time stays valid until that exact
entry is popped.

Complexity:
  - Time: O(1) for every operation.
  - Space: O(n) for n stored values (two numbers per entry).
"""


class MinStack:
    def __init__(self) -> None:
        self._stack: list[tuple[int, int]] = []   # (value, min so far)

    def push(self, val: int) -> None:
        current_min = min(val, self._stack[-1][1]) if self._stack else val
        self._stack.append((val, current_min))

    def pop(self) -> None:
        self._stack.pop()

    def top(self) -> int:
        return self._stack[-1][0]

    def getMin(self) -> int:
        return self._stack[-1][1]


if __name__ == "__main__":
    import random

    s = MinStack()
    s.push(-2)
    s.push(0)
    s.push(-3)
    assert s.getMin() == -3
    s.pop()
    assert s.top() == 0
    assert s.getMin() == -2

    # Duplicate minimums must survive a pop.
    d = MinStack()
    for v in (1, 1, 2):
        d.push(v)
    d.pop()
    d.pop()
    assert d.getMin() == 1

    # Randomized check against a plain list.
    for _ in range(300):
        ms, ref = MinStack(), []
        for _ in range(60):
            if ref and random.random() < 0.4:
                ms.pop()
                ref.pop()
            else:
                v = random.randint(-20, 20)
                ms.push(v)
                ref.append(v)
            if ref:
                assert ms.top() == ref[-1]
                assert ms.getMin() == min(ref)
    print("All tests passed for 155. Min Stack")
