import math
import numbers


class Term(object):
    def __init__(self, name, index, value=1):
        self.value = value
        self.name = name
        self.index = index

    def resolve(self, other):
        """Substitute term with another index or a number"""
        if isinstance(other, numbers.Real):
            return self.value * other
        return self * other

    def __mul__(self, other):
        cls = self.__class__
        print('Multiplying', self, other)
        return self

    def __truediv__(self, other):
        return self.__div__(other)

    def __div__(self, other):
        if not isinstance(other, numbers.Real):
            raise ValueError(f'Can be divided only by number got {type(other)}')
        cls = self.__class__
        return cls(
            name=self.name,
            index=self.index,
            value=self.value / other
        )

    def __add__(self, other):
        cls = self.__class__
        if other.index != self.index:
            raise ValueError('Cannot add different indexes')
        return cls(
            name=self.name,
            index=self.index,
            value=self.value+other.value,
        )

    def __str__(self):
        return f'{self.value}{self.name}_{self.index}'

    def __repr__(self):
        return str(self)


class Poly(object):
    def __init__(self, terms):
        self.terms = terms

    def resolve(self, index):
        # substitute know values
        res = []
        for t in self.terms:
            if not isinstance(t, numbers.Real) and t.index in _resolved_idx:
                resolved = t.resolve(_resolved_idx[t.index])
                res.append(resolved)
            else:
                res.append(t)

        # open brackets

        t_res0 = Term('P', index, 0)
        res0 = []  # i index

        t_next = Term('P', index+1, 0)
        res_next = []  # i+1 index
        for t in res:
            if not isinstance(t, numbers.Real) and t.index == index+1:
                res_next.append(t)
                t_next += t

        t_prev = Term('P', index-1, 0)
        res_prev = []  # i-1 index
        for t in res:
            if not isinstance(t, numbers.Real) and t.index == index-1:
                res_prev.append(t)
                t_prev += t

        for t in res:
            if not isinstance(t, numbers.Real) and t.index == index:
                res0.append(t)
                t_res0 += t
        # print(res_prev, res0, res_next)
        print(t_prev, t_res0, t_next)
        # add up numbers
        num = 0
        for t in res:
            if isinstance(t, numbers.Real):
                num += t

        poly = []
        if t_prev.value != 0:
            poly.append(t_prev)
        if t_next.value != 0:
            poly.append(t_next)
        if num != 0:
            poly.append(num)
        # express term with given index
        _resolved_idx[index] = Poly(poly) / -t_res0.value

    def __truediv__(self, other):
        return self.__div__(other)

    def __div__(self, other):
        if not isinstance(other, numbers.Real):
            raise ValueError('Can be divided only by number got')

        res = []
        for t in self.terms:
            res.append(t/other)
        return Poly(res)

    def __str__(self):
        return ' + '.join([str(t) for t in self.terms])

    def __repr__(self):
        return str(self)


_resolved_idx = {
    2: 1,
    -2: 0,
}


class P(object):
    def __init__(self, value=None, terms=None):
        self.value = value
        self.terms = terms or set()

    def __mul__(self, other):
        cls = self.__class__
        if isinstance(other, numbers.Real):
            return cls(value=self.value*other, terms=self.terms)
        return cls(
            value=self.value*other.value,
            terms=self.terms | other.terms,
        )

    def __rmul__(self, other):
        return self.__mul__(other)

    def __add__(self, other):
        cls = self.__class__
        if isinstance(other, numbers.Real):
            print('adding', other)
            return self + cls(value=other)

        if self.terms == other.terms:
            return cls(value=self.value+other.value, terms=self.terms)

        if other.value == 0:
            return self
        return cls(value=1, terms={str(self), str(other)})
        # print(self, '+', other)

    def __str__(self):
        terms = '*'.join(self.terms)
        return f'{self.value}{terms}'


def p_n(n, p, limit):
    if n == limit:
        return 1

    if n == -limit:
        return 0

    p_next = P(p, {f'P{n+1}'})
    print(p_next)
    return p_next + p_n(n-1, p, limit)*(1-p)


def test():
    p = [Term('P', 0, 5), Term('P', 0, 6)]
    print(sum(p))


def main():
    p = 0.6
    limit = 2
    stack = []
    stack.append(Poly([Term('P', 0, -1), Term('P', 1, p), Term('P', -1, 1-p)]))
    for i in range(1, limit):
        # P_i = p*P_{i+1} + (1-p)*P_{i-1}
        stack.append(Poly([Term('P', i, -1), Term('P', i+1, p), Term('P', i-1, 1-p)]))
        # P_{-i} = p*P_{-i+1} + (1-p)*P_{-i-1}
        stack.append(Poly([Term('P', -i, -1), Term('P', -i+1, p), Term('P', -i-1, 1-p)]))

    for step in reversed(range(limit*2-1)):
        sign = 1 if step % 2 else -1
        index = int(math.ceil(step/2))*sign
        poly = stack.pop()
        print('Step', step, 'Index', index, 'Resolving', poly)
        poly.resolve(index)
    # print(p_n(0, 0.6, 4))
    for key, value in _resolved_idx.items():
        print(key, '->', value)

    print('Probability is', _resolved_idx[0])


if __name__ == '__main__':
    # test()
    main()
