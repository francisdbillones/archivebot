import tweepy


class TrackingStream(tweepy.Stream):
    def __init__(self, *args, user_id: str, last_tweet_id: str = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id = user_id
        self.last_tweet_id = last_tweet_id
        self.filter(follow=[user_id])

    def on_status(self, tweet: tweepy.Tweet):
        ...
