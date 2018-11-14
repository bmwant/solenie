from itertools import product

import pandas as pd


def f(X):
    x1, x2, x3, x4 = X
    return (x1 or x2) and (x3 or x4)


def main():
    columns = ['x1', 'x2', 'x3', 'x4', 'y']
    data = []
    for elem in product([0, 1], repeat=4):
        row = [*elem, f(elem)]
        data.append(row)

    df = pd.DataFrame(data, columns=columns)
    df.to_csv('data.csv', header=True, index=False)


if __name__ == '__main__':
    main()
