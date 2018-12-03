# https://github.com/korolvs/snake_nn
# workon solenie3.5
import curses
from random import randint


class SnakeGame(object):
    def __init__(self, board_width=20, board_height=20, gui=False):
        self.score = 0
        self.done = False
        self.snake = []
        self.board = {'width': board_width, 'height': board_height}
        self.gui = gui
        self.food = None
        self.scr = None
        self.win = None

    def start(self):
        self.snake_init()
        self.generate_food()
        if self.gui:
            self.render_init()
        return self.generate_observations()

    def snake_init(self):
        x = randint(5, self.board["width"] - 5)
        y = randint(5, self.board["height"] - 5)
        vertical = randint(0, 1) == 0
        # Initial length is 3
        for i in range(3):
            point = [x + i, y] if vertical else [x, y + i]
            self.snake.insert(0, point)

    def generate_food(self):
        food = []
        while not food:
            food = [randint(1, self.board["width"]), randint(1, self.board["height"])]
            if food in self.snake: food = []
        self.food = food

    def render_init(self):
        self.scr = curses.initscr()
        curses.cbreak()
        curses.noecho()
        # curses.start_color()
        win = curses.newwin(self.board["width"] + 2, self.board["height"] + 2, 0, 0)
        curses.curs_set(0)
        win.nodelay(1)  # non-blocking key press reading
        win.timeout(200)
        self.win = win
        self.render()

    def render(self):
        self.win.erase()
        self.win.border(0)
        self.win.addstr(0, 2, 'Score: {}'.format(self.score))
        # an apple
        self.win.addch(self.food[0], self.food[1], '@')

        head = self.snake[0]
        self.win.addch(head[0], head[1], 'O', curses.A_BOLD)
        for point in self.snake[1:]:
            self.win.addch(point[0], point[1], 'o')

        self.win.refresh()

    def step(self, key):
        # 0 - UP
        # 1 - RIGHT
        # 2 - DOWN
        # 3 - LEFT

        # Move to chosen location
        moved = self.create_new_point(key)
        # Check if the move is valid
        self.check_collisions()
        # End game otherwise
        if self.done is True:
            self.end_game()
            return self.generate_observations()

        if self.food_eaten():
            self.score += 1
            self.generate_food()
        elif moved:
            self.remove_last_point()

        if self.gui: self.render()
        return self.generate_observations()

    def play(self):
        moves = {
            'w': 0,
            'd': 1,
            's': 2,
            'a': 3,
        }
        while True:
            try:
                key = self.win.getkey()
                move = moves.get(key)
            except curses.error as e:
                continue

            if move is not None:
                self.step(move)
            self.render()


    def create_new_point(self, key):
        new_point = [self.snake[0][0], self.snake[0][1]]
        if key == 0:
            new_point[0] -= 1
        elif key == 1:
            new_point[1] += 1
        elif key == 2:
            new_point[0] += 1
        elif key == 3:
            new_point[1] -= 1

        # Do not allow direct step back
        if new_point != self.snake[1]:
            self.snake.insert(0, new_point)
            return True

        return False

    def remove_last_point(self):
        self.snake.pop()

    def food_eaten(self):
        return self.snake[0] == self.food

    def check_collisions(self):
        done = False
        if (self.snake[0][0] == 0 or
                self.snake[0][0] == self.board["width"] + 1 or
                self.snake[0][1] == 0 or
                self.snake[0][1] == self.board["height"] + 1):
            done = True

        if self.snake[0] in self.snake[1:-1]:
            done = True

        self.done = done
        return done

    def generate_observations(self):
        return self.done, self.score, self.snake, self.food

    def render_destroy(self):
        self.win.clear()
        curses.endwin()

    def end_game(self):
        if self.gui:
            self.render_destroy()
        # raise Exception("Game over")


if __name__ == '__main__':
    game = SnakeGame(gui=True)
    game.start()
    # Play manually
    # game.play()
