from queue import Queue

import tweepy
from archivebot.restore_streams import restore_streams

from mentions_stream import MentionsStream
from tracking_stream import TrackingStream
from configs import API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET


def main(api: tweepy.API):
    queue = Queue()
    streams = restore_streams()

    mentions_stream = MentionsStream(
        API_KEY,
        API_KEY_SECRET,
        ACCESS_TOKEN,
        ACCESS_TOKEN_SECRET,
        queue=queue,
        daemon=True,
    )
    mentions_stream.filter(track=["@archivebot"]).start()

    while True:
        tweet = queue.get()

        # iterate through mentions in the tweet not including the mention to us
        # for mention in tweet.entities["user_mentions"]:
        #     if mention["screen_name"] != "@archivebot":
        #         # check if we're already tracking this user
        #         if ...:
        #             continue

        #         new_tracking_stream = TrackingStream(
        #             api, mention["screen_name"], queue=queue, daemon=True
        #         )
        #         new_tracking_stream.filter(follow=[mention["id"]])
        #         new_tracking_stream.thread
        breakpoint()


if __name__ == "__main__":
    from configs import API

    main(API)
