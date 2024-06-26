import random
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
from googletrans import Translator

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

translator = Translator()

bot_name = "Sam"

def translate_to_english(text):
    translated = translator.translate(text, dest='en')
    return translated.text

def translate_to_original_language(text, dest_language):
    translated = translator.translate(text, dest=dest_language)
    return translated.text

def get_response(msg):
    # Check if the message is in English, if not, translate it to English
    detected_language = translator.detect(msg).lang
    if detected_language != 'en':
        msg = translate_to_english(msg)

    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                response = random.choice(intent['responses'])
                # Translate response back to the original language if needed
                if detected_language != 'en':
                    response = translate_to_original_language(response, detected_language)
                return response
    
    return "I do not understand..."