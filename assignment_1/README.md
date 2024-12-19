# visunku-a1 : Search and Python II


# Placing Turrets in the castle
 
## 📄 Problem Statement
Place  `k` turrets (defined by `p`) in the castle at the empty locations (defined by `.`) so that no two turrets can see each other. Two turrets can see each other if they are on either the same row, column, or diagonal of the map, and there are no walls (defined by `X`) between them. Person defined as `@` and act similar to a wall for all the turret interactions 
 
## 🧩 Approach
We use the DFS on the various combinations of turrets placed by adding a turret everytime until we reach the required target number of turrets `k` and print the castle layout. If we fail to find a combination with required turrets then we print `False`.

In the example showed below there are upto (number of rows * number of columns) possibilities for each new turret placement depending on the castle layout. With DFS we can achive the target in 5 steps without exploring the other combinations deeply.

![eaia1-2](https://github.iu.edu/cs-b551-fall2024/visunku-a1/assets/27296/8e5cf8cb-2c4c-4f82-9d92-315a3ef3fb53)

## code implementation of DFS:##
 We use DFS to recursively place one turret at a time in the grid. The algorithm proceeds as follows:
	•	For each empty spot, we place the turret if it doesn’t violate the constraints (`no_turret_visible(castle_map, r, c)` function to check the direct sight and `add_turret(castle_map, row, col)` to add the turrent).
	•	Once a turret is placed, we recursively call the DFS function to place the next turret (`fringe.pop()` and `successors(castle_map)` functions).
	•	The recursion continues until we have placed k turrets successfully or we run out of valid positions (`is_goal(castle_map, k)`).

## 🚧 Problems Encountered

- **Infinite Loop**: The code was running in infinite loop in the case of impossible `k` turrets number. Solved this by adding the check statement (`no_turret_visible(castle_map, r, c)` function) to append only the legal successors for placing the turrets (`successors(castle_map)` function).
- **Turret compatibility at a given location**: I am checking this by iterating through all the 8 possible directions and see if we encounter a turret `p` before I encounter a wall `X` or me `@`. 

**assumptions:** 
- Turrets can be added at any locations if they are not seeing each other.
- Number of turrets will be huge for a large castle, hence we are not maintaining a new 2D list with boolean representing the feasibility of placing a turret at that location. This is a trade-off between speed and space. hence we are calculating the feasibility using the `no_turret_visible` function and optimising for space.
- In the case of no possible solution if we are iterating we might iterate through all the possible permutations. for example `m` turrents can be placed in the same `m` possitions in `m!` ways by considering the order of placement and we explore the next part which is common for all the parts again and again m! times. by using Dynamic programming approach the time for those cases can be reduced further. But here it is a trade of between space and speed. We need more clarity on the castle size and turrets count to decide. I have chosen to optimise for space considering the castle size and turrets count might be smaller values 
  
## 🏁 Conclusion:
 Able to generate a castle layout with required number of turrets abiding to the conditions mentions.

