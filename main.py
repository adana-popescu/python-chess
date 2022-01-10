import sys
from ai import AI
from board import Board
import pygame
from utils import WIDTH, HEIGHT, WHITE


def main():
    global run

    # checking the run argument, printing usage instructions if invalid
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <PVP/AI>")
        exit(1)

    player_type = sys.argv[1]
    if player_type not in ['PVP', 'AI']:
        print(f"Usage: python {sys.argv[0]} <PVP/AI>")
        exit(2)

    # setting up pygame related variables
    FPS = 60
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # instancing classes
    board = Board()
    ai = AI()

    while run:
        clock.tick(FPS)
        pygame.display.set_caption(f'Chess - {"white" if board.turn == WHITE else "black"} moves')

        # check if game end condition is met
        if board.game_ended:
            run = False
            print(f'\n{"White" if board.turn == WHITE else "Black"} won!')

        # drawing the board and pieces
        board.draw_board(WINDOW)
        for row in board.pieces:
            for piece in row:
                if piece is not None:
                    piece.draw(WINDOW)

        # checking player type
        if player_type == 'PVP':
            player_event(board)

        if player_type == 'AI':

            # checks if it's the AI's turn and moves randomly if yes
            if ai.is_turn(board):
                ai.move_random_piece(board)
            else:
                player_event(board)

        pygame.display.update()


def player_event(board):
    global run
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # gets move from player and processes it
        if event.type == pygame.MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()
            board.process_input(position)
            board.can_move()


if __name__ == '__main__':
    run = True
    main()
