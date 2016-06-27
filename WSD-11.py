import json

import flask
from flask import Flask
import requests

app = Flask(__name__)


@app.route('/show_text_file')
def show_text_file():
    req = requests.get('https://stash.waveoc.com/rest/api/1.0/projects/WIR/repos/python-learning/browse/text_file.txt?'\
                       'at=refs/heads/feature/files')
    jsn = json.loads(req.text)

    text = ''
    for line in jsn['lines']:
        text += line['text'] + '\n'

    return flask.Response(text, status=200, mimetype='application/json')


if __name__ == '__main__':
    app.run()
