from src.tweeter import tweet, delete_tweets, scheduled_tweeter
from collections import namedtuple
import unittest
import mock
import datetime

StatusTest = namedtuple('StatusTest', ['id'])
ArticleTest = namedtuple('ArticleTest', ['id', 'message', 'date'])

class TestTweeter(unittest.TestCase):
    @mock.patch('tweepy.API')
    def test_tweet(self, mock_api):
        tweet(mock_api, 'This is a test tweet', '2023-03-24 05:05:05')
        tweet_time = datetime.datetime.strptime(
            '2023-03-24 05:05:05', '%Y-%m-%d %H:%M:%S')
        mock_api.update_status.assert_called_with(
            'This is a test tweet', scheduled_at=tweet_time)

        tweet(mock_api, 'This is a test tweet')
        mock_api.update_status.assert_called_with('This is a test tweet')

    @mock.patch('tweepy.API')
    def test_delete_tweets(self, mock_api):
        test_ids = [StatusTest(1), StatusTest(2), StatusTest(3)]
        delete_tweets(mock_api, test_ids)
        mock_api.destroy_status.assert_has_calls(
            [mock.call(test.id) for test in test_ids], any_order=True)

    @mock.patch('tweepy.API')
    def test_scheduled_tweeter(self, mock_api):
        mock_item = ArticleTest(1, 'This is a test tweet', None)
        mock_tweets = [mock_item]

        scheduled_tweeter(mock_tweets)

        mock_api.update_status.assert_called_with('This is a test tweet')
        mock_api.destroy_status.assert_called_with(1)