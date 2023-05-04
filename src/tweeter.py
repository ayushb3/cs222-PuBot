import tweepy


class Tweeter:
    def __init__(self, bearer_token, api_key, api_secret, access_token, access_token_secret) -> None:
        self.api = tweepy.Client(
            bearer_token, api_key, api_secret, access_token, access_token_secret)

    def tweet(self, message: str):
        return self.api.create_tweet(text=message).data

    def delete_tweet(self, tweet_id: int):
        self.api.delete_tweet(tweet_id)

    # def update_tweet(self, tweet_id: int, message: str):
    #     self.api.update_status(message, in_reply_to_status_id=tweet_id)
