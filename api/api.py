import base64
from flask import Flask
from flask import abort, jsonify, request
from io import BytesIO
import numpy as np
from flask_cors import CORS
from PIL import Image
from tensorflow.keras.models import Sequential, model_from_json
from skimage.transform import resize
import tensorflow
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.layers import Activation, Dropout, Flatten, Dense


app = Flask(__name__)
CORS(app)

# remove this if loading from json works
model = Sequential()
model.add(Conv2D(32, (3, 3), padding='same', input_shape=(32, 32, 3)))
model.add(Activation('relu'))
model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(64, (3, 3), padding='same'))
model.add(Activation('relu'))
model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(10))
model.add(Activation('softmax'))

opt = tensorflow.keras.optimizers.RMSprop(lr=0.0001, decay=1e-6)

model.compile(loss='categorical_crossentropy',
              optimizer=opt,
              metrics=['accuracy'])

model.load_weights('./model_weights.h5')

graph = tensorflow.keras.get_default_graph()
app.run(host='127.0.0.1', port=5000, threaded=False)


@app.route('/image', methods=['POST'])
def image():
    global graph
    with graph.as_default():
        if not request.json or not 'image' in request.json:
            abort(400)
        img_bytes = BytesIO(base64.b64decode(request.json['image']))
        img = np.array(Image.open(img_bytes))
        resized = resize(img, (32, 32), anti_aliasing='reflect', mode='reflect')
        resized_reshaped = resized.reshape(1, 32, 32, 3)
        print(resized_reshaped.shape)
        # TODO: fix this
        # multithreading problems?
        pred = model.predict(resized_reshaped)
        print(pred)
        return jsonify({'msg': '200 ok'})
