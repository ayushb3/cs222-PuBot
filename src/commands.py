import time
import threading
import schedule
from src.summarizer import Summarizer
from src.tweeter import Tweeter
from src.database import Database


def run_continuously(interval=1):
    """Continuously run, while executing pending jobs at each
    elapsed time interval.
    @return cease_continuous_run: threading. Event which can
    be set to cease continuous run. Please note that it is
    *intended behavior that run_continuously() does not run
    missed jobs*. For example, if you've registered a job that
    should run every minute and you set a continuous run
    interval of one hour then your job won't be run 60 times
    at each interval but only once.
    """
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


def _tweet_scheduler(db_path: str, summarizer: Summarizer, tweeter: Tweeter, every: int, interval: str, at: str = None, on_tweet: callable = None):
    print("Starting scheduler...")

    def job():
        db = Database(db_path)
        tweet = _pick_and_tweet(db, summarizer, tweeter)
        if on_tweet:
            on_tweet(tweet)
    scheduler = getattr(schedule.every(every), interval)
    at_text = ""
    if at:
        scheduler = scheduler.at(at)
        at_text = f" at {at}"
    scheduler.do(job)
    print("Scheduler started.\n"
          f"Tweeting every {every} {interval}{at_text}...\n"
          "(Press Ctrl+C to stop)")
    # Initial run
    # job()
    return run_continuously()


def _tweet(article: dict, summarizer: Summarizer, tweeter: Tweeter) -> dict:
    author, title, content = article["author"], article["title"], article["content"]
    print(f"Summarizing '{title}' by {author}...")
    summarizer.make_tweet(content)
    text = summarizer.get_content()
    print("Tweeting...", text, sep="\n")
    tweet = tweeter.tweet(text)
    print(tweet)
    return tweet


def _pick_and_tweet(db: Database, summarizer: Summarizer, tweeter: Tweeter) -> dict:
    article = db.pick_article()
    if not article:
        print("No articles to tweet.")
        return
    return _tweet(article, summarizer, tweeter)
