from flask import Flask, render_template, request
from werkzeug import secure_filename
import os
import io
import config
import reducio as reducio
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import json


app = Flask(__name__)


main_data = []

# main_data = [{'user':'usr1','time':'12','data':'yeah, I will take care of the resentation'},
#              {'user':'usr1','time':'13','data':'lets catch up on Friday'},
#              {'user':'usr2','time':'13','data':'lets catch up on Monday'},
#              {'user':'usr1','time':'14','data':'I will take the fix the repo'}]

@app.route('/')
def hello():
     return "Hello, I'm the Server!"


def sort_data():
    global main_data
    print("sorted!")
    main_data = sorted(main_data, key=lambda k: k['time'])


def get_words(text):
    return text.split(' ')

def match_words(w1,w2):
    if(w1.lower()==w2.lower()):
        return True
    return False

def check_for_prompt(text,type):
    words = get_words(text)
    for x in range(len(words)-1):
        val = 0
        for y in range(len(config.PROMPTS[type])):
            if(match_words(words[x+y],config.PROMPTS[type][y])):
                val += 1
        if(val==len(config.PROMPTS[type])):
            return True
    return False


def is_day(word):
    for day in config.DAYS:
        if(match_words(word,day)):
            return day
    return False

@app.route('/setupmeeting')
def setupmeeting():
    meetings = []
    for element in main_data:
        text = element['data']
        words = get_words(text)
        if(check_for_prompt(text,'MEETING_SETUP')):
            for x in range(len(words)):
                if(is_day(words[x])!=False):
                    meetings.append(is_day(words[x]))
    #print(meetings)
    return json.dumps(meetings)


@app.route('/getactionpoints' , methods=['GET'])
def get_action_points():
    actions = []
    username = request.args.get('user')
    for element in main_data:
        if(element['user']==str(username)):
            print(element)
            text = element['data']
            if(check_for_prompt(text,'ACTION')):
                actions.append(element['data'])
    return json.dumps(actions)



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
    app.run(port=config.SERVER_PORT,debug=True,threaded=True,host='0.0.0.0')