
from keras.datasets import cifar10
import pickle
(x_train, y_train), (x_test, y_test) = cifar10.load_data()

pickle.dump(x_test, open("x_test.p", "wb"))
pickle.dump(x_train, open("x_train.p", "wb"))
pickle.dump(y_test, open("y_test.p", "wb"))
pickle.dump(y_train, open("y_train.p", "wb"))


