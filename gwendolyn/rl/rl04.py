import tensorflow as tf
import tensorflow.contrib.slim as slim

import numpy as np



class ContextualBandit(object):
    def __init__(self):
        self.state = 0
        self.bandits = np.array([
            [0.2, 0, -0.0, -5],
            [0.1, -5, 1, 0.25],
            [-5, 5, 5, 5],
        ])
        self.num_bandits = self.bandits.shape[0]
        self.num_actions = self.bandits.shape[1]

    def get_bandit(self):
        self.state = np.random.randint(0, len(self.bandits))
        return self.state
