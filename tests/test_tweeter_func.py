from unittest import mock
from src.tweeter import Tweeter


def test_tweet():
    with mock.patch('tweepy.Client') as MockClient:
        mock_client = MockClient.return_value
        mock_tweet = mock.MagicMock()
        mock_client.create_tweet.return_value = mock_tweet

        tweeter = Tweeter('test_bearer_token', 'test_api_key',
                          'test_api_secret', 'test_access_token', 'test_access_token_secret')
        tweet_result = tweeter.tweet('test message')

        mock_client.create_tweet.assert_called_once_with(text='test message')
        assert tweet_result == mock_tweet


def test_delete_tweet():
    with mock.patch('tweepy.Client') as MockClient:
        mock_client = MockClient.return_value

        tweeter = Tweeter('test_bearer_token', 'test_api_key',
                          'test_api_secret', 'test_access_token', 'test_access_token_secret')
        tweeter.delete_tweet(12345)

        mock_client.delete_tweet.assert_called_once_with(12345)
