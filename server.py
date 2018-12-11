from flask import Flask, render_template, request
from werkzeug import secure_filename
import os
import io
import config
app = Flask(__name__)

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

@app.route('/')
def hello():
     return "Hello, I'm the Server!"


@app.route('/upload', methods = ['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            print("here")
            filename = secure_filename(file.filename)
            file.save(os.path.join(config.UPLOAD_LOC, filename))

            # The name of the audio file to transcribe
            file_name = os.path.join(
                os.path.dirname(__file__),
                    'files',
                    filename)

            client = speech.SpeechClient()
            # Loads the audio into memory
            with io.open(file_name, 'rb') as audio_file:
                content = audio_file.read()
                audio = types.RecognitionAudio(content=content)

            config_google = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=44100,
            language_code='en-US')

            # Detects speech in the audio file
            response1 = client.recognize(config_google, audio)

            #print('response')
            print(str(response1))
            for result in response1.results:
                print('Transcript: {}'.format(result.alternatives[0].transcript))

            
            return "File Uploaded!"
        else:
            return "Error"

if __name__ == '__main__':
    app.run(port=config.SERVER_PORT,debug=True)