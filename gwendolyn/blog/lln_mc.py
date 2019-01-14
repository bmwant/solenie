"""
https://bmwlog.pp.ua/post/generating-events-to-count-probabilities-with-python
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


def f(n):
    """Factorial"""
    if n == 0 or n == 1:
        return 1
    return n*f(n-1)


def C(n, k):
    """Combinations"""
    return f(n) / (f(k) * f(n-k))


def P(n, p):
    result = 0
    for i in range(n):
        result += C(n-1+i, i) * p**n * (1-p)**i
    return result


def ex2():
    win_probability = 0.6

    def wingame():
        return random.random() < win_probability

    win_score = 4

    def trial():
        ascore = 0
        bscore = 0
        while True:
            if wingame() is True:
                ascore += 1
            else:
                bscore += 1
            if ascore == win_score:
                return True
            if bscore == win_score:
                return False

    trials = [10**6]
    for n in trials:
        success = 0
        for event in range(n):
            if trial() is True:
                success += 1
        print(n, success, success/n * 100)


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
    # ex1()
    # ex3()
    # ex4()
    ex2()
    print(P(4, 0.6))
