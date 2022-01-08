import operator


class BasePiece:
    def __init__(self, color, move_set, position, board):
        self.color = color
        self.img_path = f"{color}-{self.__class__.__name__.lower()}"
        self.move_set = move_set
        self.position = position
        self.board = board

    def is_on_board(self, new_position):
        x, y = new_position
        if not 0 <= x < 8 or not 0 <= y < 8:
            return False

        return True

    def basic_validate(self, new_position, x, y):
        if not self.is_on_board(new_position):
            return False

        if (x, y) not in self.move_set:
            return False

        return True


class Pawn(BasePiece):
    def __init__(self, color, position, board):
        if self.color == "white":
            move_set = [(0, 1), (1, 1), (-1, 1)]
        else:
            move_set = [(0, -1), (-1, -1), (1, -1)]
        super().__init__(color, move_set, position, board)

    # TODO: first move of two squares
    def validate_move(self, new_position):
        (x, y) = (new_position[0] - self.position[0], new_position[1] - self.position[1])
        if not self.basic_validate(new_position, x, y):
            return False

        if (x, y) != self.move_set[0]:
            if self.board[new_position[0]][new_position[1]].color == self.color:
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

        if x == 0:
            for i in range(min(self.position[1], new_position[1]), max(self.position[1], new_position[1])):
                if self.board[0][i] is not None:
                    return False
            if self.board[0][new_position[1]].color == self.color:
                return False

        if y == 0:
            for i in range(min(self.position[0], new_position[0]), max(self.position[1], new_position[1])):
                if self.board[i][0] is not None:
                    return False
            if self.board[new_position[0]][0].color == self.color:
                return False

        return True


class Bishop(BasePiece):
    move_set = []
    for i in range(1, 8):
        move_set.extend([(i, i), (-i, i)])

    def __init__(self, color, position, board):
        super().__init__(color, self.move_set, position, board)

    def validate_move(self, new_position):
        (x, y) = (new_position[0] - self.position[0], new_position[1] - self.position[1])
        if not self.basic_validate(new_position, x, y):
            return False

        for i in range(min(self.position[0], new_position[0]), max(self.position[1], new_position[1])):
            if self.board[i][i] is not None:
                return False

        if self.board(new_position[0], new_position[1]) is not None:
            return False

        return True


class Knight(BasePiece):
    move_set = [(-1, 2), (1, 2), (-2, 1), (2, 1), (-2, -1), (2, -1), (-1, -2), (1, -2)]

    def __init__(self, color, position, board):
        super().__init__(color, self.move_set, position, board)

    def validate_move(self, new_position):
        (x, y) = (new_position[0] - self.position[0], new_position[1] - self.position[1])
        if not self.basic_validate(new_position, x, y):
            return False



