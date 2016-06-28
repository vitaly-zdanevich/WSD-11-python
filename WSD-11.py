import json
import zipfile
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

    text = ''
    for line in jsn['lines']:
        text += line['text'] + '\n'

    return flask.Response(text, status=200, mimetype='application/json')


@app.route('/show_archive_files')
def show_archive_files():
    req = requests.get('https://stash.waveoc.com/projects/WIR/repos/python-learning/browse/Archive.zip'
                       '?at=refs/heads/feature/files&raw')

    archive = zipfile.ZipFile(BytesIO(req.content))

    with archive.open('Opportunity_Trigger.cls') as myfile:
        return flask.Response(myfile.read(), status=200, mimetype='text/text')

if __name__ == '__main__':
    app.run()
