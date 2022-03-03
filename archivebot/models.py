from datetime import datetime


class SQLTweet:
    CREATE_STATEMENT = """
    CREATE TABLE IF NOT EXISTS tweet (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        in_reply_to INTEGER DEFAULT NULL,
        content TEXT NOT NULL,
        date DATETIME NOT NULL,
        deleted BOOL DEFAULT 0,
        FOREIGN KEY(user_id) REFERENCES user(id),
        FOREIGN KEY(in_reply_to) REFERENCES tweet(id)
    )
    """

    def __init__(
        self,
        id: int,
        user_id: int,
        in_reply_to: int = None,
        content: str = None,
        date: datetime = None,
        deleted: bool = False,
    ):
        self.id = id
        self.user_id = user_id
        self.in_reply_to = in_reply_to
        self.content = content
        self.date = date
        self.deleted = deleted


class SQLUser:
    CREATE_STATEMENT = """
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY,
        screen_name TEXT UNIQUE NOT NULL,
        monitored BOOL DEFAULT 0
    )
    """

    def __init__(self, id: int, screen_name: str, monitored: bool):
        self.id = id
        self.screen_name = screen_name
        self.monitored = monitored
