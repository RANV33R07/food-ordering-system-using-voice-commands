from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
from gtts import gTTS

app = Flask(__name__)

# Sample restaurant menu data
restaurants = {
    'Italian Bistro': ['Spaghetti', 'Lasagna', 'Pizza'],
    'Sushi House': ['Sushi', 'Tempura', 'Sashimi']
}

@app.route('/')
def index():
    return render_template('index.html', restaurants=restaurants)

@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_input = request.form['user_input']
    response = get_response(user_input)
    return jsonify({'response': response})

def get_response(user_input):
    if user_input in [item for sublist in restaurants.values() for item in sublist]:
        return f"We have {user_input} available for order."
    else:
        return "Sorry, we don't serve that item."

@app.route('/voice_input', methods=['POST'])
def voice_input():
    recognizer = sr.Recognizer()
    audio_file = request.files['audio']
    audio = sr.AudioFile(audio_file)
    with audio as source:
        audio_data = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio_data)
        return jsonify({'text': text})
    except sr.UnknownValueError:
        return jsonify({'error': 'Could not understand the audio'})
    except sr.RequestError:
        return jsonify({'error': 'Could not request results from speech recognition service'})

if __name__ == '__main__':
    app.run(debug=True)
