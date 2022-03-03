from snscrape.modules.twitter import Tweet

def publish_deleted_tweets(deleted_tweets: list[Tweet]):
    for tweet in deleted_tweets:
        print(f"Deleted tweet: {tweet.id}")