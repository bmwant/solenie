"""
Adapted from https://github.com/eriklindernoren/ML-From-Scratch/blob/master/mlfromscratch/unsupervised_learning/restricted_boltzmann_machine.py
"""

import numpy as np


class RBM(object):
    def __init__(self, n_hidden=128, learning_rate=0.1, batch_size=10, n_iterations=100):
        self.n_iterations = n_iterations
        self.batch_size = batch_size
        self.lr = learning_rate
        self.n_hidden = n_hidden
        # self.progressbar

    def _initialize_weights(self, X):
        n_visible = X.shape[1]
        self.W = np.random.normal(scale=0.1, size=(n_visible, self.n_hidden))
        self.v0 = np.zeros(n_visible)  # bias visible
        self.h0 = np.zeros(self.n_hidden)  # bias hidden

    def fit(self, X, y=None):
        self._initialize_weights(X)

        self.training_errors = []
        self.training_reconstructions = []
        for _ in self.progressbar(range(self.n_iterations)):
            batch_errors = []
            for batch in batch_iterator(X, batch_size=self.batch_size):
                # Positive phase
                positive_hidden = sigmoid(batch.dot(self.W) + self.h0)
                hidden_states = self._sample(positive_hidden)
                positive_associations = batch.T.dot(positive_hidden)

                # Negative phase
                negative_visible = sigmoid(hidden_states.dot(self.W.T) + self.v0)
                negative_visible = self._sample(negative_visible)
                negative_hidden = sigmoid(negative_visible.dot(self.W) + self.h0)
                negative_associations = negative_visible.T.dot(negative_hidden)

                self.W += self.lr * (positive_associations - negative_associations)
                self.h0 += self.lr * (positive_hidden.sum(axis=0) - negative_hidden.sum(axis=0))
                self.v0 += self.lr * (batch.sum(axis=0) - negative_visible.sum(axis=0))

                batch_errors.append(np.mean((batch - negative_visible) ** 2))

            self.training_errors.append(np.mean((batch - negative_visible) ** 2))
            idx = np.random.choice(range(X.shape[0]), self.batch_size)
            self.training_reconstructions.append(self.reconstruct(X[idx]))

    def _sample(self, X):
        return X > np.random.random_sample(size=X.shape)

    def reconstruct(self, X):
        positive_hidden = sigmoid(X.dot(self.W) + self.h0)
        hidden_states = self._sample(positive_hidden)
        negative_visible = sigmoid(hidden_states.dot(self.W.T) + self.v0)
        return negative_visible
