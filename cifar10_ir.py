
import tensorflow
import pickle
import numpy as np
from scipy import stats
from tensorflow.keras.models import Sequential, model_from_json
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.layers import Activation, Dropout, Flatten, Dense
from tensorflow.keras.utils import to_categorical


def make_dumps():
    (x_train, y_train), (x_test, y_test) = \
    tensorflow.keras.datasets.cifar10.load_data()
    pickle.dump(x_test, open("x_test.p", "wb"))
    pickle.dump(x_train, open("x_train.p", "wb"))
    pickle.dump(y_test, open("y_test.p", "wb"))
    pickle.dump(y_train, open("y_train.p", "wb"))


def load_dump(dump_name):
    return pickle.load(open(dump_name, "rb"))


def first_order_texture_measures(img):
    r = img[:, :, 0]
    g = img[:, :, 1]
    b = img[:, :, 2]

    r_mean = np.mean(r, axis=1)
    g_mean = np.mean(g, axis=1)
    b_mean = np.mean(b, axis=1)

    r_var = np.var(r, axis=1)
    g_var = np.var(g, axis=1)
    b_var = np.var(b, axis=1)

    fetures = np.concatenate(
        (r_mean, g_mean, b_mean, r_var, g_var, b_var), axis=0)

    return fetures.reshape(-1, len(fetures))


def extract_rgb_features(image_array):
    features = first_order_texture_measures(image_array[0])
    for i in range(len(image_array)):
        if (i != 0):
            print('viela ' + repr(i))
            features = np.concatenate((features, first_order_texture_measures(image_array[i])), axis=0)
    return features


x_train = load_dump('x_train.p')
y_train = load_dump('y_train.p')
x_test = load_dump('x_test.p')
y_test = load_dump('y_test.p')
y_train_cat = to_categorical(y_train)
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255

model = Sequential()
model.add(Conv2D(32, (3, 3), padding='same', input_shape=x_train.shape[1:]))
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

model.fit(x=x_train, y=y_train_cat, epochs=20)

filename = 'model_' + '1' + '.h5'
model.save(filename)
print('>Saved %s' % filename)

# saving as json
json_string = model.to_json()
open('./model_architecture.json', 'w').write(json_string)
model.save_weights('model_weights.h5')
