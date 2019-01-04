"""
https://bmwlog.pp.ua/post/count-your-probabilities-using-python
"""
import random

from itertools import count
import numpy as np
import matplotlib.pyplot as plt


def plot(trial, line=50.0):
    n = 10**4
    data_x = np.arange(1, n, 1)
    data_y = []
    success = 0
    for event in range(1, n):
        if trial() is True:
            success += 1
        data_y.append(success/event * 100)

    plt.yscale('linear')
    plt.ylim(0, 100)
    plt.axhline(y=line, color='r')
    plt.xscale('log')
    plt.plot(data_x, data_y)
    plt.show()


def ex1():
    win_probability = 0.4
    games = 5
    trials = [100, 10**3, 10**6]

    def wingame():
        return random.random() < win_probability

    def trial():
        for game in range(1, games+1):
            if wingame() is True:
                if game != 5:
                    return False
                return True
        return False

    for n in trials:
        success = 0
        for event in range(n):
            if trial() is True:
                success += 1
        print(n, success, success/n * 100)

    expected = 0.6**4 * 0.4 * 100
    plot(trial, line=expected)


def ex2():
    pass

def ex3():
    def winroll():
        return random.randint(1, 6) == 6

    def trial():
        for i in count():
            if winroll() is True:
                return i % 2 == 0

    trials = [100, 10**3, 10**6]
    for n in trials:
        success = 0
        for event in range(n):
            if trial() is True:
                success += 1
        print(n, success, success/n * 100)

    expected = 6/11 * 100
    plot(trial, line=expected)


def ex4():
    def roll():
        return random.randint(1, 20)

    def trial():
        # Alice's roll and Bill's roll
        return roll() > roll()

    trials = [100, 10**3, 10**6]
    for n in trials:
        success = 0
        for event in range(n):
            if trial() is True:
                success += 1
        print(n, success, success/n * 100)

    expected = 19/40 * 100
    plot(trial, line=expected)


if __name__ == '__main__':
    ex1()
    # ex3()
    # ex4()
