"""
LeetCode 1235 -- Maximum Profit in Job Scheduling (Hard)
https://leetcode.com/problems/maximum-profit-in-job-scheduling/

Problem
-------
Job i runs from startTime[i] to endTime[i] and pays profit[i]. Pick a set of
non-overlapping jobs (a job may start exactly when another ends) to maximise
total profit.

Thought process
---------------
1. This is weighted interval scheduling. Greedy (earliest end, biggest profit)
   fails because one fat job can beat several small ones, so we need DP.
2. Sort jobs by end time. Let dp[i] = best profit using only the first i jobs
   (in end-time order). For job i we have two choices:
     - skip it:  dp[i] = dp[i-1]
     - take it:  profit[i] + dp[j], where j = number of jobs that end at or
                 before job i starts.
3. Because the ends are sorted, j is found with binary search
   (bisect_right on the end times with key = start of job i).
4. dp[n] is the answer.

Why it works: in any optimal set, the last job (by end time) is either job i
or not. If it is, everything else must finish by start_i, which is exactly the
prefix of j jobs -- and dp[j] is already optimal for that prefix.

Complexity
----------
Time:  O(n log n) -- sorting plus one binary search per job.
Space: O(n) for dp and the end-time array.
"""

from bisect import bisect_right
from typing import List


class Solution:
    def jobScheduling(self, startTime: List[int], endTime: List[int], profit: List[int]) -> int:
        jobs = sorted(zip(endTime, startTime, profit))
        ends = [e for e, _, _ in jobs]
        dp = [0] * (len(jobs) + 1)
        for i, (end, start, gain) in enumerate(jobs, 1):
            j = bisect_right(ends, start, 0, i - 1)  # jobs ending <= start
            dp[i] = max(dp[i - 1], dp[j] + gain)
        return dp[-1]


if __name__ == "__main__":
    s = Solution()
    assert s.jobScheduling([1, 2, 3, 3], [3, 4, 5, 6], [50, 10, 40, 70]) == 120
    assert s.jobScheduling([1, 2, 3, 4, 6], [3, 5, 10, 6, 9], [20, 20, 100, 70, 60]) == 150
    assert s.jobScheduling([1, 1, 1], [2, 3, 4], [5, 6, 4]) == 6
    assert s.jobScheduling([1], [2], [7]) == 7
    print("1235 Maximum Profit in Job Scheduling: all tests passed")
