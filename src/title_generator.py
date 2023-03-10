from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import nltk
nltk.download('punkt')

tokenizer = AutoTokenizer.from_pretrained("fabiochiu/t5-small-medium-title-generation")
model = AutoModelForSeq2SeqLM.from_pretrained("fabiochiu/t5-small-medium-title-generation")

max_input_length = 1000

def generate_title(text: str):
    inputs = ["summarize: " + text]
    inputs = tokenizer(inputs, max_length=max_input_length, truncation=True, return_tensors="pt")
    output = model.generate(**inputs, num_beams=8, do_sample=True, min_length=10, max_length=64)
    decoded_output = tokenizer.batch_decode(output, skip_special_tokens=True)[0]
    predicted_title = nltk.sent_tokenize(decoded_output.strip())[0]
    
    return predicted_title

