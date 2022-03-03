import itertools as it
import sqlite3
from tqdm import tqdm

import snscrape.modules.twitter as twitter
from snscrape.modules.twitter import Tweet

from models import SQLUser, SQLTweet


def task(
    user: SQLUser, last_tweet: Tweet = None, check_delete_limit: int = None
) -> tuple[SQLUser, list[Tweet], list[SQLTweet], Tweet]:
    """
    Returns a tuple of (new_tweets, deleted_tweets)
    """
    print(f"Task for user {user.id}")
    tweet_iterator = tqdm(
        twitter.TwitterUserScraper(str(user.id), isUserId=True).get_items()
    )

    with sqlite3.connect("archivebot.db") as conn:
        cursor = conn.cursor()
        stored_tweets = [
            SQLTweet(*tweet)
            for tweet in cursor.execute(
                """
            SELECT id, date FROM tweet
            WHERE user_id = ?
            """,
                (user.id,),
            )
        ]

    if last_tweet is not None:
        # just in case last_tweet has been deleted,
        # matching against id will not work because
        # the last_tweet will not be in retrieved_tweets.
        # so we just check for tweets younger than last_tweet.
        new_tweets = list(
            it.takewhile(lambda tweet: tweet.date < last_tweet.date, tweet_iterator)
        )
    else:
        new_tweets = list(tweet_iterator)
    # since tweet_iterator is now exhausted of new tweets,
    # we take the rest of the tweets (up to check_delete_limit) and check for deletions.
    # if check_delete_limit is None, we take all tweets.
    # if check_delete_limit is 0, we take no tweets.

    if check_delete_limit is not None:
        tweet_iterator = it.islice(tweet_iterator, check_delete_limit)
    old_tweet_ids = {tweet.id for tweet in tweet_iterator}
    deleted_tweets = [tweet for tweet in stored_tweets if tweet.id not in old_tweet_ids]

    return (
        user,
        new_tweets,
        deleted_tweets,
        new_tweets[-1] if new_tweets else last_tweet,
    )
