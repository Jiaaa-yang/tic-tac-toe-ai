"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy
import numpy as np

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if board == initial_state():
        return X
    # Check if there is equal number of X and O on board. If true, since X started, next will be X turn
    elif sum(cell.count(X) for cell in board) == sum(cell.count(O) for cell in board):
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    size = len(board)
    availableMoves = set()

    for i in range(size):
        for j in range(size):
            if board[i][j] == EMPTY:
                availableMoves.add((i, j))

    return availableMoves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise IndexError

    result_board = deepcopy(board)
    if player(board) == X:
        result_board[action[0]][action[1]] = X

    else:
        result_board[action[0]][action[1]] = O

    return result_board


def row_column_win(board):

    # Check 3 consecutive in a row which is not EMPTY
    size = len(board)
    for i in range(size):
        if len(set(board[i])) == 1 and board[i][0]:
            return board[i][0]
 
    # Check 3 consecutive in a column which is not EMPTY
    flipped_board = np.transpose(board)
    for i in range(size):
        if len(set(flipped_board[i])) == 1 and flipped_board[i][0]:
            return flipped_board[i][0]


def diagonal_win(board):
    
    size = len(board)

    # Check for top left right bottom diagonal
    if len(set(board[i][i] for i in range(size))) == 1 and board[0][0]:
        return board[0][0]
    
    # CHeck for top right left bottom diagonal
    if len(set(board[i][size - 1 - i] for i in range(size))) == 1 and board[0][2]:
        return board[0][2]


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if row_column_win(board):
        return row_column_win(board)

    return diagonal_win(board)


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):

        return True

    elif sum(cell.count(EMPTY) for cell in board) == 0:

        return True

    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1

    elif winner(board) == O:
        return -1

    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # Check whether computer is playing as O or X, then minimise or maximise respectively
    if player(board) == O:
        child, util = minimise(board, -math.inf, math.inf)
    else:
        child, util = maximise(board, -math.inf, math.inf)

    moves = actions(board)
    for move in moves:
        if result(board, move) == child:
            return move
    return None


def maximise(board, a, b):

    if terminal(board):

        return None, utility(board)

    max_child, max_util = (None, -math.inf)

    # Get child state of board for all possible move of current board
    moves = actions(board)
    for move in moves:
        child_board = result(board, move)
        (child, util) = minimise(child_board, a, b)
        if util > max_util:
            (max_child, max_util) = (child_board, util)
        if max_util >= b:
            break
        if max_util > a:
            a = max_util

    return max_child, max_util


def minimise(board, a, b):

    if terminal(board):

        return None, utility(board)

    min_child, min_util = None, math.inf

    # Get child state of board for all possible move of current board
    moves = actions(board)
    for move in moves:
        child_board = result(board, move)
        (child, util) = maximise(child_board, a, b)
        if util < min_util:
            (min_child, min_util) = (child_board, util)
        if min_util <= a:
            break
        if min_util < b:
            b = min_util

    return min_child, min_util
