import tweepy
import datetime
from settings import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET


def api():
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    return tweepy.API(auth)


def tweets(api: tweepy.API):
    for t in tweepy.Cursor(api.user_timeline).items():
        yield t


def tweet(api: tweepy.API, message: str, date: str = None):
    """Function to publish tweet with optional date for scheduling"""

    if message and date:
        tweet_time = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        api.update_status(message, scheduled_at=tweet_time)
    elif message:
        api.update_status(message)


def delete_tweets(api: tweepy.API, statuses: list):
    """Function to delete a tweets from given list of tweet statuses"""
    for status in statuses:
        api.destroy_status(status.id)
