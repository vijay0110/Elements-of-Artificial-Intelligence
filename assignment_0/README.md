# Assigniment 0
## Escape the Mystical Castle 🏰🚪

Welcome to our BFS Path Finding Algorithm repository! This project contains a Breadth-First Search (BFS) implementation for finding a path in a grid with obstacles. Below you'll find detailed documentation about our approach, challenges, and solutions.


## 📄 Problem Statement

You are trapped in a mystical castle, represented as an NxM grid map, and you need to find the shortest path from your current location (`p`) to the magic portal (`@`). The map is composed of:
- `p` (Start Point)
- `@` (Goal Point)
- `.` (Movable Path)
- `X` (Walls)

You can move one square at a time in any of the four principal compass directions (Left, Right, Down, Up). The program should output:
1. The shortest distance between `p` and `@`.
2. A sequence of moves (`L`, `R`, `D`, `U`) representing the path.

If no path exists, the program should output a distance of `-1` and not display a path.

## 💡 A bit about BFS (Breadth First Search)
Breadth-First Search (BFS) is an algorithm that explores a graph level by level, starting from a source node and visiting all nodes at the current depth before moving on to the next. It guarantees the shortest path in unweighted graphs because it reaches each node via the minimum number of edges, expanding nodes in order of their distance from the start.

![Description of Image](https://www.simplilearn.com/ice9/free_resources_article_thumb/BFS-Algorithm-Soni/bredth-first-search-in-graph-data-structure.png "Alt text for image")

*Image source: [Simplilearn](https://www.simplilearn.com/tutorials/data-structure-tutorial/bfs-algorithm)*


## 🧩 Approach

**Note:** The boilerplate code for this solution was provided to us and our task was to rectify issues/bugs within the code and make it work.

1. **Grid Representation**: The grid is read from a file with dimensions N (rows) and M (columns), and cells are marked as `p`, `@`, `.`, or `X`.

2. **BFS Algorithm**: Breadth-First Search (BFS) algorithm is used to explore the grid level by level to find the shortest path from `p` to `@`. BFS is well-suited for this task as it efficiently finds the shortest path in unweighted grids.

3. **Movement and Path Tracking**:
   - **Initialization**: Start from `p`, mark it as visited, and use a queue to explore neighboring cells.
   - **Path Reconstruction**: Track the path by concatenation to reconstruct the sequence of moves once the goal is reached.

4. **File Handling**: The program takes a command-line argument specifying the filename containing the grid map.

## 💡 Notes
- To ensure global uniformity of the solution in an instance where there are multiple possible shortest path we follow the sequence of possible moves defined in the `moves()` function provided to us which adds path in `D`, `U`, `L` & `R` order.

## 🚧 Problems Encountered

- **Infinite Loop**: The boilerplate code was running in infinite loop. This was because there was no code to keep track of the visited nodes.
- **No Path String**: There was no code to keep track of the direction (U, D, L, R) that we took at each step of the solution.
- **No Queue Implementation**: In it's given state the code used an array to append and pop elements which meant it worked as a stack instead of queue which is necessary for BFS.

## 🛠️ What We Did

- **Infinite Loop Solution:** 
    - To solve the problem of keeping track of visited nodes we used an array of same dimension as the map and initialized all the locations with 0.
        ```
        visited_nodes = [[0 for _ in range(len(castle_map[0]))] for _ in range(len(castle_map))]
        ```
    - Before expanding a node we checked whether its visited or not by checking its row,col value in our visited nodes array, if it was 1 then the node was already visited; therefore we skip it.
        ```
        if visited_nodes[curr_move[0]][curr_move[1]] != 1:
            #rest of the code
        ```
    - Thus we solved the infinite loop issue 🙌.
- **No Path String Solution:**
    - We modified the fringe tuple to also include a string for each node which would be it's path from the starting location.
        ```
        fringe=[(current_loc,0, "")]
        ```
    - We also wrote a function that when given two consecutive locations returns the direction string (U, D, L, R).
        ```
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
        ```
    - At every iteration when were inserting a node into the queue we concatenated the direction of movement of the current node and the path till previous node to get the full path up till that point.
        ```
        fringe.append((move, curr_dist + 1, curr_path + generate_path_direction(curr_move, move)))
        ```
- **No Queue Implementation:**
    - For this we just used the `pop(0)` method to pop the first element int the list therfore following the FIFO constraints of a queue.
        ```
        fringe=[(current_loc,0, "")]

        # popping the first element
        (curr_move, curr_dist, curr_path)=fringe.pop(0)
        ```

- **Additional Things**:
    - We added a simple if check in the main function to check if a solution is present otherwise print "-1"

## 🏁 Conclusion:
 We were able to reach the `magical portal` in the shortest path usign the BFS algorithm by following the same priority order of directions.

