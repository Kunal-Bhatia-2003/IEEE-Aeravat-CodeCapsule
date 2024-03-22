from flask import Flask, render_template, request
from googletrans import Translator

app = Flask(__name__)

# Function to translate text
def translate_text(text, target_language):
  translator = Translator()
  translated_text = translator.translate(text, dest=target_language)
  return translated_text.text

@app.route('/')
def index():
  # List of supported languages with their corresponding codes
  languages = {
      'mr': 'Marathi',
      'ta': 'Tamil',
      'te': 'Telugu',
      'bn': 'Bengali',
      'hi': 'Hindi',
      'en': 'English'
  }
  return render_template('index.html', languages=languages)

@app.route('/translate', methods=['POST'])
def translate():
  text = request.form['text']
  target_language = request.form['target_language']
  translated_text = translate_text(text, target_language)
  return render_template('result.html', text=text, translated_text=translated_text)

if __name__ == '__main__':
  app.run(debug=True)
