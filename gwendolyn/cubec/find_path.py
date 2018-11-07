import queue


class Cube(object):
    def __init__(
        self,
        front: int,
        back: int,
        bottom: int,
        top: int,
        left: int,
        right: int
    ):
        self.front = front
        self.back = back
        self.bottom = bottom
        self.top = top
        self.left = left
        self.right = right

    @property
    def value(self):
        return self.bottom

    def move_right(self):
        cls = self.__class__
        return cls(
            front=self.front,
            back=self.back,
            bottom=self.right,
            top=self.left,
            left=self.bottom,
            right=self.top,
        )

    def move_left(self):
        cls = self.__class__
        return cls(
            front=self.front,
            back=self.back,
            bottom=self.left,
            top=self.right,
            left=self.top,
            right=self.bottom,
        )

    def move_forward(self):
        cls = self.__class__
        return cls(
            front=self.bottom,
            back=self.top,
            bottom=self.back,
            top=self.front,
            left=self.left,
            right=self.right,
        )

    def move_backward(self):
        cls = self.__class__
        return cls(
            front=self.top,
            back=self.bottom,
            bottom=self.front,
            top=self.back,
            left=self.left,
            right=self.right,
        )

    def __str__(self):
        return (
            ' {}\n'
            ' {}\n'
            '{}{}{}\n'
            ' {}\n'
        ).format(
            self.top,
            self.back,
            self.left, self.bottom, self.right,
            self.front,
        )


class Position(object):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def forward(self):
        cls = self.__class__
        return cls(x=self.x, y=self.y+1)

    def backward(self):
        cls = self.__class__
        return cls(x=self.x, y=self.y-1)

    def left(self):
        cls = self.__class__
        return cls(x=self.x-1, y=self.y)

    def right(self):
        cls = self.__class__
        return cls(x=self.x+1, y=self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash((self.x, self.y))


class Game(object):

    REVERSED_DIRECTIONS_ABBR = {
        'backward': 'F',
        'left': 'R',
        'forward': 'B',
        'right': 'L',
    }

    def __init__(self, initial_state: Cube, start: Position, end: Position):
        self.initial_state = initial_state
        self.start = start
        self.end = end
        self.map = dict()
        self.queue = queue.Queue()
        self._min_score = float('inf')

    def solve(self):
        self.queue.put((self.start, self.initial_state))
        self.map[self.start] = self.initial_state.value

        while not self.queue.empty():
            pos, state = self.queue.get()
            min_score = self.map[pos]
            if pos == self.end and min_score < self._min_score:
                self._min_score = min_score

            # moving in positive directions first
            for direction in ('forward', 'right', 'backward', 'left'):
                new_pos = getattr(pos, direction)()
                move_method = f'move_{direction}'
                new_state = getattr(state, move_method)()
                new_value = min_score + new_state.value
                current_value = self.map.get(new_pos, self._min_score)
                # Continue path only if it is cheaper
                if new_value <= current_value:
                    self.map[new_pos] = new_value
                    self.queue.put((new_pos, new_state))

        return self._min_score

    def _get_min_direction(self, pos):
        min_score = float('inf')
        min_direction = None
        for direction in ('backward', 'left', 'forward', 'right'):
            new_pos = getattr(pos, direction)()
            if self.map.get(new_pos, min_score) < min_score:
                min_score = self.map[new_pos]
                min_direction = direction

        return min_direction

    def get_path(self):
        if self._min_score == float('inf') or not self.map:
            raise RuntimeError('No solution! '
                               'Have you solved the game already?')
        pos = self.end
        path = [f'{self.end}[{self._min_score}] DONE!']
        while pos != self.start:
            min_direction = self._get_min_direction(pos)
            pos = getattr(pos, min_direction)()
            move = self.REVERSED_DIRECTIONS_ABBR[min_direction]
            score = self.map[pos]
            path.append(f'{pos}[{score}] -> {move}')

        return reversed(path)


def main():
    cube = Cube(
        front=1,
        back=6,
        bottom=5,
        top=2,
        left=3,
        right=4,
    )
    start = Position(2, 2)
    end = Position(2, 20)
    game = Game(initial_state=cube, start=start, end=end)
    print(game.solve())
    print('\n'.join(game.get_path()))


if __name__ == '__main__':
    main()
