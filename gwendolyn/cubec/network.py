# https://towardsdatascience.com/how-to-build-your-own-neural-network-from-scratch-in-python-68998a08e4f6
import numpy as np


def sigmoid(x):
    return 1.0/(1+ np.exp(-x))

def sigmoid_derivative(x):
    return x * (1.0 - x)


class NeuralNetwork(object):
    def __init__(self, X, y):
        self.input = X
        self.weights1 = np.random.rand(self.input.shape[1], 4)
        self.weights2 = np.random.rand(4,1)
        self.y = y
        self.output = np.zeros(y.shape)

    def feedforward(self):
        self.layer1 = sigmoid(np.dot(self.input, self.weights1))
        self.output = sigmoid(np.dot(self.layer1, self.weights2))

    def backprop(self):
        # application of the chain rule to find derivative of
        # the loss function with respect to weights2 and weights1
        d_weights2 = np.dot(
            self.layer1.T,
            (2*(self.y - self.output) * sigmoid_derivative(self.output))
        )
        d_weights1 = np.dot(
            self.input.T,
            (np.dot(2*(self.y - self.output) * sigmoid_derivative(self.output), self.weights2.T) * sigmoid_derivative(self.layer1))
        )

        # update the weights with the derivative (slope) of the loss function
        self.weights1 += d_weights1
        self.weights2 += d_weights2

    def predict(self, x):
        layer1 = sigmoid(np.dot(x, self.weights1))
        output = sigmoid(np.dot(layer1, self.weights2))
        return output


def main():
    X = np.array([[0,0,1],
                  [0,1,1],
                  [1,0,1],
                  [1,1,1]])
    y = np.array([[0],[1],[1],[0]])
    nn = NeuralNetwork(X, y)

    for i in range(1500):
        nn.feedforward()
        nn.backprop()

    print(nn.output)
    x_seen = np.array([0, 0, 1])
    print(nn.predict(x_seen))
    x_unseen = np.array([0, 1, 0])
    print(nn.predict(x_unseen))


if __name__ == '__main__':
    main()
