"""
LeetCode 355: Design Twitter
Difficulty: Medium
Topic: Design / Heap (k-way merge)

Problem
-------
Build a tiny Twitter supporting:
  - postTweet(userId, tweetId): user posts a tweet.
  - getNewsFeed(userId): the 10 most recent tweet ids from the user and
    everyone they follow, newest first.
  - follow(followerId, followeeId) / unfollow(followerId, followeeId).

Approach (thought process)
--------------------------
1. Store each user's tweets as a list of (time, tweetId) in posting order,
   using a global counter for time so tweets across users are comparable.
   A list is naturally sorted by time, newest at the end.
2. Store follows as a set per user, so follow/unfollow are O(1) and
   duplicates don't matter.
3. The feed is "top 10 newest across several already-sorted lists". That is
   the merge-k-sorted-lists pattern (23), but we only need 10 items, so we
   don't merge everything.
4. Push the newest tweet of each relevant user (self + followees) into a
   max-heap keyed by time (negate for Python's min-heap). Pop the newest,
   record it, and push that same user's next-older tweet. Stop after 10.
5. A user always sees their own tweets, so include them even though they
   don't "follow" themselves; ignore attempts to unfollow yourself.

Why it works: each list is sorted, so the overall newest unseen tweet must
be the head of one of the lists; the heap always holds every list's head,
so its top is that tweet.

Complexity (F = number of people in the feed, 10 = feed size):
  - postTweet / follow / unfollow: O(1).
  - getNewsFeed: O(F + 10 log F) — build the heap, then 10 pops/pushes.
  - Space: O(total tweets + total follow edges).
"""

import heapq
from collections import defaultdict
from typing import List


class Twitter:
    def __init__(self):
        self.time = 0
        self.tweets = defaultdict(list)     # user -> [(time, tweetId), ...]
        self.following = defaultdict(set)   # user -> {followee, ...}

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.tweets[userId].append((self.time, tweetId))
        self.time += 1

    def getNewsFeed(self, userId: int) -> List[int]:
        heap = []
        for uid in self.following[userId] | {userId}:
            if self.tweets[uid]:
                idx = len(self.tweets[uid]) - 1
                t, tid = self.tweets[uid][idx]
                heap.append((-t, tid, uid, idx))
        heapq.heapify(heap)

        feed = []
        while heap and len(feed) < 10:
            _, tid, uid, idx = heapq.heappop(heap)
            feed.append(tid)
            if idx > 0:
                t, nxt = self.tweets[uid][idx - 1]
                heapq.heappush(heap, (-t, nxt, uid, idx - 1))
        return feed

    def follow(self, followerId: int, followeeId: int) -> None:
        if followerId != followeeId:
            self.following[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        self.following[followerId].discard(followeeId)


if __name__ == "__main__":
    tw = Twitter()
    tw.postTweet(1, 5)
    assert tw.getNewsFeed(1) == [5]
    tw.follow(1, 2)
    tw.postTweet(2, 6)
    assert tw.getNewsFeed(1) == [6, 5]
    tw.unfollow(1, 2)
    assert tw.getNewsFeed(1) == [5]

    # Feed caps at 10 and interleaves users by time.
    tw2 = Twitter()
    for i in range(8):
        tw2.postTweet(1, 100 + i)
        tw2.postTweet(2, 200 + i)
    tw2.follow(1, 2)
    feed = tw2.getNewsFeed(1)
    assert feed == [207, 107, 206, 106, 205, 105, 204, 104, 203, 103], feed
    tw2.unfollow(1, 1)  # unfollowing yourself is a no-op
    assert tw2.getNewsFeed(1)[0] == 207
    print("Feed:", feed)
    print("All tests passed.")
