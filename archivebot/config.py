import os

MAX_WORKERS = os.cpu_count()
DB_FILENAME = "archivebot.db"

MONITORED_USERS = [
    (1077117570019258373, "francishubertdb"),
    #(1349149096909668363, "POTUS"),
    #(12, "jack"),
]

import sqlite3

import db

with sqlite3.connect("archivebot.db") as conn:
    conn.cursor().executemany(
        """
        INSERT OR IGNORE INTO user (id, screen_name, monitored)
        VALUES (?, ?, 1)
        """,
        [(user_id, username) for user_id, username in MONITORED_USERS],
    )
