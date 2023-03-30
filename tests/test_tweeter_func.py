from src.tweeter import tweet, delete_tweets
from collections import namedtuple
import unittest
import mock
import datetime

StatusTest = namedtuple('StatusTest', ['id'])


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
