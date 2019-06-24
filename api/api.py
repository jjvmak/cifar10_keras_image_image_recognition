import base64
from flask import Flask
from flask import abort, jsonify, request
from io import BytesIO
import numpy as np
from flask_cors import CORS
from PIL import Image
import tensorflow as tf
from skimage.transform import resize


app = Flask(__name__)
CORS(app)

# TODO: open from json
# model = tf.keras.models.load_model('model_1.h5')

@app.route('/image', methods=['POST'])
def image():
    if not request.json or not 'image' in request.json:
        abort(400)
    img_bytes = BytesIO(base64.b64decode(request.json['image']))
    img = np.array(Image.open(img_bytes))
    resized = resize(img, (32, 32), anti_aliasing='reflect', mode='reflect')
    resized = resized.reshape((1, 32, 32, 3))
    print(resized.shape)
    # TODO: fix this
    # print(model.predict(resized))
    return jsonify({'msg': '200 ok'})
