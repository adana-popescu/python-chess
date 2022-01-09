from board import Board
import pygame
from utils import WIDTH, HEIGHT

FPS = 60
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess')


def main():
    board = Board()

    run = True
    clock = pygame.time.Clock()
    # ok=1

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                board.process_input(position)
                board.can_move()

        board.draw_board(WINDOW)

        for row in board.pieces:
            for piece in row:
                if piece is not None:
                    piece.draw(WINDOW)

        # if ok:
        #     # board.move_piece(0, 1, (0, 2))
        #     # ok=0
        pygame.display.update()


if __name__ == '__main__':
    main()
