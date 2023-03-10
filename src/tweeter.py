import tweepy
from settings import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
from summarizer import summarize
import os


def api():
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    return tweepy.API(auth)

# Function to publish tweet with optional date for scheduling
def tweet(api: tweepy.API, message: str, date: str):
    if message and date:
        tweet_time = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        api.update_status(message, scheduled_at=tweet_time)
        print('Tweeted successfully!')
    else if message:
        api.update_status(message)
    else:
        print('Tweeted unsuccessfully!')