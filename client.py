from flask import Flask
import requests
import config
import pyaudio
import wave
import datetime
import sched,time

app = Flask(__name__)
s = sched.scheduler(time.time, time.sleep)

p = pyaudio.PyAudio()


def record_audio(time):
    stream = p.open(format=config.FORMAT,
                channels=config.CHANNELS,
                rate=config.RATE,
                input=True,
                frames_per_buffer=config.CHUNK)
    frames = []
    for i in range(0, int(config.RATE / config.CHUNK * time)):
        data = stream.read(config.CHUNK)
        frames.append(data)    
    cur_time = str(datetime.datetime.now().time())
    cur_time = cur_time.replace(":","").replace(".","")
    file_name = config.WAVE_OUTPUT_DIR + config.CLIENT_NAME+'_'+cur_time + ".raw"
    wf = wave.open(file_name,'wb')
    wf.setnchannels(config.CHANNELS)
    wf.setsampwidth(p.get_sample_size(config.FORMAT))
    wf.setframerate(config.RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    stream.stop_stream()
    stream.close()


    fin = open(file_name, 'rb')
    files = {'file': fin} 
    requests.post('http://'+config.SERVER_ADDRESS+':'+config.SERVER_PORT+'/upload', files=files)    
    s.enter(0, 1, record_audio, (time,))


# In[5]:






@app.route('/')
def hello():
    return "Hello, I'm a Client!"

s.enter(0, 1, record_audio, (config.RECORD_SECONDS,))
s.run()


if __name__ == '__main__':
    app.run(port=config.CLIENT_PORT,debug=True)