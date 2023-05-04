import pytest
from src.summarizer import Summarizer


def test_summarizer_make_tweet():
    summarizer = Summarizer()
    text = "Coffee is a popular beverage consumed around the world. It is made by brewing roasted and ground coffee beans, which are typically sourced from various regions across the globe. Coffee is known for its stimulating effects due to the presence of caffeine, which can help improve alertness, focus, and mood. In addition to its functional benefits, coffee is also appreciated for its unique flavor and aroma, which can vary depending on factors such as the type of coffee bean, the roasting process, and the brewing method. Whether enjoyed as a morning ritual or a midday pick-me-up, coffee is a staple in many people's daily routines."
    summarizer.make_tweet(text)
    assert len(summarizer.get_content()) <= 280
    assert "#" in summarizer.get_content()
