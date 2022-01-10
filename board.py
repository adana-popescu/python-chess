from pieces import *


class Board:
    def __init__(self):
        self.turn = WHITE
        self.selected = None
        self.move_attempt = None
        self.game_ended = False
        self.pieces = [[None] * 8 for i in range(8)]

        for i in range(8):
            self.pieces[i][1] = Pawn(WHITE, (i, 1), self.pieces)
            self.pieces[i][6] = Pawn(BLACK, (i, 6), self.pieces)

        # added rooks
        self.pieces[0][0] = Rook(WHITE, (0, 0), self.pieces)
        self.pieces[7][0] = Rook(WHITE, (7, 0), self.pieces)
        self.pieces[0][7] = Rook(BLACK, (0, 7), self.pieces)
        self.pieces[7][7] = Rook(BLACK, (7, 7), self.pieces)

        # added knights
        self.pieces[1][0] = Knight(WHITE, (1, 0), self.pieces)
        self.pieces[6][0] = Knight(WHITE, (6, 0), self.pieces)
        self.pieces[1][7] = Knight(BLACK, (1, 7), self.pieces)
        self.pieces[6][7] = Knight(BLACK, (6, 7), self.pieces)

        # added bishops
        self.pieces[2][0] = Bishop(WHITE, (2, 0), self.pieces)
        self.pieces[5][0] = Bishop(WHITE, (5, 0), self.pieces)
        self.pieces[2][7] = Bishop(BLACK, (2, 7), self.pieces)
        self.pieces[5][7] = Bishop(BLACK, (5, 7), self.pieces)

        # added queen
        self.pieces[3][0] = Queen(WHITE, (3, 0), self.pieces)
        self.pieces[3][7] = Queen(BLACK, (3, 7), self.pieces)

        # added king
        self.pieces[4][0] = King(WHITE, (4, 0), self.pieces)
        self.pieces[4][7] = King(BLACK, (4, 7), self.pieces)

    @staticmethod
    def draw_board(window):
        # draws the checkered board
        window.fill(BLACK_COLOR)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(window, WHITE_COLOR, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def move_piece(self, piece, new_position):
        # validates the move and updates the board pieces matrix
        if piece.validate_move(new_position):
            x, y = piece.position
            self.pieces[x][y] = None
            piece.position = new_position

            # if the captured piece is a King, prepare the game for ending
            if isinstance(self.pieces[new_position[0]][new_position[1]], King):
                self.game_ended = True

            self.pieces[piece.position[0]][piece.position[1]] = piece

            if not self.game_ended:
                self.turn = not self.turn

    @staticmethod
    def get_square_from_coords(position):
        # determines which matrix row and column is clicked by getting its coordinates
        x, y = position
        x = x // SQUARE_SIZE
        y = ROWS - 1 - y // SQUARE_SIZE

        return x, y

    def process_input(self, position):
        # gets the matrix row and number
        x, y = self.get_square_from_coords(position)

        # if clicking on an empty square without having a piece selected, it does nothing
        if self.selected is None and self.pieces[x][y] is None:
            pass
        # if there is no selected piece and someone clicked on a piece on the right turn, it selects it
        elif self.selected is None and self.pieces[x][y].color == self.turn:
            self.selected = self.pieces[x][y]
        # if someone clicks on the selected piece, it deselects it
        elif self.selected is not None and self.selected == self.pieces[x][y]:
            self.selected = None
        # if someone selects a piece of the same color as the previous one, it keeps the latest selection
        elif self.selected is not None and self.pieces[x][y] is not None and self.selected.color == self.pieces[x][y].color:
            self.selected = self.pieces[x][y]
        # if there is a selected piece, update the position where it's trying to move to
        elif self.selected is not None:
            self.move_attempt = (x, y)

    def can_move(self):
        # if all the conditions are met for moving a piece, it moves it and deselects everything
        if self.selected is not None and self.move_attempt is not None:
            self.move_piece(self.selected, self.move_attempt)
            self.selected = None
            self.move_attempt = None
