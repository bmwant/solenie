import keras
from keras.models import Sequential
from keras.layers import Dense
from ann_visualizer.visualize import ann_viz


def vis01():
    network = Sequential()

    network.add(Dense(units=1,
                      activation='sigmoid',
                      kernel_initializer='uniform',
                      input_dim=4))

    ann_viz(network, title='NN01')


def vis02():
    network = Sequential()

    # hidden Layer 1
    network.add(Dense(units=4,
                      activation='sigmoid',
                      kernel_initializer='uniform',
                      input_dim=4))

    # output
    network.add(Dense(units=1,
                      activation='sigmoid',
                      kernel_initializer='uniform'))

    ann_viz(network, title='NN02')


if __name__ == '__main__':
    vis01()
