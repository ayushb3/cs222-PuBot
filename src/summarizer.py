import torch
from transformers import pipeline
from settings import MAX_TWEET_CONTENT_LENGTH

small_summarizer = pipeline(
    "summarization", model="facebook/bart-large-cnn", framework="pt")
large_summarizer = pipeline(
    "summarization", model="pszemraj/led-large-book-summary", framework="pt", device=0 if torch.cuda.is_available() else -1)


def summarize(text: str):
    """Summarize text using Hugging Face's transformers library."""
    if len(text) < 1024:
        return small_summarizer(text, max_length=MAX_TWEET_CONTENT_LENGTH, min_length=30, do_sample=False, truncation=True)[0]['summary_text']
    return large_summarizer(text, max_length=MAX_TWEET_CONTENT_LENGTH, min_length=30, do_sample=False, truncation=True)[0]['summary_text']
