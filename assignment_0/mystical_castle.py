#!/usr/local/bin/python3
#
# mystical_castle.py : a maze solver
#
# Submitted by : Vijay (visunku), Atharva (atmalji), Singsidd (singsidd)
#
# Based on skeleton code provided in CSCI B551, Fall 2024.

import sys
from collections import deque

# Parse the map from a given filename
def parse_map(filename):
        with open(filename, "r") as f:
                return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]
                
# Check if a row,col index pair is on the map
def valid_index(pos, n, m):
        return 0 <= pos[0] < n  and 0 <= pos[1] < m

# Find the possible moves from position (row, col)
def moves(map, row, col):
        moves=((row+1,col), (row-1,col), (row,col-1), (row,col+1))

        # Return only moves that are within the castle_map and legal (i.e. go through open space ".")
        return [ move for move in moves if valid_index(move, len(map), len(map[0])) and (map[move[0]][move[1]] in ".@" ) ]

# this function generates the path direction based on the current
# and previous positions.
def generate_path_direction(previous_move, current_move):
        x, y = current_move[0] - previous_move[0], current_move[1] - previous_move[1]

        if x == -1 and y == 0:
                return "U"
        if x == 1 and y == 0:
                return "D"
        if x == 0 and y == -1:
                return "L"
        if x == 0 and y == 1:
                return "R"



# Perform search on the map

# This function MUST take a single parameter as input -- the castle map --
# and return a tuple of the form (move_count, move_string), where:
# - move_count is the number of moves required to navigate from start to finish, or -1
#    if no such route exists
# - move_string is a string indicating the path, consisting of U, L, R, and D characters
#    (for up, left, right, and down)

def search(castle_map):
        # Here we traverse the entire map in a linear fashion and identify
        # the current location (row, col) for the starting point "p"
        current_loc=[(row_i,col_i) for col_i in range(len(castle_map[0])) for row_i in range(len(castle_map)) if castle_map[row_i][col_i]=="p"][0]
        fringe=[(current_loc,0, "")]

        # visited_nodes = [[0]* len(castle_map[0])] * len(castle_map)

        # Here we are generating a grid of same dimensions as the
        # map and initializing all the values with 0. later
        # whenever we visit a node we check if the value of the location
        # of that node in the visited nodes array is 1 if so we don't
        # expand it
        visited_nodes = [[0 for _ in range(len(castle_map[0]))] for _ in range(len(castle_map))]

        # print(visited_nodes)

        while fringe:
                (curr_move, curr_dist, curr_path)=fringe.pop(0)
                # print(fringe)

                # print("VALUE IN VISITED ARRAY FOR: " + " " + str(curr_move)+ " " + str(visited_nodes[curr_move[0]][curr_move[1]]))
                
                # Here we check if the node we are about to expand is visited
                # or not. If it is already visited then we will not expand the node
                if visited_nodes[curr_move[0]][curr_move[1]] != 1:
                        # print("NOT EXPLORED:" + str(curr_move))
                        # print(visited_nodes[curr_move[0]])
                        visited_nodes[curr_move[0]][curr_move[1]] = 1
                        
                        # print(visited_nodes[curr_move[0]])
                        # print(visited_nodes)
                        for move in moves(castle_map, *curr_move):
                                        # print("CURRENT MOVE:" + str(move))
                                        if castle_map[move[0]][move[1]]=="@":
                                                # print("GOAL IS NOT AT: " + str(move))
                                                return (curr_dist+1, curr_path + generate_path_direction(curr_move, move))  # return a dummy answer
                                        else:
                                                fringe.append((move, curr_dist + 1, curr_path + generate_path_direction(curr_move, move)))
                                                # print(fringe)

# Main Function
if __name__ == "__main__":
        castle_map=parse_map(sys.argv[1])
        print("Shhhh... quiet while I navigate!")
        solution = search(castle_map)
        if solution:
                print("Here's the solution I found:")
                print(str(solution[0]) + " " + solution[1])
        else:
                print("-1")
