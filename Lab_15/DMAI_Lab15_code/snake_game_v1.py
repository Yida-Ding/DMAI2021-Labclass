from random import randint
import matplotlib.pyplot as plt
import time

class SnakeGame:
    def __init__(self, board_width = 20, board_height = 20, gui = False):
        self.score = 0
        self.done = False
        self.board = {'width': board_width, 'height': board_height}
        self.gui = gui

    def start(self):
        self.snake_init()
        self.generate_food()
        if self.gui:
            self.render_init()
        return self.generate_observations()

    def snake_init(self):
        x = randint(5, self.board["width"] - 5)
        y = randint(5, self.board["height"] - 5)
        self.snake = []
        vertical = randint(0,1) == 0
        for i in range(5):
            point = [x + i, y] if vertical else [x, y + i]
            self.snake.insert(0, point)

    def generate_food(self):
        food = []
        while food == []:
            food = [randint(1, self.board["width"]), randint(1, self.board["height"])]
            if food in self.snake: food = []
        self.food = food

    def render_init(self):
#        plt.figure(figsize=(5,5))
        plt.xlim(0,self.board['width'])
        plt.ylim(0,self.board['height'])
        self.render()

    def render(self):
        ???
'''     Use matplotlib to plot a figure once a new action is performed.'''
        

    def step(self, action):
        # 0 - LEFT
        # 1 - UP
        # 2 - RIGHT
        # 3 - DOWN
        ????
'''     Perform a new action "action".'''
        return self.generate_observations()

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
        self.snake.insert(0, new_point)

    def remove_last_point(self):
        self.snake.pop()

    def food_eaten(self):
        return self.snake[0] == self.food

    def check_collisions(self):
        if (self.snake[0][0] == 0 or
            self.snake[0][0] == self.board["width"] + 1 or
            self.snake[0][1] == 0 or
            self.snake[0][1] == self.board["height"] + 1 or
            self.snake[0] in self.snake[1:-1]):
            self.done = True

    def generate_observations(self):
        return self.done, self.score, self.snake, self.food

    def render_destroy(self):
        plt.savefig('game.pdf')
        plt.close()

    def end_game(self):
        if self.gui: 
            self.render_destroy()
        raise Exception("Game over")

if __name__ == "__main__":
    game = SnakeGame(gui = True)
    game.start()
    for _ in range(20):
        time.sleep(1)
        game.step(randint(0,3))