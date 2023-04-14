import torch
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from settings import MAX_TWEET_CONTENT_LENGTH, MAX_TITLE_LENGTH
import nltk

class Summarizer:
    def __init__(self):
        self.small_summarizer = pipeline(
            "summarization", model="facebook/bart-large-cnn", framework="pt")
        self.large_summarizer = pipeline(
            "summarization", model="pszemraj/led-large-book-summary", framework="pt", device=0 if torch.cuda.is_available() else -1)
        self.tokenizer = AutoTokenizer.from_pretrained(
            "fabiochiu/t5-small-medium-title-generation")
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            "fabiochiu/t5-small-medium-title-generation")

        self.max_input_length = 1000
        self.summary_text = None
        self.title = None

    def summarize(self,text: str):
        """Summarize text using Hugging Face's transformers library."""
        if len(text) < 1024:
            self.summary_text = self.small_summarizer(text, max_length=MAX_TWEET_CONTENT_LENGTH, min_length=30, do_sample=False, truncation=True)[0]['summary_text']
        self.summary_text = self.large_summarizer(text, max_length=MAX_TWEET_CONTENT_LENGTH, min_length=30, do_sample=False, truncation=True)[0]['summary_text']
    
    def generate_title(self,text: str):
        nltk.download('punkt', quiet=True)
        inputs = ["summarize: " + text]
        inputs = self.tokenizer(inputs, max_length=self.max_input_length,
                           truncation=True, return_tensors="pt")
        output = self.model.generate(**inputs, num_beams=8, do_sample=True,
                                min_length=10, max_length=MAX_TITLE_LENGTH)
        decoded_output = self.tokenizer.batch_decode(
            output, skip_special_tokens=True)[0]
        predicted_title = nltk.sent_tokenize(decoded_output.strip())[0]

        self.title = predicted_title
    
small_summarizer = pipeline(
    "summarization", model="facebook/bart-large-cnn", framework="pt")
large_summarizer = pipeline(
    "summarization", model="pszemraj/led-large-book-summary", framework="pt", device=0 if torch.cuda.is_available() else -1)


def summarize(text: str):
    """Summarize text using Hugging Face's transformers library."""
    if len(text) < 1024:
        return small_summarizer(text, max_length=MAX_TWEET_CONTENT_LENGTH, min_length=30, do_sample=False, truncation=True)[0]['summary_text']
    return large_summarizer(text, max_length=MAX_TWEET_CONTENT_LENGTH, min_length=30, do_sample=False, truncation=True)[0]['summary_text']
