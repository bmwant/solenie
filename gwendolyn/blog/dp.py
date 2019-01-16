import numbers


_memory = []


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


def fill_memory(n):
    global _memory
    _memory = [(0, X(1))]*(2*n+1)
    _memory[-n] = (0, X(0))
    _memory[n] = (1, X(0))


def resolve(n, p):
    q = 1-p
    for i in reversed(range(n)):
        # resolve from right to center
        prob_next = _memory[i+1]
        prob_prev = _memory[i-i]
        _memory[i] = (
            q*prob_prev[0] + p*prob_next[0],
            q*prob_prev[1] + p*prob_next[1],
        )

        # resolve from left to center
        prob_prev = _memory[-i-1]
        prob_next = _memory[-i+1]
        _memory[-i] = (
            q*prob_prev[0] + p*prob_next[0],
            q*prob_prev[1] + p*prob_next[1],
        )

    # calculate base probability
    solution = _memory[0]
    coef = (X(value=1) - solution[1]).value
    p0 = solution[0] / coef
    return p0


def main():
    N = 4
    p = 0.6
    fill_memory(N)
    p0 = resolve(N, p)
    print(f'Probability for N={N} steps is {p0*100:.4}%')
    for i in range(2*N+1):
        print(i-N, '->', _memory[i-N])


if __name__ == '__main__':
    main()

