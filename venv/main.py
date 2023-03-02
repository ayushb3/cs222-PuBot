import tweepy
import keys

def api():
    auth = tweepy.OAuthHandler(keys.api_key, keys.api_secret)
    auth.set_access_token(keys.access_token, keys.access_token_secret)

    return tweepy.API(auth)


def tweet(api: tweepy.API, message: str):
    if message:
        api.update_status(message)
        print('Tweeted successfully!')
    else:
        print('Tweeted unsuccessfully!')


if __name__ == '__main__':
    api = api()
    tweet(api, 'This was tweeted from Python')