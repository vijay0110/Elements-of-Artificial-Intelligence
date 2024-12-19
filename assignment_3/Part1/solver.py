#!/usr/local/bin/python3
# solver.py : solve the game
#
# Code by: name IU ID
#
# Based on skeleton code for CSCI-B551
#

import sys
import time
import random
from typing import Union


def parse_board_string_to_grid(board: str, n: int) -> list[list[str]]:
    return [[k for k in board[i:i + n]] for i in range(0, len(board), n)]

def parse_board_grid_to_string(board: list[list[str]]) -> str:
    return "".join("".join(row) for row in board)

def return_empty_positions(board: list[list[str]]) -> list[tuple[int, int]]:
    return [(i, j) for i in range(len(board)) for j in range(len(board[i])) if board[i][j] == '.']

def print_board(board: Union[list[list[str]], str], n: int, m: int):
    """Prints the board in a human readable format.

    Args:
        board (Union[list[list[str]], str]): The board to be printed. 
        n (int): number of rows in the board. 
        m (int): number of columns in the board. 
    """
    if isinstance(board, str):
        assert len(board) == n * m, "Board size does not match n x m"
        board = parse_board_string_to_grid(board, m)
    
    for row in board:
        print("".join(row))

def copy_and_modify(board, pos):
    # Create a new board that is a copy of the current board.
    new_board = [row[:] for row in board]
    # Modify the board at the specified position.
    new_board[pos[0]][pos[1]] = 'x'
    return new_board

def generate_valid_boards(board, n, m, length):
    list_new_boards = []
    # Iterate over all empty positions and create a new board for each.
    for pos in return_empty_positions(board):
        # Copy and modify the board for each position.
        new_board = copy_and_modify(board, pos)
        list_new_boards.append(new_board)
    return list_new_boards


def check_game_completion(board,n,m,length,move_num):
    max_len = 0
    cnt = 0
    for i in range(n):
        len_curr = 0
        for j in range(m):
            if board[i][j] == 'x':
                len_curr = len_curr + 1
                cnt = cnt + 1
            else:
                len_curr = 0
            if len_curr > max_len:
                max_len = len_curr
    for j in range(m):
        len_curr = 0
        for i in range(n):
            if board[i][j] == 'x':
                len_curr = len_curr + 1
            else:
                len_curr = 0
            if len_curr > max_len:
                max_len = len_curr

    for i in range(n):
        len_curr = 0
        j = 0
        while i < n and i >= 0 and j >= 0 and j < m:
            if board[i][j] == 'x':
                len_curr = len_curr + 1
            else:
                len_curr = 0
            if len_curr > max_len:
                max_len = len_curr
            i = i + 1 
            j = j + 1

        len_curr = 0
        j = 0
        while i < n and i >= 0 and j >= 0 and j < m:
            if board[i][j] == 'x':
                len_curr = len_curr + 1
            else:
                len_curr = 0
            if len_curr > max_len:
                max_len = len_curr
            i = i - 1 
            j = j + 1

    for i in range(n):
        len_curr = 0
        j = m-1
        while i < n and i >= 0 and j >= 0 and j < m:
            if board[i][j] == 'x':
                len_curr = len_curr + 1
            else:
                len_curr = 0
            if len_curr > max_len:
                max_len = len_curr
            i = i + 1 
            j = j - 1

        len_curr = 0
        j = m-1
        while i < n and i >= 0 and j >= 0 and j < m:
            if board[i][j] == 'x':
                len_curr = len_curr + 1
            else:
                len_curr = 0
            if len_curr > max_len:
                max_len = len_curr
            i = i - 1 
            j = j - 1   
       
    if max_len >= length:
        return True,max_len,cnt
    return False,max_len,cnt
    
def evaluate_board(board,n,m,length,depth):
    status,max_len,curr_cnt = check_game_completion(board,n,m,length,0)
    if depth % 2 == 0 and status:
        return -100
    elif depth % 2 == 1 and status:
        return 100
    else:
        return 0
    

def min_func(board, n, m, length, depth, alpha, beta, depthlimit):

    # Check if it reached the maximum depth or a win position
    status, max_len, curr_cnt = check_game_completion(board, n, m, length, 0)
    if depth >= depthlimit or status:
        return board, evaluate_board(board, n, m, length, depth)

    finalBoard = board
    min_value = float("inf")

    # Generate the next valid moves
    next_moves = generate_valid_boards(board, n, m, length)

    # Iterate over the list of already generated next moves
    for successor in next_moves:
        # Perform the max value function for the successor to determine its evaluation
        _, eval = max_func(successor, n, m, length, depth + 1, alpha, beta, depthlimit)

        # Update the minimum evaluation value if the new evaluation is better
        if eval < min_value:
            finalBoard, min_value = successor, eval

        # Update beta value
        if min_value < beta:
            beta = min_value

        # Alpha-Beta Pruning check
        if beta <= alpha:
            return finalBoard, min_value

    return finalBoard, min_value



def max_func(board, n, m, length, depth, alpha, beta, depthlimit):

    # Check if it reached the maximum depth or a win position
    status, max_len, curr_cnt = check_game_completion(board, n, m, length, 0)
    if depth >= depthlimit or status:
        return board, evaluate_board(board, n, m, length, depth)

    finalBoard = board
    max_value = float("-inf")

    # Generate the next valid moves
    next_moves = generate_valid_boards(board, n, m, length)

    # Iterate over the list of already generated next moves
    for successor in next_moves:
        # Perform the min value function for the successor to determine its evaluation
        _, eval = min_func(successor, n, m, length, depth + 1, alpha, beta, depthlimit)

        # Update the maximum evaluation value if the new evaluation is better
        if eval > max_value:
            finalBoard, max_value = successor, eval

        # Update alpha value
        if max_value > alpha:
            alpha = max_value

        # Alpha-Beta Pruning check
        if beta <= alpha:
            return finalBoard, max_value

    return finalBoard, max_value


def minimax_alphabeta(board,n,m,length,depth,alpha,beta,depthlimit):
    return max_func(board,n,m,length,depth,alpha,beta,depthlimit)


def solver(board: str, n: int, m: int, length: int = 3):
    """This function should solve the game and return the new board.

    Args:
        board (str): describes the current board state. It is a string of length n x m.
        n (int): number of rows in the board.
        m (int): number of columns in the board.
        length (int): length of the line to be formed.
    """
    # print("length = ",len(board), n, m, length)

    assert set(board) in [{'.', 'x'}, {'.'}, {'x'}], "Invalid characters in board"
    assert len(board) == n * m, "Board size does not match n x m"
    board : list[list[str]] = parse_board_string_to_grid(board, m)
    status,max_len,curr_cnt = check_game_completion(board,n,m,length,0)
    # print(status,max_len,curr_cnt,length)
    assert not status, "game is completed already"

    # Currently placing 'x' on the board in a random position.
    # This is just a placeholder, and needs to be replaced by the actual algorithm.
    # The algorithm should return a new board, which is different from the input board.
    
    #set alpha beta values for minmax tree pruning
    alpha ,beta = float("-inf"),float("inf")
    depth = 0
    depthlimit = 6

    best_next_move,_ = minimax_alphabeta(board,n,m,length,depth,alpha,beta,depthlimit)
    
    # empty_positions = return_empty_positions(board)
    # # pick a random empty position from list of empty positions
    # i, j = random.choice(empty_positions)
    # board[i][j] = 'x'

    return best_next_move

if __name__ == "__main__":
    board_string = sys.argv[1]
    n = int(sys.argv[2])
    m = int(sys.argv[3])
    length = int(sys.argv[4])
    print ("Starting from initial board:\n")
    print_board(board_string, n, m)
    print ("\nDeciding the next step...\n")
    new_board = solver(board_string, n, m, length)
    print ("Here's what we found:\n")
    print_board(new_board, n, m)
