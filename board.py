from pieces import *


class Board:
    def __init__(self):
        self.turn = WHITE
        self.selected = None
        self.move_attempt = None
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
        window.fill(BLACK_COLOR)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(window, WHITE_COLOR, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def move_piece(self, x, y, new_position):
        piece = self.pieces[x][y]
        if piece.validate_move(new_position):
            x, y = piece.position
            self.pieces[x][y] = None
            piece.position = new_position
            self.pieces[piece.position[0]][piece.position[1]] = piece
            self.turn = not self.turn

    @staticmethod
    def get_square_from_coords(position):
        x, y = position
        x = x // SQUARE_SIZE
        y = ROWS - 1 - y // SQUARE_SIZE

        return x, y

    def process_input(self, position):
        x, y = self.get_square_from_coords(position)

        if self.selected is None and self.pieces[x][y] is None:
            pass
        elif self.selected is None and self.pieces[x][y].color == self.turn:
            self.selected = self.pieces[x][y]
        elif self.selected is not None and self.selected == self.pieces[x][y]:
            self.selected = None
        elif self.selected is not None:
            self.move_attempt = (x, y)

    def can_move(self):
        if self.selected is not None and self.move_attempt is not None:
            x, y = self.selected.position
            self.move_piece(x, y, self.move_attempt)
            self.selected = None
            self.move_attempt = None
