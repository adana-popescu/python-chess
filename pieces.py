"""
Classes that model the chess pieces.

Each class is derived from BasePiece, which is a basic implementation of a piece.
The characteristics of a piece include the color, the image path, the move set and the position.
Each piece's class also has a method that validates a given move according to classic chess rules.
"""

from abc import abstractmethod
import pygame
from utils import *


class BasePiece:
    """
    A basic implementation of an abstract piece class.
    """

    def __init__(self, color, move_set, position, board):
        """
        Class constructor

        :param color: the color of the piece, which can be either white or black
        :param move_set: a tuple array. Each tuple is the difference between the current coordinates and the end
         coordinates of a possible move
        :param position: a tuple containing the current position
        :param board: the board it is currently on
        """

        self.color = color
        self.img_path = f"assets/{'white' if color == WHITE else 'black'}-{self.__class__.__name__.lower()}.png"
        self.image = pygame.image.load(self.img_path)
        self.move_set = move_set
        self.position = position
        self.board = board

    @staticmethod
    def is_on_board(position):
        """
        Checks if the piece is on board.

        :param position: a tuple consisting of a given position
        :return: False if that position is out of the board's bounds, True otherwise
        """

        x, y = position

        # checks if piece is not out of bounds
        if not 0 <= x < 8 or not 0 <= y < 8:
            return False

        return True

    def basic_validate(self, new_position, x, y):
        """
        Basic validation for the attempted move

        :param new_position: the position it is trying to move to
        :param x: x coordinate of the current position
        :param y: y coordinate of the current position
        :return: False, if the attempted move is invalid, True otherwise
        """

        # checks if piece is on board
        if not self.is_on_board(new_position):
            return False

        # checks if the next move is part of the piece's possible moves
        if (x, y) not in self.move_set:
            return False

        # checks if the ending position is not empty and of the opposite color
        if self.board[new_position[0]][new_position[1]] is not None and \
                self.board[new_position[0]][new_position[1]].color == self.color:
            return False

        return True

    def validate_horizontally(self, new_position):
        """
        Validates a horizontal move attempt

        :param new_position: the position it is trying to move to
        :return: False, if the attempted move is invalid, True otherwise
        """

        # if the move is not horizontal
        if self.position[1] != new_position[1]:
            return False

        # checks if there are no other pieces placed between the starting and ending position
        for i in range(min(self.position[0], new_position[0]) + 1, max(self.position[0], new_position[0])):
            if self.board[i][self.position[1]] is not None:
                return False

        return True

    def validate_vertically(self, new_position):
        """
        Validates a vertical move attempt

        :param new_position: the position it is trying to move to
        :return: False, if the attempted move is invalid, True otherwise
        """

        # if the move is not vertical
        if self.position[0] != new_position[0]:
            return False

        # checks if there are no other pieces placed between the starting and ending position
        for i in range(min(self.position[1], new_position[1]) + 1, max(self.position[1], new_position[1])):
            if self.board[self.position[0]][i] is not None:
                return False

        return True

    def validate_diagonally(self, new_position, x, y):
        """
        Validates a diagonal  move attempt

        :param new_position: the position it is trying to move to
        :param x: x coordinate of the current position
        :param y: y coordinate of the current position
        :return: False, if the attempted move is invalid, True otherwise
        """

        # if the move is not diagonal
        if self.position[0] == new_position[0] or self.position[1] == new_position[1]:
            return False

        sign_x = x // (abs(x))
        sign_y = y // (abs(y))

        # checks if there are no other pieces placed between the starting and ending position
        for i, j in zip(range(self.position[0] + sign_x, new_position[0], sign_x),
                        range(self.position[1] + sign_y, new_position[1], sign_y)):
            if self.board[i][j] is not None:
                return False

        return True

    @abstractmethod
    def validate_move(self, new_position):
        """
        Abstract method that will be overwritten in order to validate each piece's move set according to chess rules

        :param new_position: the position it is trying to move to
        :return: False, if the attempted move is invalid, True otherwise
        """

        raise NotImplementedError

    def draw(self, window):
        """
        Method that draws the piece on the board

        :param window: the window where it will be drawn
        :return: None
        """

        x = self.position[0] * SQUARE_SIZE
        y = HEIGHT - (self.position[1] + 1) * SQUARE_SIZE
        window.blit(self.image, (x, y))


class Pawn(BasePiece):
    """
    A class that extends the BasicPiece class. It is meant to model the behaviour of a chess pawn.
    """

    # hardcoded move set that is dependant on color
    def __init__(self, color, position, board):
        """
        Class constructor
        Extends the BasicPiece constructor. It initializes the move set with a hardcoded array.

        :param color: the color of the piece, which can be either white or black
        :param position: a tuple containing the current position
        :param board: the board it is currently on
        """

        if color == WHITE:
            move_set = [(0, 1), (1, 1), (-1, 1), (0, 2)]
        else:
            move_set = [(0, -1), (-1, -1), (1, -1), (0, -2)]
        super().__init__(color, move_set, position, board)

    def validate_move(self, new_position):
        """
        Overrides the BasicPiece method. Calls the basic_validate method. Has its' own set of extra custom checks.

        :param new_position: the position it is trying to move to
        :return: False, if the attempted move is invalid, True otherwise
        """

        (x, y) = (new_position[0] - self.position[0], new_position[1] - self.position[1])
        if not self.basic_validate(new_position, x, y):
            return False

        # if the pawn tries to capture vertically
        if ((x, y) == (0, 1) or (x, y) == (0, -1)) and self.board[new_position[0]][new_position[1]] is not None:
            return False

        # checks if it's moving diagonally to capture a piece
        if x != 0 and y != 0:
            if self.board[new_position[0]][new_position[1]] is not None and \
                    self.board[new_position[0]][new_position[1]].color == self.color or \
                    self.board[new_position[0]][new_position[1]] is None:
                return False

        # checks if it's in its' starting position in order to move two squares
        if y == 2 or y == -2:
            if not self.validate_vertically(new_position):
                return False
            if self.color == WHITE and self.position[1] != 1:
                return False
            elif self.color == BLACK and self.position[1] != 6:
                return False

        return True


class Rook(BasePiece):
    """
        A class that extends the BasicPiece class. It is meant to model the behaviour of a chess rook.
    """

    def __init__(self, color, position, board):
        """
        Class constructor
        Extends the BasicPiece constructor. It initializes the move set with a generated array.

        :param color: the color of the piece, which can be either white or black
        :param position: a tuple containing the current position
        :param board: the board it is currently on
        """

        move_set = []
        for i in range(1, 8):
            move_set.extend([(i, 0), (-i, 0), (0, i), (0, -i)])
        super().__init__(color, move_set, position, board)

    def validate_move(self, new_position):
        """
        Overrides the BasicPiece method. Uses the validate_vertically and validate_horizontally methods from BasicPiece.

        :param new_position: the position it is trying to move to
        :return: False, if the attempted move is invalid, True otherwise
        """

        (x, y) = (new_position[0] - self.position[0], new_position[1] - self.position[1])
        if not self.basic_validate(new_position, x, y):
            return False

        # vertical and horizontal validation
        if not self.validate_vertically(new_position) and not self.validate_horizontally(new_position):
            return False

        return True


class Bishop(BasePiece):
    """
        A class that extends the BasicPiece class. It is meant to model the behaviour of a chess bishop.
        """

    def __init__(self, color, position, board):
        """
        Class constructor
        Extends the BasicPiece constructor. It initializes the move set with a generated array.

        :param color: the color of the piece, which can be either white or black
        :param position: a tuple containing the current position
        :param board: the board it is currently on
        """

        move_set = []
        for i in range(1, 8):
            move_set.extend([(i, i), (-i, i), (-i, -i), (i, -i)])
        super().__init__(color, move_set, position, board)

    def validate_move(self, new_position):
        """
        Overrides the BasicPiece method. Uses the validate_diagonally method from BasicPiece.

        :param new_position: the position it is trying to move to
        :return: False, if the attempted move is invalid, True otherwise
        """

        (x, y) = (new_position[0] - self.position[0], new_position[1] - self.position[1])
        if not self.basic_validate(new_position, x, y):
            return False

        # diagonal validation
        if not self.validate_diagonally(new_position, x, y):
            return False

        return True


class Knight(BasePiece):
    """
     A class that extends the BasicPiece class. It is meant to model the behaviour of a chess knight.
    """

    def __init__(self, color, position, board):
        """
        Class constructor
        Extends the BasicPiece constructor. It initializes the move set with a hardcoded array.

        :param color: the color of the piece, which can be either white or black
        :param position: a tuple containing the current position
        :param board: the board it is currently on
        """

        # hardcoded move set
        move_set = [(-1, 2), (1, 2), (-2, 1), (2, 1), (-2, -1), (2, -1), (-1, -2), (1, -2)]
        super().__init__(color, move_set, position, board)

    def validate_move(self, new_position):
        """
        Overrides the BasicPiece method. Calls the basic_validate method. Has its' own set of extra custom checks.

        :param new_position: the position it is trying to move to
        :return: False, if the attempted move is invalid, True otherwise
        """

        (x, y) = (new_position[0] - self.position[0], new_position[1] - self.position[1])
        if not self.basic_validate(new_position, x, y):
            return False

        return True


class Queen(BasePiece):
    """
    A class that extends the BasicPiece class. It is meant to model the behaviour of a chess queen.
    """

    def __init__(self, color, position, board):
        """
        Class constructor
        Extends the BasicPiece constructor. It initializes the move set with a generated array.

        :param color: the color of the piece, which can be either white or black
        :param position: a tuple containing the current position
        :param board: the board it is currently on
        """

        move_set = []
        for i in range(1, 8):
            move_set.extend([(i, 0), (-i, 0), (0, i), (0, -i), (i, i), (-i, i), (-i, -i), (i, -i)])
        super().__init__(color, move_set, position, board)

    def validate_move(self, new_position):
        """
        Overrides the BasicPiece method. Uses the validate_vertically, validate_horizontally  and validate_diagonally
        methods from BasicPiece.

        :param new_position: the position it is trying to move to
        :return: False, if the attempted move is invalid, True otherwise
        """

        (x, y) = (new_position[0] - self.position[0], new_position[1] - self.position[1])
        if not self.basic_validate(new_position, x, y):
            return False

        # horizontal, vertical and diagonal validation
        if not self.validate_horizontally(new_position) and \
                not self.validate_vertically(new_position) and \
                not self.validate_diagonally(new_position, x, y):
            return False

        return True


class King(BasePiece):
    """
    A class that extends the BasicPiece class. It is meant to model the behaviour of a chess king.
    """

    def __init__(self, color, position, board):
        """
        Class constructor
        Extends the BasicPiece constructor. It initializes the move set with a hardcoded array.

        :param color: the color of the piece, which can be either white or black
        :param position: a tuple containing the current position
        :param board: the board it is currently on
        """

        move_set = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        super().__init__(color, move_set, position, board)

    def validate_move(self, new_position):
        """
        Overrides the BasicPiece method. Calls the basic_validate method.

        :param new_position: the position it is trying to move to
        :return: False, if the attempted move is invalid, True otherwise
        """

        (x, y) = (new_position[0] - self.position[0], new_position[1] - self.position[1])
        if not self.basic_validate(new_position, x, y):
            return False

        return True
