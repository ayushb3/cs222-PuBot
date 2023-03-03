from transformers import pipeline

summarizer = pipeline("summarization")


def summarize(text: str):
    """Summarize text using Hugging Face's transformers library."""
    return summarizer(text, max_length=100, min_length=30, do_sample=False)[0]['summary_text']
