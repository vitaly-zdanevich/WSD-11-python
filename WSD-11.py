import json
import zipfile
import base64
from io import BytesIO

import flask
from flask import Flask

import requests

app = Flask(__name__)


@app.route('/show_text_file')
def show_text_file():
    req = requests.get('https://stash.waveoc.com/rest/api/1.0/projects/WIR/repos/python-learning/browse/text_file.txt?'
                       'at=refs/heads/feature/files')
    jsn = json.loads(req.text)

    text = '\n'.join([line['text'] for line in jsn['lines']])

    return flask.Response(text, status=200, mimetype='text/text')


@app.route('/show_archive_files')
def show_archive_files():
    req = requests.get('https://stash.waveoc.com/projects/WIR/repos/python-learning/browse/Archive.zip'
                       '?at=refs/heads/feature/files&raw')

    archive = zipfile.ZipFile(BytesIO(req.content))

    with archive.open('Opportunity_Trigger.cls') as myfile:
        text_file = ''.join([line.decode() for line in myfile.readlines()])

    with archive.open('Bonus_Image.jpg', 'r') as myimage:
        image = base64.b64encode(myimage.read()).decode()

    return flask.render_template('page.html', text_file=text_file, image=image)

if __name__ == '__main__':
    app.run(debug=True)
