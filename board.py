import pygame
from utils import *


class Board:
    @staticmethod
    def draw_board(window):
        window.fill(BLACK_COLOR)
        for row in range(ROWS):
            for col in range(row%2, ROWS, 2):
                pygame.draw.rect(window, WHITE_COLOR, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

