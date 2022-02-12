import json

from tracking_stream import TrackingStream
from configs import API, API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET


def restore_streams() -> list[TrackingStream]:
    with open("streams.json") as reader:
        streams = json.load(reader)

    tracking_streams = []

    for stream in streams:
        user_id = stream["user_id"]
        last_tweet_id = stream["last_tweet_id"]

        new_tracking_stream = TrackingStream(
            API_KEY,
            API_KEY_SECRET,
            ACCESS_TOKEN,
            ACCESS_TOKEN_SECRET,
            user_id,
            last_tweet_id=last_tweet_id,
        )
        tracking_streams.append(new_tracking_stream)

    return tracking_streams
