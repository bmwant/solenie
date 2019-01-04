"""
https://bmwlog.pp.ua/post/count-your-probabilities-using-python
"""
from itertools import count, permutations, islice, product


def is_white(num):
    return num % 2

def is_black(num):
    return not is_white(num)

def same_color(num, other):
    return num % 2 == other % 2

def same_color_pair(pair):
    return pair[0] % 2 == pair[1] % 2

def same_first_and_third(triple):
    return same_color(triple[0], triple[2])

def eight_heads(flips):
    return flips.count(1) == 8

def all_red_marbles(triple):
    return triple[0] % 2 == triple[1] % 2 == triple[2] % 2 == 1

def ex1():
    black_beads = list(islice(filter(is_black, count()), 6))
    white_beads = list(islice(filter(is_white, count()), 10))
    beads = [*black_beads, *white_beads]
    outcomes = list(permutations(beads, 2))
    successful_outcomes = list(filter(same_color_pair, outcomes))
    print(len(successful_outcomes) / len(outcomes))


def ex2():
    beads = list(islice(count(), 10))
    outcomes = list(permutations(beads, 3))
    successful_outcomes = list(filter(same_first_and_third, outcomes))
    print('{}/{}'.format(len(successful_outcomes), len(outcomes)))


def ex3():
    outcomes = list(product([1, 0], repeat=10))
    successful_outcomes = list(filter(eight_heads, outcomes))
    print('{}/{}'.format(len(successful_outcomes), len(outcomes)))


def ex4():
    blue_marbles = list(islice(filter(is_black, count()), 10))
    red_marbles = list(islice(filter(is_white, count()), 7))
    marbles = [*blue_marbles, *red_marbles]
    outcomes = list(permutations(marbles, 3))
    successful_outcomes = list(filter(all_red_marbles, outcomes))
    print('{}/{}'.format(len(successful_outcomes), len(outcomes)))


if __name__ == '__main__':
    # ex1()
    # ex2()
    # ex3()
    ex4()
