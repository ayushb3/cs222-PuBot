from src.summarizer import summarize
from src.tweeter import api, tweet
from src.database import insert_article, get_single_article
from datetime import datetime
import argparse


def pick_and_tweet(options):
    # TODO: replace with random database select
    article = {'title': 'Test Article', 'author': 'John Doe',
               'content': 'This is a test article.'}
    tweet(api(), summarize(article['content']))

def tweet_at(options):
    article = get_single_article(options.id)
    tweet(api(),summarize(article['content']),options.time)


def add_article(options, content):
    insert_article(options.title, options.author, options.date, content)


if __name__ == '__main__':
    global_parser = argparse.ArgumentParser(
        prog="PuBot", description="Twitter bot to summarize text")
    global_parser.add_argument(
        '-db', '--database', help='Path to sqlite database file', default='articles.db')

    subparsers = global_parser.add_subparsers(required=True, dest='command')

    tweet_parser = subparsers.add_parser(
        'tweet', help='Tweet a summary of a randomly selected text in database')
    tweet_parser.set_defaults(func=pick_and_tweet)

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
        metavar="CONTENT", help='Content of a text', dest='operands')
    db_parser.set_defaults(func=add_article)
    args = global_parser.parse_args()

    if hasattr(args, 'operands') and not isinstance(args.operands, list):
        setattr(args, 'operands', [args.operands])

    if not hasattr(args, 'operands'):
        setattr(args, 'operands', [])

    args.func(args, *args.operands)
