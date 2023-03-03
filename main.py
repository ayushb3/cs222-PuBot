import tweepy
from settings import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
from src.summarizer import summarize
import os


def api():
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    return tweepy.API(auth)


def tweet(api: tweepy.API, message: str):
    if message:
        api.update_status(message)
        print('Tweeted successfully!')
    else:
        print('Tweeted unsuccessfully!')


if __name__ == '__main__':
    text = os.sys.argv[1]
    api = api()
    tweet(api, summarize(text))
