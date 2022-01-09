from pieces import *


def main():
    board = [[None] * 8 for i in range(8)]
    init_board(board)


def init_board(board):
    for i in range(8):
        board[i][1] = Pawn(WHITE, (i, 1), board)
        board[i][6] = Pawn(BLACK, (i, 6), board)

    # added rooks
    board[0][0] = Rook(WHITE, (0, 0), board)
    board[0][7] = Rook(WHITE, (0, 7), board)
    board[7][0] = Rook(BLACK, (7, 0), board)
    board[7][7] = Rook(BLACK, (7, 7), board)

    # added knights
    board[0][1] = Knight(WHITE, (0, 1), board)
    board[0][6] = Knight(WHITE, (0, 6), board)
    board[7][1] = Knight(BLACK, (0, 1), board)
    board[7][6] = Knight(BLACK, (0, 6), board)

    # added bishops
    board[0][2] = Bishop(WHITE, (0, 2), board)
    board[0][5] = Bishop(WHITE, (0, 5), board)
    board[7][2] = Bishop(BLACK, (7, 2), board)
    board[7][5] = Bishop(BLACK, (7, 5), board)

    # added queen
    board[0][3] = Queen(WHITE, (0, 3), board)
    board[7][3] = Queen(BLACK, (7, 3), board)

    # added king
    board[0][4] = King(WHITE, (0, 4), board)
    board[7][4] = King(BLACK, (7, 4), board)


if __name__ == '__main__':
    main()
