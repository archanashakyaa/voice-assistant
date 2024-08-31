from flask import Flask, render_template, request
import speech_recognition as sr
from gtts import gTTS
import os

app = Flask(_name_)

# Initialize recognizer class (for recognizing the speech)
r = sr.Recognizer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    if request.method == 'POST':
        # Check if the POST request has the file part
        if 'file' not in request.files:
            return "No file part"

        file = request.files['file']

        # If the user does not select a file, the browser submits an empty file without a filename.
        if file.filename == '':
            return "No selected file"

        # Process the audio file with SpeechRecognition
        try:
            with sr.AudioFile(file) as source:
                audio = r.record(source)
                text = r.recognize_google(audio)
                response_text = handle_command(text)
                tts = gTTS(text=response_text, lang='en')
                tts.save("response.mp3")
                return response_text
        except Exception as e:
            return str(e)

def handle_command(command):
    # Define simple command responses
    if "hello" in command.lower():
        return "Hello! How can I help you?"
    elif "how are you" in command.lower():
        return "I'm a voice assistant. I am always good."
    else:
        return "Sorry, I didn't understand that command."

if _name_ == "_main_":
    app.run(debug=True)