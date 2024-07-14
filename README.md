# Path-Finding

## Project Overview
Path Planning is a fundamental problem in robotics, aiming to find an optimal, obstacle-free path for a robot from a starting position to a given destination. One of the most common and widely used approaches to solve this problem is the A* (A Star) search algorithm.

The goal of this project is to design and implement the A* search technique for solving the path planning problem. The environment of the robot is represented by a grid map where the initial (S) and goal (G) states are clearly localized on the map. Some cells in the map contain obstacles that the robot cannot traverse.

## Implementation Details
### A* Search Algorithm
The A* search algorithm is an informed search algorithm that aims to find the shortest path from the initial state (S) to the goal state (G). It uses a heuristic to estimate the cost to reach the goal from each node, which helps in efficiently finding the optimal path.

#### Heuristic Function
The heuristic function used in this implementation is the Euclidean distance between the current cell and the goal cell, calculated as:
\[ h(n) = \sqrt{(x_{current} - x_{goal})^2 + (y_{current} - y_{goal})^2} \]

### Movement Costs
- Horizontal or Vertical Move: Cost = 1
- Diagonal Move: Cost = √2

## Visualization
A visual simulator is provided to visualize the A* search process. The grid map, obstacles, and the path found by the algorithm will be displayed in a graphical interface.

##
![Screenshot 2024-07-14 140658](https://github.com/user-attachments/assets/369b3786-8bc2-483a-8d4a-b12147d715e8)
![Screenshot 2024-07-14 140712](https://github.com/user-attachments/assets/5df0d0d4-b4dd-4aab-a959-e640b9a1389d)

