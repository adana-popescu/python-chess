from board import Board
from pieces import *
import pygame

FPS = 60
WINDOW = pygame.display.set_mode((480, 480))
pygame.display.set_caption('Chess')


def main():
    board = [[None] * 8 for i in range(8)]
    init_board(board)
    draw_board = Board()

    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
        draw_board.draw_board(WINDOW)

        for row in board:
            for piece in row:
                if piece is not None:
                    piece.draw(WINDOW)
        pygame.display.update()


def init_board(board):
    for i in range(8):
        board[i][1] = Pawn(WHITE, (i, 1), board)
        board[i][6] = Pawn(BLACK, (i, 6), board)

    # added rooks
    board[0][0] = Rook(WHITE, (0, 0), board)
    board[7][0] = Rook(WHITE, (7, 0), board)
    board[0][7] = Rook(BLACK, (0, 7), board)
    board[7][7] = Rook(BLACK, (7, 7), board)

    # added knights
    board[1][0] = Knight(WHITE, (1, 0), board)
    board[6][0] = Knight(WHITE, (6, 0), board)
    board[1][7] = Knight(BLACK, (1, 7), board)
    board[6][7] = Knight(BLACK, (6, 7), board)

    # added bishops
    board[2][0] = Bishop(WHITE, (2, 0), board)
    board[5][0] = Bishop(WHITE, (5, 0), board)
    board[2][7] = Bishop(BLACK, (2, 7), board)
    board[5][7] = Bishop(BLACK, (5, 7), board)

    # added queen
    board[3][0] = Queen(WHITE, (3, 0), board)
    board[3][7] = Queen(BLACK, (3, 7), board)

    # added king
    board[4][0] = King(WHITE, (4, 0), board)
    board[4][7] = King(BLACK, (4, 7), board)


if __name__ == '__main__':
    main()
