import sqlite3

from snscrape.modules.twitter import Tweet

from models import SQLTweet, SQLUser
from config import DB_FILENAME

with sqlite3.connect(DB_FILENAME) as conn:
    conn.cursor().executescript(
        "\n;\n".join((SQLTweet.CREATE_STATEMENT, SQLUser.CREATE_STATEMENT))
    )


def get_users_to_monitor() -> list[SQLUser]:
    with sqlite3.connect(DB_FILENAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM user
            WHERE monitored = 1
            """
        )
        return [SQLUser(*user) for user in cursor.fetchall()]


def save_tweets(tweets: list[Tweet]):
    with sqlite3.connect("archivebot.db") as conn:
        cursor = conn.cursor()
        cursor.executemany(
            """
            INSERT OR IGNORE INTO tweet (id, user_id, content, date)
            VALUES (?, ?, ?, ?)
            """,
            [(tweet.id, tweet.user.id, tweet.content, tweet.date) for tweet in tweets],
        )
        for tweet in tweets:
            print(f"Saved tweet: {tweet.id} from user {tweet.user.username}")


def set_deleted_tweets(tweets: list[SQLTweet]):
    with sqlite3.connect("archivebot.db") as conn:
        cursor = conn.cursor()
        cursor.executemany(
            """
            UPDATE tweet SET deleted = 1 WHERE id = ?
            """,
            [(tweet.id,) for tweet in tweets],
        )
        for tweet in tweets:
            print(f"Deleted tweet: {tweet.id} from user {tweet.user_id}")


def get_tweets(user: SQLUser) -> SQLTweet:
    with sqlite3.connect("archivebot.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM tweet
            WHERE user_id = ?
            """,
            (user.id,),
        )
        return [SQLTweet(*tweet) for tweet in cursor.fetchall()]
