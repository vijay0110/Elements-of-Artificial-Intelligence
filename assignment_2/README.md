visunku-atmalji-singsidd-a2

# Part 1: Road Trip! #


## Cost Function Implementations

This project includes five distinct cost functions, each designed to optimize for a specific route-finding objective: segment count, distance, time, accident likelihood, and coverage of U.S. states. Below are the details for each cost function.

### a) Segments: **`cost_segments_heuristic`**

   - **Objective**: **Minimize the number of road segments.**
   
   - **Approach**: Calculates the total segments traveled from the starting point plus an estimated minimum number of segments required to reach the destination.
   
   - **Formula**: `fringe_hops + 1 + int(haversine_distance / 120)`
   
   - **Details**: Here, `120` represents the 99th percentile of segment distances (around 118 miles), providing a realistic heuristic for estimating segment count.

---

### b) Distance: **`cost_distance_heuristic`**

   - **Objective**: **Minimize total distance traveled.**
   
   - **Approach**: Adds the total distance covered from the starting point plus the straight-line (Haversine) distance to the destination.
   
   - **Formula**: `haversine_distance + fringe_distance + current_distance`
   
   - **Details**: This function optimizes for the shortest possible route by combining actual distance and heuristic distance to the destination.

---

### c) Time: **`cost_time_heuristic`**

   - **Objective**: **Minimize total travel time.**
   
   - **Approach**: Adds the time taken from the start to the current location and estimates time to the destination using maximum speed limits.
   
   - **Formula**: `fringe_time + current_distance / (speed_limit + 5) + haversine_distance / (max_speed + 5)`
   
   - **Details**: Assumes a buffer of 5 mph over the speed limit for practical travel time estimation.

---

### d) Delivery: **`cost_delivery_heuristic`**

   - **Objective**: **Minimize expected accident probability, prioritizing safer routes.**
   
   - **Approach**: Calculates cumulative accident probability from the start and estimates minimum accident probability to the destination.
   
   - **Formula**: `fringe_delivery + 0.000001 * speed_limit * current_distance + 0.000001 * min_speed * haversine_distance`
   
   - **Details**: Accident probability is modeled as increasing with both speed and distance, with a constant scaling factor of `0.000001`.

---

### e) Tour: **`state_tour_heuristic`**

   - **Objective**: **Visit as many unvisited U.S. states as possible along the route.**
   
   - **Approach**: Adds a base penalty for each unvisited state, plus the total travel distance and the Haversine distance from the current location to the destination and to each unvisited state.
   
   - **Formula**:
     ```python
     unvisited_states = get_unvisited_states(us_states_gps, states_travelled)
     cost_ = len(unvisited_states) * 1000
     cost_ += current_distance + haversine_distance
     for state in unvisited_states:
         state_coords = us_states_gps[state]
         cost_ += haversine(city_lat_long, (state_coords[0], state_coords[1]))
     return cost_
     ```
   
   - **Details**: Each unvisited state incurs a penalty of `1000`, incentivizing the route to cover all contiguous states. This function prioritizes progress toward unvisited regions by adding the straight-line distance to each unvisited state.

---


### **Code functionality:** ###
This code implements an A* search algorithm to find the optimal route between a start and end city based on specified cost functions (e.g., segments, distance, time). Each city (or "state") in the path is expanded from the fringe, a priority queue managed with heapq, where cities with the lowest estimated cost are prioritized. For each city, the algorithm calculates the cumulative cost (e.g., total distance, time) plus a heuristic estimate to the destination. If a city offers a lower cost path than previously found, it is added back into the fringe with updated information. The algorithm continues until the destination is reached or all possible paths are explored.

### **Challenges Faced ** ###

1. **Segments Calculation and Outliers**: For the `segments` cost function, we faced the challenge of avoiding outliers, such as segments up to 900 miles long, which significantly skewed the segment calculations. To address this, we set a realistic threshold for segment length based on the 99th percentile (118 miles) to prevent the algorithm from over-prioritizing long segments.

2. **Distance Calculation**: To calculate the straight-line distance between cities accurately, we implemented the Haversine function, which provides an approximate great-circle distance in miles based on GPS coordinates. This helped ensure that our heuristics had a realistic measure of remaining distance.

3. **Priority Queue with `heapq`**: We chose a min-heap (`heapq`) over using a list with sorting for managing the fringe. With `heapq`, both push and pop operations are `O(log(n))`, while lists require `O(nlog(n))` for sorting and `O(n)` for pop operations. This improved the algorithm’s time complexity and efficiency.

4. **Challenges with BFS and Uniform Cost Search**: Initially, we implemented BFS for the `segments` cost function and Uniform Cost Search (UCS) for the `distance` and `time` functions without heuristics. However, these approaches took significant time to explore and expand all paths exhaustively. By incorporating heuristics into these cost functions, we guided the search more effectively and reduced computation time, allowing the algorithm to find optimal paths more efficiently.

Here is an map showing the places explored to reach newyork from salt lake city with distance cost **without heuristics**:
<img width="983" alt="Screenshot 2024-11-06 at 10 24 10 AM" src="https://github.iu.edu/cs-b551-fall2024/cs-b551-fall2024-visunku-atmalji-singsidd-a2-Private/assets/27296/04040adf-cfa0-4004-95be-9c8e636941ef">

Here is an map showing the places explored to reach newyork from salt lake city with distance cost **using heuristics**:
<img width="987" alt="Screenshot 2024-11-06 at 10 24 31 AM" src="https://github.iu.edu/cs-b551-fall2024/cs-b551-fall2024-visunku-atmalji-singsidd-a2-Private/assets/27296/54fc80e5-35cb-4ea9-b035-c4c00a48865d">

# Problem 2 Solver using UCS (Uniform Cost Search)

## **Introduction**

The problem of assigning students to teams involves several constraints: team sizes, preferred teammates, and exclusions of specific individuals. The goal is to minimize the total cost of assignments based on these constraints. This solution uses the **Uniform Cost Search (UCS)** algorithm to progressively build teams from scratch, aiming to minimize the total cost at each step.

## **High-Level Approach**

### 1. **Initial Setup**

- The algorithm begins with no students assigned to any teams.
- The function `parse_input()` reads the input file containing student preferences and exclusion lists, which include:
  - Preferred teammates for each student.
  - Excluded teammates (students that the current student does not want to be grouped with).
  - Preferred team size for each student.
  
  This data is stored in a dictionary called `student_preferences`, where each key is a student's name, and the value is a list of preferences, desired team size, and exclusions.

### 2. **State Representation**

- A state is represented as a list of teams, where each team is a list of students assigned to that team.
- Initially, the state is empty, meaning no teams have been formed.
- At each step, the state is updated by adding students to existing or new teams. The goal is to form valid teams while minimizing the total cost.

### 3. **Goal Condition**

- The algorithm keeps expanding the state by adding students to teams until all students have been assigned to teams.
- This is checked using the `is_goal()` function, which ensures that all students are assigned to at least one team.
- Once the goal state is reached, the algorithm yields the result, i.e., the list of teams and the total cost.

### 4. **Successor Generation**

- Successors represent all possible new states that can be formed by adding one or more unassigned students to teams.
- The successor generation is managed by the `add_new_group()` and `find_possible_team_members()` functions:
  - `add_new_group(state)` creates a new team by adding unassigned students to the current list of teams.
  - `find_possible_team_members(state)` creates valid two-person and three-person teams and returns a list of possible new teams that can be formed, adhering to the constraints.

### 5. **Cost Calculation**

- The `cost_function(teams)` calculates the total cost of a given team arrangement, based on:
  - **Grading cost** (`k`): A fixed cost per team.
  - **Incorrect team size**: If a team's size does not match the student's preferred team size, a penalty is applied.
  - **Preferred teammates**: If a student does not have their preferred teammates, a penalty is applied.
  - **Excluded teammates**: If a student is grouped with an excluded teammate, a penalty is applied.

### 6. **Priority Queue and UCS**

- The algorithm uses a **priority queue** to explore states with the lowest cost first. 
- The queue stores tuples of `(cost, state)`, where:
  - `cost` is the total cost of the current team assignment.
  - `state` is the list of teams.
- The algorithm starts with the initial state (no teams) and iteratively adds successors to the queue. The least costly state is processed first, ensuring that the search explores the most promising solutions first.

### 7. **Interruptibility**

- The algorithm is designed to be interruptible. It yields an intermediate result whenever it finds a valid team assignment. 
- This allows the program to provide feedback about the current solution even before reaching the final optimal assignment.

### 8. **Final Output**

- Once the algorithm reaches the goal state, it outputs the assigned groups (teams) and the total cost:
  - The assigned groups are presented as a list of teams, each consisting of student usernames separated by hyphens.
  - The total cost is the sum of the grading cost, penalties for incorrect team sizes, missing preferred teammates, and including excluded teammates.

## **Conclusion**

This approach ensures an optimal solution by incrementally exploring valid team configurations, considering all constraints, and minimizing the total cost at each step.


