"""
Tic Tac Toe Player
"""

import numpy as np
import copy

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
    num_of_x = 0
    num_of_o = 0
    for i in board:
        for j in i:
            if j == X:
                num_of_x += 1
            if j == O:
                num_of_o += 1
    if num_of_x > num_of_o:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    
    
    actions = tuple()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
               actions = actions + tuple(((i,j),))
    return actions


def result(brd, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    
    board = copy.deepcopy(brd)
    
    if not brd[action[0]][action[1]] == EMPTY:
        raise Exception('Action not allowed')
    
    board[action[0]][action[1]] = player(board)
    
    
    return board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    
    
    # Rad
    for row in board:
        if row[0] == row[1] and row[1] == row[2] and not row[2] == EMPTY:
            return row[0]
        
    # Kolonne
    for col in np.array(board).T:
        if col[0] == col[1] and col[1] == col[2] and not col[2] == EMPTY:
            return col[0]
        
    # Diagonal
    if board[0][0] == board[1][1] and board[1][1] == board[2][2] and not board[2][2] == EMPTY:
        return board[0][0]
    if board[2][0] == board[1][1] and board[1][1] == board[0][2] and not board[0][2] == EMPTY:
        return board[2][0]
    
    return None
    

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
         return True

    numpyBoard = np.array(board)
    emptyCount = np.count_nonzero(numpyBoard == EMPTY)
    if emptyCount == 0:
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
    else:
        return 0
    
    
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    P = player(board)
    if P == X:
        return Max(board)[1]
    else:
        return Min(board)[1]




def Max(board):
    if terminal(board):
        return (utility(board), None)

    best_score = -np.inf
    best_action = None
    for action in actions(board):
        Result = Min(result(board, action))
        if Result[0] > best_score:
            best_score = Result[0]
            best_action = action

    return (best_score, best_action)


def Min(board):
    if terminal(board):
        return (utility(board), None)

    best_score = np.inf
    best_action = None
    for action in actions(board):
        Result = Max(result(board, action))
        if Result[0] < best_score:
            best_score = Result[0]
            best_action = action

    return (best_score, best_action)