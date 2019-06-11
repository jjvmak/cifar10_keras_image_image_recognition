
from keras.datasets import cifar10
import pickle


def make_dumps():
    (x_train, y_train), (x_test, y_test) = cifar10.load_data()
    pickle.dump(x_test, open("x_test.p", "wb"))
    pickle.dump(x_train, open("x_train.p", "wb"))
    pickle.dump(y_test, open("y_test.p", "wb"))
    pickle.dump(y_train, open("y_train.p", "wb"))


def load_dump(dump_name):
    return pickle.load(open(dump_name, "rb"))


x_train = load_dump('x_train.p')
y_train = load_dump('y_train.p')
x_test = load_dump('x_test.p')
y_test = load_dump('y_test.p')
