import base64
from flask import Flask
from flask import abort, jsonify, request
from PIL import Image
from io import BytesIO
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/image', methods=['POST'])
def image():
    if not request.json or not 'image' in request.json:
        abort(400)
    #print(request.json['image'])
    # TODO: solve the padding problem
    #img_bytes = BytesIO(base64.b64decode(request.json['image']))
    #img = np.array(Image.open(img_bytes)).transpose()
    return jsonify({'msg': '200 ok'})
