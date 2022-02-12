from queue import Queue

import tweepy


class MentionsStream(tweepy.Stream):
    def __init__(self, *args, queue: Queue, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = queue

    def on_status(self, tweet: tweepy.Tweet):
        self.queue.put(tweet)
