import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

from config import MAX_WORKERS
from task import task
import db


def main():
    users_to_monitor = db.get_users_to_monitor()
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(task, user, check_delete_limit=10)
            for user in users_to_monitor
        }

        while True:
            done, not_done = concurrent.futures.wait(futures)

            for future in done:
                user, new_tweets, deleted_tweets, last_tweet = future.result()
                db.save_tweets(new_tweets)
                db.set_deleted_tweets(deleted_tweets)

                # submit again
                futures.add(
                    executor.submit(
                        task, user, last_tweet=last_tweet, check_delete_limit=10
                    )
                )

                futures.remove(future)


if __name__ == "__main__":
    main()
