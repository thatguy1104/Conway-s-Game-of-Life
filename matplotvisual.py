import numpy as np
import matplotlib.pyplot as plt
import pygame
import time
import sys
import random
import time

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
dimensions = 40

matrix = [[0 for i in range(dimensions)]for j in range(dimensions)]

class Matplot:
    def __init__(self):
        self.SCREENHEIGHT = 800
        self.SCREENWIDTH = 800
        self.gameDisplay = pygame.display.set_mode((self.SCREENWIDTH, self.SCREENHEIGHT))
        self.square_lenght = self.SCREENWIDTH / dimensions
        self.window_setup()
        self.drawLines()
        self.setup()
        self.main_loop()

    def window_setup(self):
        pygame.init()
        pygame.display.set_caption('Welcome to the Game of Life')
        self.gameDisplay.fill(BLACK)
        pygame.display.update()

    def drawLines(self):
        self.gameDisplay.fill(BLACK)
        positionY = 0
        THICKNESS = 1

        for i in range(dimensions):
            positionX = 0
            for k in range(dimensions):
                pygame.draw.rect(self.gameDisplay, WHITE, (positionX, positionY,
                                                           self.SCREENWIDTH / dimensions, self.SCREENWIDTH / dimensions), THICKNESS)
                positionX = positionX + self.SCREENWIDTH / dimensions
            positionY = positionY + self.SCREENHEIGHT / dimensions
        pygame.display.update()

    def colour_matrix(self, i, j, colour):
        start_x = i * self.square_lenght
        end_x = start_x + self.square_lenght

        start_y = j * self.square_lenght
        end_y = start_y + self.square_lenght

        if colour == 'W':
            pygame.draw.rect(self.gameDisplay, WHITE, (start_x,
                                                       start_y, self.square_lenght, self.square_lenght), 0)
        elif colour == 'B':
            pygame.draw.rect(self.gameDisplay, BLACK, (start_x,
                                                       start_y, self.square_lenght, self.square_lenght), 0)

    def update_matrix_visual(self):
        for i in range(dimensions):
            for j in range(dimensions):
                if matrix[i][j] == 1:
                    self.colour_matrix(i, j, 'W')
                else:
                    self.colour_matrix(i, j, 'B')
        pygame.display.update()

    def setup(self):
        for i in range(dimensions):
            for j in range(dimensions):
                matrix[i][j] = random.randint(0, 1)

    # Credits to the function below: https://trinket.io/pygame/447e96f4d4
    def count_neighbours(self, i, j):
        s = 0  # The total number of live neighbours.
        # Loop over all the neighbours.
        for x in [i - 1, i, i + 1]:
            for y in [j - 1, j, j + 1]:
                if (x == i and y == j):
                    continue  # Skip the current point itself - we only want to count the neighbours!
                if (x != dimensions and y != dimensions):
                    s += matrix[x][y]
                # The remaining branches handle the case where the neighbour is off the end of the grid.
                # In this case, we loop back round such that the grid becomes a "toroidal array".
                elif (x == dimensions and y != dimensions):
                    s += matrix[0][y]
                elif (x != dimensions and y == dimensions):
                    s += matrix[x][0]
                else:
                    s += matrix[0][0]
        return s

    def main_logic(self):
        global matrix
        next_matrix = [[0 for i in range(dimensions)] for j in range(dimensions)]

        # Compute next_matrix based on matrix
        for i in range(dimensions):
            for j in range(dimensions):
                state = matrix[i][j]
                neighbours = self.count_neighbours(i, j)

                if state == 0 and neighbours == 3:
                    next_matrix[i][j] = 1
                elif state == 1 and (neighbours < 2 or neighbours > 3):
                    next_matrix[i][j] = 0
                else:
                    next_matrix[i][j] = state
        matrix = next_matrix

    def main_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.update_matrix_visual()
            self.main_logic()
