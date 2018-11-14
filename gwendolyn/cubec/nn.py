import numpy as np
import pandas as pd


def sigmoid(x):
    return 1.0 / (1 + np.exp(-x))


def sigmoid_derivative(x):
    return x * (1.0 - x)


class NeuralNetwork(object):
    def __init__(self, X, y):
        self.input = X

        self.layer1 = None
        self.weights1 = np.random.rand(X.shape[1], X.shape[0])
        self.weights2 = np.random.rand(X.shape[0], 1)

        self.y = y
        self.output = np.zeros(y.shape)

    def _feed_forward(self):
        self.layer1 = sigmoid(np.dot(self.input, self.weights1))
        self.output = sigmoid(np.dot(self.layer1, self.weights2))

    def _back_prop(self):
        diff = self.y - self.output
        out_deriv = sigmoid_derivative(self.output)
        d_weights2 = np.dot(
            self.layer1.T,
            2 * diff * out_deriv
        )

        product = np.dot(2*diff*out_deriv, self.weights2.T) * \
                  sigmoid_derivative(self.layer1)
        d_weights1 = np.dot(
            self.input.T,
            product
        )
        self.weights1 += d_weights1
        self.weights2 += d_weights2

    def fit(self):
        iterations = 1000
        print('Training network...')
        for _ in range(iterations):
            self._feed_forward()
            self._back_prop()

    def predict(self, x):
        layer1 = sigmoid(np.dot(x, self.weights1))
        output = sigmoid(np.dot(layer1, self.weights2))
        return output

    def accuracy(self, X_test, y_test):
        """RMSE accuracy, lower is better"""
        predictions = self.predict(X_test)
        return np.sqrt(((predictions - y_test) ** 2).mean())


def main():
    df = pd.read_csv('data.csv')
    size = int(len(df)*0.8)
    df_train = df[:size]
    df_test = df[size:]
    X_train = df_train[['x1', 'x2', 'x3', 'x4']].copy()
    y_train = df_train.filter(['y'], axis=1)

    X_test = df_test[['x1', 'x2', 'x3', 'x4']].copy()
    y_test = df_test.filter(['y'], axis=1)
    nn = NeuralNetwork(X_train, y_train)
    nn.fit()

    with np.printoptions(precision=3, suppress=True):
        print(nn.output)

    for (row, actual) in zip(X_test.values, y_test.values):
        print(nn.predict(row), actual)

    print('Accuracy (RMSE): {:.4}'.format(nn.accuracy(X_test, y_test)['y']))


if __name__ == '__main__':
    main()
