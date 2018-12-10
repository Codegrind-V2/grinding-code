from flask import Flask
import requests
import config
app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello, I'm a Client!"

@app.route('/sendfile')
def sendFile():
    requests.post('http://'+config.SERER_ADDRESS+':'+config.SERVER_PORT, files={'file': ('image.jpg', open('image.jpg', 'rb'))})
    return 'success'

if __name__ == '__main__':
    app.run(port=config.CLIENT_PORT,debug=True)