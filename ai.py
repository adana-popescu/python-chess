import random
from utils import WHITE, BLACK, ROWS
from pieces import *


class AI:
    def __init__(self):
        self.color = random.randint(0, 1)

    def is_turn(self, board):
        #   checks if the assigned color corresponds to the current turn
        if self.color == board.turn:
            return True

        return False

    @staticmethod
    def get_random_valid_move(piece):
        # gets and shuffles the possible moves of the piece
        possible_moves = piece.move_set.copy()
        random.shuffle(possible_moves)

        # checks the moves and returns the first valid move of the given piece
        for move in possible_moves:
            new_position = (piece.position[0] + move[0], piece.position[1] + move[1])
            if piece.validate_move(new_position):
                return new_position

        return None

    def move_random_piece(self, board):

        # randomly going through the pieces
        for row in random.sample(board.pieces, k=len(board.pieces)):
            for piece in random.sample(row, k=len(row)):

                # if a piece of the same color as the AI is found
                if piece is not None and piece.color == self.color:
                    move = self.get_random_valid_move(piece)

                    # if it has a valid move, it moves it
                    if move is not None:
                        board.move_piece(piece, move)
                        return
