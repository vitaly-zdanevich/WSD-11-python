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

    text = ''
    for line in jsn['lines']:
        text += line['text'] + '\n'

    return flask.Response(text, status=200, mimetype='text/text')


@app.route('/show_archive_files')
def show_archive_files():
    req = requests.get('https://stash.waveoc.com/projects/WIR/repos/python-learning/browse/Archive.zip'
                       '?at=refs/heads/feature/files&raw')

    archive = zipfile.ZipFile(BytesIO(req.content))

    content = '<html><head></head><body><div>'
    with archive.open('Opportunity_Trigger.cls') as myfile:
        content += str(myfile.readlines()) \
            .replace('\\n\', b\'}\']', "<br>}") \
            .replace("\\n', b'", "<br>") \
            .replace('\\n", b"', "<br>") \
            .replace('\\n\', b"', '<br>') \
            .replace('\\n", b\'', '<br>') \
            .replace('[b\'', '<br>') \
            .replace(' ', '&nbsp;')
        # TODO you know better solution?

    content += '</div><br><br><img src=\'data:image/jpg;base64,'
    with archive.open('Bonus_Image.jpg', 'r') as myimage:
        content += str((base64.b64encode(myimage.read()))).replace('b\'', '').replace('/9k=', '')

    content += "/></body></html>"
    return flask.Response(content, status=200, mimetype='text/html')

if __name__ == '__main__':
    app.run()
