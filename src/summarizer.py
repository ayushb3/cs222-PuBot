import random
import openai
import tiktoken
from spacy_download import load_spacy
from settings import OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY


class Summarizer:
    max_tokens = 4096
    output_tokens = 55

    def __init__(self, prompt="Please summarize the following text for a tweet of max 280 characters and include some hashtags at the end:\n\n %s\n"):
        self.nlp = load_spacy('en_core_web_sm')
        self.encoding = tiktoken.encoding_for_model(
            'text-davinci-003')
        self.prompt = prompt
        self.max_input_tokens = self.max_tokens - \
            self.__num_tokens(self.prompt) - self.output_tokens
        self.__summary = None

    def __num_tokens(self, text: str) -> int:
        return len(self.encoding.encode(text))

    def __get_chunk(self, text: str):
        total_tokens = self.__num_tokens(text)
        if total_tokens <= self.max_input_tokens:
            return text
        ratio = self.max_input_tokens / total_tokens
        sentences = self.nlp(text)
        chunk = ""
        for sentence in sentences.sents:
            if random.random() > ratio:
                continue
            add = sentence.text
            if chunk:
                add = " " + add
            if self.__num_tokens(chunk + add) > self.max_input_tokens:
                break
            chunk += add
        return chunk

    def __openai_summarize(self, text: str):
        chunk = self.__get_chunk(text)
        input_text = self.prompt % chunk
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=input_text,
            temperature=0.75,
            max_tokens=self.output_tokens,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=1
        )
        summary = response.choices[0]["text"]
        self.__summary = summary[1:]

    def make_tweet(self, text: str):
        self.__openai_summarize(text)

    def get_content(self):
        return self.__summary
