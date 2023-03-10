import tweepy
from settings import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
from src.summarizer import summarize
from src.tweeter import api, tweet
import os




if __name__ == '__main__':
    text = os.sys.argv[1]
    api = api()
    tweet(api, summarize(text))
