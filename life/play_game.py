import sys
from time import sleep

import pygame as pygame

from life.gameoflife import GameOfLife

# game colors
BACKGROUND = (50, 50, 50)
BORDER = (150, 150, 150)
CELL = (200, 200, 0)

# game size
WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400
CELL_SIZE = 10

# grid origin
ORIGIN_X = int(WINDOW_WIDTH / CELL_SIZE) / 2
ORIGIN_Y = int(WINDOW_HEIGHT / CELL_SIZE) / 2

# update speed
UPDATE_DELAY = 0.3

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()


    def update(self, occupied):
        self.drawGrid(occupied)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


    def drawGrid(self, occupied):
        self.screen.fill(BACKGROUND)
        for x in range(0, WINDOW_WIDTH, CELL_SIZE):
            for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                if (int(x / CELL_SIZE) - ORIGIN_X, int(y / CELL_SIZE) - ORIGIN_Y) in occupied:
                    pygame.draw.rect(self.screen, CELL, rect, 0)
                else:
                    pygame.draw.rect(self.screen, BORDER, rect, 1)


if __name__ == '__main__':
    # init population
    POP_SIZE = 10
    initial_population = []
    for i in range(POP_SIZE):
        initial_population.append((0, i))

    # shift y origin to center population
    ORIGIN_Y = int(WINDOW_HEIGHT / CELL_SIZE) / 2 - int(POP_SIZE / 2)

    game_logic = GameOfLife(initial_population)

    terminal = False
    period = 0
    generation = 0

    game_display = Game()

    while True:
        terminal, period, generation = game_logic.next_generation()
        print(f"Generation: {generation}")
        game_display.update(game_logic.occupied)
        sleep(UPDATE_DELAY)