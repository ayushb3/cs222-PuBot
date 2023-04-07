import tweepy
import schedule
import time
import datetime
from settings import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
from src.summarizer import summarize
import os
from src.database import get_all_new_articles, delete_article


def api():
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    return tweepy.API(auth)

def tweeter():
    # TO DO: not necessary to have hasDate anymore if we are deleting after tweeting
    tweets_to_be_scheduled = get_all_new_articles(hasDate=True)
    tweets_to_be_put_on_scheduler = get_all_new_articles(hasDate=False)
    for t in tweets_to_be_scheduled:
        tweet(api = api(), message=t[1], date=t[2])
        delete_article(t[0])
    schedule.every().day.at("12:00").do(scheduled_tweeter, tweets_to_be_put_on_scheduler)
    # TO DO: check if parameters are passed as references so that we move onto different tweets


    # if we run out of tweets, stop the schedule
    while len(schedule.jobs) != 0:
        schedule.run_pending()
        time.sleep(1)

# Function to publish tweet with optional date for scheduling for an article that has not been released yet
# def tweet(api: tweepy.API, message: str, date: str):
#     if message: 
#         if date:
#             tweet_time = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
#             api.update_status(message, scheduled_at=tweet_time)
#             print('Tweeted successfully!')
#         api.update_status(message)
#     else:
#         print('Tweeted unsuccessfully!')

# Function to schedule tweets for a specified frequency given in hours
def scheduled_tweeter(tweets):
        item = tweets.pop(0)  
        tweet(api = api(), message = item[1], date=None)
        delete_article(item[0])
        

# Function to delete a user selected tweet out of a range of the numTweets most recent tweets
# def delete_tweets(api: tweepy.API, numTweets: int):
#     tweets = api.user_timeline(count=10)

#     print("Recent tweets:")
#     for i, tweet in enumerate(tweets):
#         print(f"{i+1} : {tweet.text}")
#     for x in range(3):
#         choice = int(input("Enter the number corresponding to the tweet you want to delete: "))

#         try:
#             if choice < 1 or choice > len(tweets):
#                 raise ValueError
#             break
#         except ValueError:
#             print("Invalid choice. Please enter a number between 1 and", len(tweets))
#     else:
#         print("You have exceeded the maximum number of attempts. Please try again later.")
#         exit()


#     tweet_id = tweets[choice-1].id_str

#     api.destroy_status(tweet_id)
#     print(f"The tweet has been deleted.")

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
