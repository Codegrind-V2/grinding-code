from flask import Flask
import requests
import config
app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello, I'm a Client!"

@app.route('/sendfile')
def sendFile():
    headers = {
    'content-type': 'image/jpeg'
    }
    fin = open('speech.raw', 'rb')
    files = {'file': fin} 
    requests.post('http://'+config.SERVER_ADDRESS+':'+config.SERVER_PORT+'/upload', files=files)
    return 'success'

if __name__ == '__main__':
    app.run(port=config.CLIENT_PORT,debug=True)