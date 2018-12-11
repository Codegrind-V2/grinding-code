from flask import Flask, render_template, request
from werkzeug import secure_filename
import os
import io
import config
import reducio as reducio



app = Flask(__name__)

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types


main_data = []

@app.route('/')
def hello():
     return "Hello, I'm the Server!"


def sort_data():
    global main_data
    print("sorted!")
    main_data = sorted(main_data, key=lambda k: k['time'])



@app.route('/getsummary',methods=['POST'])
def return_sumamry():
    text = ""
    for element in main_data:
        text += element['data']
    ans = reducio.reducio(text,3)
    print(ans)
    return ans


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
            name = filename.split('_')

            #print('response')
            print(str(response1))
            for result in response1.results:
                #print('Transcript: {}'.format(result.alternatives[0].transcript))
                dic = {'user':name[0] , 'time':name[1].split('.')[0] , 'data':format(result.alternatives[0].transcript)}
                print(dic)
                main_data.append(dic)
             
            print(main_data)
            sort_data()  
            return "File Uploaded!"
        else:
            return "Error"



if __name__ == '__main__':
    app.run(port=config.SERVER_PORT,debug=True,threaded=True)