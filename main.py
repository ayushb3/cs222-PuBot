"""PuBot: Twitter bot to summarize text
CLI Usage:
"""

import argparse
import subprocess
import time
import schedule
import wikipedia
from src.summarizer import Summarizer
from src.tweeter import Tweeter
from src.database import Database
from settings import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, BEARER_TOKEN


def start_flask(options):
    from webserver import app
    app.config['database'] = Database(options.database)
    app.config['tweeter'] = Tweeter(BEARER_TOKEN, API_KEY, API_SECRET,
                                    ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    app.config['summarizer'] = Summarizer()
    app.run(debug=True)



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
    db = Database(options.database)
    tweeter = Tweeter(BEARER_TOKEN, API_KEY, API_SECRET,
                      ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    summarizer = Summarizer()
    article = db.pick_article()
    if not article:
        print("No articles to tweet.")
        return
    title, author = article["title"], article["author"]
    print(f"Summarizing '{title}' by {author}...")
    summarizer.make_tweet(article["content"])
    text = summarizer.get_content()
    print("Tweeting...", text, sep="\n")
    tweet = tweeter.tweet(text)
    print(tweet)


# def tweet_at(options):
#     article = get_single_article(options.id)
#     tweet(api(), summarize(article['content']), options.time)


def add_article(options):
    db = Database(options.database)
    db.insert_article(options.author, options.title, options.file.read())


def add_wikipedia_article(options):
    db = Database(options.database)
    wikipedia.set_lang("en")
    page = wikipedia.page(options.title, preload=True)
    db.insert_article("Wikipedia", page.original_title, page.content)
    print(f"Added '{page.original_title}' by Wikipedia to database.")


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

    # tweet_at_parser = subparsers.add_parser(
    #     'tweetat', help='Tweet a specific article at a specific time'
    # )
    # tweet_at_parser.add_argument(
    #     '-t', '--time', help='Time to tweet (Y-m-d H:M:S)'
    # )
    # tweet_at_parser.add_argument(
    #     '--id', help='article id'
    # )
    # tweet_at_parser.set_defaults(func=tweet_at)

    db_parser = subparsers.add_parser(
        'insert', help='Insert a new article into the database')
    db_parser.add_argument(
        '-t', '--title', help='Title of the article')
    db_parser.add_argument(
        '-a', '--author', help='Author of the article')
    # db_parser.add_argument(
    #     '-d', '--date', help='Date of the article (Y-m-d)', type=lambda d: datetime.strptime(d, '%Y-%m-%d'))
    db_parser.add_argument(
        '-f', '--file', help='File containing content of article', type=argparse.FileType('r'), required=True)
    # db_parser.add_argument(
    #     metavar="CONTENT", help='Content of a text', dest='operands')
    db_parser.set_defaults(func=add_article)

    wiki_parser = subparsers.add_parser(
        'insertwiki', help='Insert a new wikipedia article into the database')
    wiki_parser.add_argument(
        '-t', '--title', required=True, help='Title of the wikipedia article')
    wiki_parser.set_defaults(func=add_wikipedia_article)

    flask_parser = subparsers.add_parser(
        'flask', help='Run the flask server'
    )
    flask_parser.set_defaults(func=start_flask)

    args = global_parser.parse_args()

    if hasattr(args, 'operands') and not isinstance(args.operands, list):
        setattr(args, 'operands', [args.operands])

    if not hasattr(args, 'operands'):
        setattr(args, 'operands', [])

    args.func(args, *args.operands)
