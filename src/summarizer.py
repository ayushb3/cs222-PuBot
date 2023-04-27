from settings import OPENAI_API_KEY
import openai
openai.api_key = OPENAI_API_KEY

class Summarizer:
    def __init__(self):
        self.__summary = None

    def __openai_summarize(self,text: str):
        prompt = f"Summarize the following text for a tweet: \n\n{text}\n"
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
        self.__summary = summary[1:]
    
    def make_tweet(self, text: str):
        self.__openai_summarize(text)

    def get_content(self):
        return self.__summary
