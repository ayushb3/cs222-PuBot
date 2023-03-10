import tweepy
import datetime
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
    elif message:
        api.update_status(message)
    else:
        print('Tweeted unsuccessfully!')

# Function to delete a user selected tweet out of a range of the numTweets most recent tweets
def delete_tweets(api: tweepy.API, numTweets: int):
    tweets = api.user_timeline(count=10)

    print("Recent tweets:")
    for i, tweet in enumerate(tweets):
        print(f"{i+1} : {tweet.text}")
    for x in range(3):
        choice = int(input("Enter the number corresponding to the tweet you want to delete: "))

        try:
            if choice < 1 or choice > len(tweets):
                raise ValueError
            break
        except ValueError:
            print("Invalid choice. Please enter a number between 1 and", len(tweets))
    else:
        print("You have exceeded the maximum number of attempts. Please try again later.")
        exit()


    tweet_id = tweets[choice-1].id_str

    api.destroy_status(tweet_id)
    print(f"The tweet has been deleted.")