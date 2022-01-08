import operator


class BasePiece:
    def __init__(self, color, move_set, position, board):
        self.color = color
        self.img_path = f"{color}-{self.__class__.__name__.lower()}"
        self.move_set = move_set
        self.position = position
        self.board = board

    @staticmethod
    def is_on_board(self, new_position):
        x, y = new_position

        # checks if piece is not out of bounds
        if not 0 <= x < 8 or not 0 <= y < 8:
            return False

        return True

    def basic_validate(self, new_position, x, y):
        # checks if piece is on board
        if not self.is_on_board(new_position):
            return False

        # checks if the next move is part of the piece's possible moves
        if (x, y) not in self.move_set:
            return False

        return True

    def validate_horizontally(self, new_position, x, y):
        # checks if there are no other pieces placed between the starting and ending position
        for i in range(min(self.position[0], new_position[0]), max(self.position[0], new_position[0])):
            if self.board[i][0] is not None:
                return False

        # checks if the ending position is either empty or of the opposite color
        if self.board[new_position[0]][0].color == self.color:
            return False

        return True

    def validate_vertically(self, new_position, x, y):
        # checks if there are no other pieces placed between the starting and ending position
        for i in range(min(self.position[1], new_position[1]), max(self.position[1], new_position[1])):
            if self.board[0][i] is not None:
                return False

        # checks if the ending position is either empty or of the opposite color
        if self.board[0][new_position[1]].color == self.color:
            return False

        return True

    def validate_diagonally(self, new_position, x, y):
        # checks if there are no other pieces placed between the starting and ending position
        for i in range(min(self.position[0], new_position[0]), max(self.position[0], new_position[0])):
            if self.board[i][i] is not None:
                return False

        # checks if the ending position is either empty or of the opposite color
        if self.board[0][new_position[1]].color == self.color:
            return False

        return True


class Pawn(BasePiece):
    # hardcoded move set that is dependant on color
    def __init__(self, color, position, board):
        if self.color == "white":
            move_set = [(0, 1), (1, 1), (-1, 1), (0, 2)]
        else:
            move_set = [(0, -1), (-1, -1), (1, -1), (0, -2)]
        super().__init__(color, move_set, position, board)

    def validate_move(self, new_position):
        (x, y) = (new_position[0] - self.position[0], new_position[1] - self.position[1])
        if not self.basic_validate(new_position, x, y):
            return False

        # checks if it's moving diagonally to capture a piece
        if x != 0 and y != 0:
            if self.board[new_position[0]][new_position[1]] is not None and \
                    self.board[new_position[0]][new_position[1]].color == self.color:
                return False

        # checks if it's in its' starting position in order to move two squares
        if y == 2 or y == -2:
            if not self.validate_vertically(new_position, x, y):
                return False
            if self.color == 'white' and self.position[0] != 1:
                return False
            elif self.color == 'black' and self.position[0] != 6:
                return False

        return True


class Rook(BasePiece):
    move_set = []
    for i in range(1, 8):
        move_set.extend([(i, 0), (-i, 0), (0, i), (0, -i)])

    def __init__(self, color, position, board):
        super().__init__(color, self.move_set, position, board)

    def validate_move(self, new_position):
        (x, y) = (new_position[0] - self.position[0], new_position[1] - self.position[1])
        if not self.basic_validate(new_position, x, y):
            return False

        # vertical and horizontal validation
        if not self.validate_vertically(new_position, x, y) and not self.validate_horizontally(new_position, x, y):
            return False

        return True


class Bishop(BasePiece):
    move_set = []
    for i in range(1, 8):
        move_set.extend([(i, i), (-i, i), (-i, -i), (i, -i)])

    def __init__(self, color, position, board):
        super().__init__(color, self.move_set, position, board)

    def validate_move(self, new_position):
        (x, y) = (new_position[0] - self.position[0], new_position[1] - self.position[1])
        if not self.basic_validate(new_position, x, y):
            return False

        # diagonal validation
        if not self.validate_diagonally(new_position, x, y):
            return False

        return True


class Knight(BasePiece):
    # hardcoded move set
    move_set = [(-1, 2), (1, 2), (-2, 1), (2, 1), (-2, -1), (2, -1), (-1, -2), (1, -2)]

    def __init__(self, color, position, board):
        super().__init__(color, self.move_set, position, board)

    def validate_move(self, new_position):
        (x, y) = (new_position[0] - self.position[0], new_position[1] - self.position[1])
        if not self.basic_validate(new_position, x, y):
            return False


class Queen(BasePiece):
    move_set = []
    for i in range(1, 8):
        move_set.extend([(i, 0), (-i, 0), (0, i), (0, -i), (i, i), (-i, i), (-i, -i), (i, -i)])

    def __init__(self, color, position, board):
        super().__init__(color, self.move_set, position, board)

    def validate_move(self, new_position):
        (x, y) = (new_position[0] - self.position[0], new_position[1] - self.position[1])
        if not self.basic_validate(new_position, x, y):
            return False

        # horizontal, vertical and diagonal validation
        if not self.validate_horizontally(new_position, x, y) and \
                not self.validate_vertically(new_position, x, y) and \
                not self.validate_diagonally(new_position, x, y):
            return False

        return True


class King(BasePiece):
    move_set = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]

    def __init__(self, color, position, board):
        super().__init__(color, self.move_set, position, board)

    def validate_move(self, new_position):
        (x, y) = (new_position[0] - self.position[0], new_position[1] - self.position[1])
        if not self.basic_validate(new_position, x, y):
            return False

        return True
