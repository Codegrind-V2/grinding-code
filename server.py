from flask import Flask, render_template, request
from werkzeug import secure_filename
import os
import config
app = Flask(__name__)


@app.route('/')
def hello():
     return "Hello, I'm the Server!"


@app.route('/upload', methods = ['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(config.UPLOAD_LOC, filename))
            return "File Uploaded!"
        else:
            return "Error"

if __name__ == '__main__':
    app.run(port=config.SERVER_PORT,debug=True)