"""
https://rubikscode.net/2018/10/01/introduction-to-restricted-boltzmann-machines/
Adapted from https://rubikscode.net/2018/10/22/implementing-restricted-boltzmann-machine-with-python-and-tensorflow/
python 3.5.6
tensorflow==1.12.0
"""
import tensorflow as tf
import numpy as np


class RBM(object):
    def __init__(self, visible_dim, hidden_dim, learning_rate, number_of_iterations):
        self._graph = tf.Graph()

        with self._graph.as_default():
            self._num_iter = number_of_iterations
            self._visible_biases = tf.Variable(
                tf.random_uniform([1, visible_dim], 0, 1, name='visible_biases'))
            self._hidden_biases = tf.Variable(
                tf.random_uniform([1, hidden_dim], 0, 1, name='hidden_biases')
            )
            self._hidden_states = tf.Variable(
                tf.zeros([1, hidden_dim], tf.float32, name='hidden_biases')
            )
            self._visible_cd_states = tf.Variable(
                tf.zeros([1, visible_dim], tf.float32, name='visible_biases')
            )
            self._hidden_cd_states = tf.Variable(
                tf.zeros([1, hidden_dim], tf.float32, name='hidden_biases')
            )
            self._weights = tf.Variable(
                tf.random_normal([visible_dim, hidden_dim], 0.01), name='weights')
            self._learning_rate = tf.Variable(
                tf.fill([visible_dim, hidden_dim], learning_rate), name='learning_rate'
            )

            self._input_sample = tf.placeholder(tf.float32, [visible_dim], name='input_sample')

            # Gibbs Sampling
            input_matrix = tf.transpose(
                tf.stack([self._input_sample for i in range(hidden_dim)])
            )
            _hidden_probabilities = tf.sigmoid(
                tf.add(tf.multiply(input_matrix, self._weights),
                       tf.stack([self._hidden_biases[0] for _ in range(visible_dim)]))
            )
            self._hidden_states = self.calculate_state(_hidden_probabilities)
            _visible_probabilities = tf.sigmoid(
                tf.add(
                    tf.multiply(self._hidden_states, self._weights),
                    tf.transpose(tf.stack([self._visible_biases[0] for _ in range(hidden_dim)]))
                )
            )
            self._visible_cd_states = self.calculate_state(_visible_probabilities)
            self._hidden_cd_states = self.calculate_state(
                tf.sigmoid(
                    tf.multiply(self._visible_cd_states, self._weights) + self._hidden_biases
                )
            )

            # CD
            positive_gradient_matrix = tf.multiply(input_matrix, self._hidden_states)
            negative_gradient_matrix = tf.multiply(self._visible_cd_states, self._hidden_cd_states)

            new_weights = self._weights
            new_weights.assign_add(
                tf.multiply(positive_gradient_matrix, self._learning_rate)
            )
            new_weights.assign_sub(
                tf.multiply(negative_gradient_matrix, self._learning_rate)
            )

            self._training = tf.assign(self._weights, new_weights)

            # Initialize session and run it
            self._sess = tf.Session()
            initialization = tf.global_variables_initializer()
            self._sess.run(initialization)

    def train(self, input_vectors):
        # number of epochs
        for iter_no in range(self._num_iter):
            for input_vec in input_vectors:
                self._sess.run(
                    self._training,
                    feed_dict={self._input_sample: input_vec},
                )

    def calculate_state(self, probability):
        return tf.floor(probability + tf.random_uniform(tf.shape(probability), 0, 1))


if __name__ == '__main__':
    rbm = RBM(visible_dim=4, hidden_dim=3, learning_rate=0.1, number_of_iterations=100)
    data = np.array([
        [0, 1, 1, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 1],
    ])
    rbm.train(data)
