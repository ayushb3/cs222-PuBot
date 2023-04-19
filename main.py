"""PuBot: Twitter bot to summarize text
CLI Usage:
"""

from datetime import datetime
import argparse
import subprocess
import time
import schedule
from src.summarizer import summarize
from src.title_generator import generate_title
from src.tweeter import api, tweet
from src.database import insert_article, pick_article, create_table


def tweet_scheduler(options):
    print("Starting scheduler...")

    def job():
        subprocess.run(['python', 'main.py', 'tweet'], check=True, shell=True)
    scheduler = getattr(schedule.every(options.every), options.interval)
    at_text = ""
    if options.at:
        scheduler = scheduler.at(options.at)
        at_text = f" at {options.at}"
    scheduler.do(job)
    print("Scheduler started.\n"
          f"Tweeting every {options.every} {options.interval}{at_text}...\n"
          "(Press Ctrl+C to stop)")
    # Initial run
    job()
    while True:
        schedule.run_pending()
        time.sleep(1)


def pick_and_tweet(options):
    article = pick_article()
    if not article:
        print("No articles to tweet.")
        return
    print(f"Summarizing '{article[1]}' by {article[2]}...")
    summary = summarize(article[4])
    title = generate_title(article[4])
    tweet_content = f"{title}\n{summary}"
    print("Tweeting:\n\n" + tweet_content)
    # tweet(api(), tweet_content) Can't tweet yet

def tweet_at(options):
    article = get_single_article(options.id)
    tweet(api(),summarize(article['content']),options.time)



def add_article(options):
    create_table()
    insert_article(options.title, options.author,
                   options.date, options.file.read())


if __name__ == '__main__':
    global_parser = argparse.ArgumentParser(
        prog="PuBot", description="Twitter bot to summarize text")
    global_parser.add_argument(
        '-db', '--database', help='Path to sqlite database file', default='articles.db')

    subparsers = global_parser.add_subparsers(required=True, dest='command')

    tweet_parser = subparsers.add_parser(
        'tweet', help='Tweet a summary of a randomly selected text in database')
    tweet_parser.set_defaults(func=pick_and_tweet)


    scheduler_parser = subparsers.add_parser(
        'scheduler', help='Schedule tweets at a specified interval')
    scheduler_parser.add_argument(
        '-e', '--every', help='How many intervals to wait for every tweet (Ex: every 5 [INTERVAL])', type=int, default=1)
    scheduler_parser.add_argument(
        '-i', '--interval', default="days", const="days", nargs="?",
        help='Duration of interval (Ex: [EVERY] days)', choices=['weeks', 'days', 'hours', 'minutes', 'seconds'])
    scheduler_parser.add_argument(
        '-a', '--at', help='The specific time to tweet in an interval (Ex: 12:00 for at noon every day)')
    scheduler_parser.set_defaults(func=tweet_scheduler)
    tweet_at_parser = subparsers.add_parser(
        'tweetat', help='Tweet a specific article at a specific time'
    )
    tweet_at_parser.add_argument(
        '-t', '--time', help='Time to tweet (Y-m-d H:M:S)'
    )
    tweet_at_parser.add_argument(
        '--id', help ='article id'
    )
    tweet_at_parser.set_defaults(func = tweet_at)

    db_parser = subparsers.add_parser(
        'insert', help='Insert a new article into the database')
    db_parser.add_argument(
        '-t', '--title', help='Title of the article')
    db_parser.add_argument(
        '-a', '--author', help='Author of the article')
    db_parser.add_argument(
        '-d', '--date', help='Date of the article (Y-m-d)', type=lambda d: datetime.strptime(d, '%Y-%m-%d'))
    db_parser.add_argument(
        '-f', '--file', help='File containing content of article', type=argparse.FileType('r'), required=True)
    # db_parser.add_argument(
    #     metavar="CONTENT", help='Content of a text', dest='operands')
    db_parser.set_defaults(func=add_article)
    args = global_parser.parse_args()

    if hasattr(args, 'operands') and not isinstance(args.operands, list):
        setattr(args, 'operands', [args.operands])

    if not hasattr(args, 'operands'):
        setattr(args, 'operands', [])

    args.func(args, *args.operands)
