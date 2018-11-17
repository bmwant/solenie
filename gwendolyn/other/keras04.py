import os
import random
import pickle
import argparse

import matplotlib
matplotlib.use('Agg')

from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from keras.models import Sequential
from keras.layers.core import Dense
from keras.optimizers import SGD
from imutils import paths

import cv2
import numpy as np
import matplotlib.pyplot as plt


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dataset', required=True,
                        help='path to input dataset of images')
    parser.add_argument('-m', '--model', required=True,
                        help='path to output trained model')
    parser.add_argument('-l', '--label-bin', required=True,
                        help='path to output label binarizer')
    parser.add_argument('-p', '--plot', required=True,
                        help='path to output accuracy/loss plot')
    args = vars(parser.parse_args())
    return args


def load_images(dataset):
    print('Loading images...')
    data = []
    labels = []
    image_paths = sorted(list(paths.list_images(dataset)))
    random.seed(42)
    random.shuffle(image_paths)

    for image_path in image_paths:
        image = cv2.imread(image_path)
        image = cv2.resize(image, (32, 32)).flatten()
        data.append(image)

        label = image_path.split(os.path.sep)[-2]
        labels.append(label)

    data = np.array(data, dtype='float') / 255.0
    labels = np.array(labels)
    return data, labels


def create_model(num_classes):
    model = Sequential()
    model.add(Dense(1024, input_shape=(3072,), activation='sigmoid'))
    model.add(Dense(512, activation='sigmoid'))
    model.add(Dense(num_classes, activation='softmax'))

    return model


def save_model(model, model_path, lb, lb_path):
    model.save(model_path)
    with open(lb_path, 'wb') as f:
        f.write(pickle.dumps(lb))


def main():
    args = parse_args()
    data, labels = load_images(args['dataset'])
    (X_train, X_test, Y_train, Y_test) = train_test_split(
        data, labels, test_size=0.25, random_state=42)

    lb = LabelBinarizer()
    Y_train = lb.fit_transform(Y_train)
    Y_test = lb.transform(Y_test)
    num_classes = lb.classes_

    INIT_LR = 0.01
    EPOCHS = 75
    model = create_model(num_classes)
    print('Training network...')
    opt = SGD(lr=INIT_LR)
    # binary_crossentropy for 2-class classification
    model.compile(loss='categorical_crossentropy', optimizer=opt,
                  metrics=['accuracy'])

    H = model.fit(X_train, Y_train, validation_data=(X_test, Y_test),
                  epochs=EPOCHS, batch_size=32)

    print('Evaluating network...')
    predictions = model.predict(X_test, batch_size=32)
    print(classification_report(Y_test.argmax(axis=1),
                                predictions.argmax(axis=1),
                                target_names=lb.classes_))
    N = np.arange(0, EPOCHS)
    plt.style.use('ggplot')
    plt.figure()
    plt.plot(N, H.history['loss'], label='train_loss')
    plt.plot(N, H.history['val_loss'], label='val_loss')
    plt.plot(N, H.history['acc'], label='train_acc')
    plt.plot(N, H.history['val_acc'], label='val_acc')
    plt.title('Training Loss and Accuracy (Simple NN)')
    plt.xlabel('Epoch #')
    plt.ylabel('Loss/Accuracy')
    plt.legend()
    plt.savefig(args['plot'])


if __name__ == '__main__':
    main()
