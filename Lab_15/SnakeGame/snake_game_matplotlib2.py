from random import randint
import matplotlib.pyplot as plt
import time
import matplotlib.animation as manimation

class SnakeGame:
    def __init__(self, board_width = 20, board_height = 20, gui = False):
        self.score = 0
        self.done = False
        self.board = {'width': board_width, 'height': board_height}
        self.gui = gui

    def start(self):
        self.snake_init()
        self.generate_food()
        return self.generate_observations()

    def snake_init(self):
        x = randint(5, self.board["width"] - 5)
        y = randint(5, self.board["height"] - 5)
        self.snake = []
        vertical = randint(0,1) == 0
        for i in range(3):
            point = [x + i, y] if vertical else [x, y + i]
            self.snake.insert(0, point)

    def generate_food(self):
        food = []
        while food == []:
            food = [randint(1, self.board["width"]), randint(1, self.board["height"])]
            if food in self.snake: food = []
        self.food = food

    def render(self):
        plt.plot(self.food[0],self.food[1],'g*',markersize=10)
        plt.title('Score : ' + str(self.score))
        for i, point in enumerate(self.snake):
            if i == 0:
               plt.plot(point[0], point[1], 'rs',markersize=10)
            else:
                plt.plot(point[0], point[1], 'yo',markersize=5)
        plt.xlim(0,self.board['width'])
        plt.ylim(0,self.board['height'])
        plt.xticks(range(0,self.board['width']+1),[str(i) for i in range(0,self.board['width']+1)])
        plt.yticks(range(0,self.board['height']+1),[str(i) for i in range(0,self.board['height']+1)])
        plt.show()

    def step(self, key):
        # 0 - UP
        # 1 - RIGHT
        # 2 - DOWN
        # 3 - LEFT
        if self.done == True: 
            return False
        else:
            self.create_new_point(key)
            if self.food_eaten():
                self.score += 1
                self.generate_food()
            else:
                self.remove_last_point()
            self.check_collisions()
            if self.gui: 
                self.render()
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
            self.snake[0] in self.snake[1:]):
            self.done = True

    def generate_observations(self):
        return self.done, self.score, self.snake, self.food


if __name__ == "__main__":
    game = SnakeGame(gui = True)
    game.start()
    for _ in range(20):
        time.sleep(0.1)
        game.step(randint(0,3))
    print("Game Over!")
