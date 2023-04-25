import pytest
from src.summarizer import Summarizer




class TestSummarizer:

    def test_make_tweet(self):
        summarizer = Summarizer()
        text = "This is a long text that needs to be summarized into a tweet. It contains many words and sentences that will need to be condensed into a short summary."
        summarizer.make_tweet(text)
        tweet_content = summarizer.get_content()
        assert isinstance(tweet_content, str)
        assert len(tweet_content) <= 280
        assert len(tweet_content) > 0

    def test_make_tweet_short_text(self):
        summarizer = Summarizer()
        text = "This is a short text."
        summarizer.make_tweet(text)
        tweet_content = summarizer.get_content()
        assert isinstance(tweet_content, str)
        assert len(tweet_content) <= 280
        assert len(tweet_content) > 0

    def test_get_content(self):
        summarizer = Summarizer()
        text = "This is a long text that needs to be summarized into a tweet. It contains many words and sentences that will need to be condensed into a short summary."
        summarizer.make_tweet(text)
        tweet_content = summarizer.get_content()
        assert isinstance(tweet_content, str)
        assert len(tweet_content) <= 280
        assert len(tweet_content) > 0

    def test_summarize(self):
        summarizer = Summarizer()
        text = "This is a long text that needs to be summarized into a tweet. It contains many words and sentences that will need to be condensed into a short summary."
        summarizer._Summarizer__summarize(text)
        summary_text = summarizer._Summarizer__summary_text
        assert isinstance(summary_text, str)
        assert len(summary_text) <= 280
        assert len(summary_text) > 0

    def test_generate_title(self):
        summarizer = Summarizer()
        text = "This is a long text that needs to be summarized into a tweet. It contains many words and sentences that will need to be condensed into a short summary."
        summarizer._Summarizer__generate_title(text)
        title = summarizer._Summarizer__title
        assert isinstance(title, str)
        assert len(title) <= 100
        assert len(title) > 0