import numbers


_memory = {}


class X(object):
    """Representing unknown value which will be resolved in future"""
    def __init__(self, value=1.0):
        self.value = value

    def __add__(self, other):
        cls = self.__class__
        return cls(value=self.value+other.value)

    def __sub__(self, other):
        cls = self.__class__
        return cls(value=self.value-other.value)

    def __mul__(self, other):
        cls = self.__class__
        if isinstance(other, cls):
            return cls(value=self.value*other.value)
        elif isinstance(other, numbers.Real):
            return cls(value=self.value*other)
        else:
            raise TypeError(f'Cannot multiply with type {type(other)}')

    def __rmul__(self, other):
        return self.__mul__(other)

    def __str__(self):
        return f'{self.value}x'

    def __repr__(self):
        return str(self)


def fill_memory(n, p):
    _memory[(-n, -n)] = (0, X(0))
    _memory[(n, n)] = (1, X(0))

    for i in range(1-n, n):
        _memory[(i, i-1)] = 1-p
        _memory[(i, i+1)] = p


def resolve(n):
    for i in reversed(range(n)):
        # resolve right to center
        prob_next = _memory.get((i+1, i+1), (0, X(1)))
        prob_prev = _memory.get((i-1, i-1), (0, X(1)))

        # these values are pre-filled
        coef0 = _memory[(i, i-1)]  # it's just a 1-p
        coef1 = _memory[(i, i+1)]  # it's just a p

        _memory[(i, i)] = (
            coef0*prob_prev[0] + coef1*prob_next[0],
            coef0*prob_prev[1] + coef1*prob_next[1],
        )

        # resolve left to center
        prob_prev = _memory.get((-i-1, -i-1), (0, X(1)))
        prob_next = _memory.get((-i+1, -i+1), (0, X(1)))
        # using pre-filled values
        coef0 = _memory[(-i, -i-1)]
        coef1 = _memory[(-i, -i+1)]
        _memory[(-i, -i)] = (
            coef0*prob_prev[0] + coef1*prob_next[0],
            coef0*prob_prev[1] + coef1*prob_next[1],
        )

    # calculate base probability
    solution = _memory[(0, 0)]
    coef = (X(value=1) - solution[1]).value
    p = solution[0] / coef
    return p


def main():
    N = 4
    fill_memory(N, 0.6)
    p = resolve(N)
    print(f'Probability for N={N} steps is {p*100:.4}%')
    # for key, value in _memory.items():
    #     print(key, '->', value)


if __name__ == '__main__':
    main()

