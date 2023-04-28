from settings import OPENAI_API_KEY
import openai
import tiktoken
openai.api_key = OPENAI_API_KEY

class Summarizer:
    def __init__(self):
        self.__summary = None

    def __openai_summarize(self,text: str):
        if len(text) > 2000:
            text = text[:2000]
        input_text = f"Please summarize the following text for a tweet and include some hashtags at the end:\n\n {text}\n"
        encoding = tiktoken.encoding_for_model('text-davinci-003')
        encoded_text = encoding.encode(input_text)
        prompt = encoding.decode(encoded_text)
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt= prompt,
            temperature=0.7,
            max_tokens=60,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=1
        )
        summary = response.choices[0]["text"]
        print(summary)
        self.__summary = summary[1:]
    
    def make_tweet(self, text: str):
        self.__openai_summarize(text)

    def get_content(self):
        return self.__summary
