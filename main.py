from board import Board
import pygame
from utils import WIDTH, HEIGHT, WHITE

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
        pygame.display.set_caption(f'Chess - {"white" if board.turn == WHITE else "black"} moves')

        if board.game_ended:
            run = False
            print(f'\n{"White" if board.turn == WHITE else "Black"} won!')

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

        pygame.display.update()


if __name__ == '__main__':
    main()
