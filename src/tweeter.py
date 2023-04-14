import tweepy


class Tweeter:
    def __init__(self, api_key, api_secret, acces_token, access_token_secret) -> None:
        auth = tweepy.OAuthHandler(api_key, api_secret)
        auth.set_access_token(acces_token, access_token_secret)
        self.api = tweepy.API(auth)

    @property
    def tweets(self):
        for t in tweepy.Cursor(self.api.user_timeline).items():
            yield t

    def tweet(self, message: str) -> tweepy.Models.Status:
        return self.api.update_status(message)

    def delete_tweet(self, tweet_id: int):
        self.api.destroy_status(tweet_id)
