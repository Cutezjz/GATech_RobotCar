# --------------
# USER INSTRUCTIONS
#
# Write a function called stochastic_value that
# returns two grids. The first grid, value, should
# contain the computed value of each cell as shown
# in the video. The second grid, policy, should
# contain the optimum policy for each cell.
#
# --------------
# GRADING NOTES
#
# We will be calling your stochastic_value function
# with several different grids and different values
# of success_prob, collision_cost, and cost_step.
# In order to be marked correct, your function must
# RETURN (it does not have to print) two grids,
# value and policy.
#
# When grading your value grid, we will compare the
# value of each cell with the true value according
# to this model. If your answer for each cell
# is sufficiently close to the correct answer
# (within 0.001), you will be marked as correct.

import math

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>'] # Use these when creating your policy grid.

# ---------------------------------------------
#  Modify the function stochastic_value below
# ---------------------------------------------

# def calculate_costs(value_grid, target, left, right, success_prob):
#
#     target_x = target[0]
#     target_y = target[1]
#     target_value = value_grid[target_x][target_y]
#     print type(target_value)
#     value_state = success_prob*target_value
#     cells_to_check = [left, right] # create an array of the cells I want to check, which are left and right
#
#     for square in cells_to_check:
#         if square[0] >= 0 and square[0] < len(grid) and square[1] >=0 and square[1] < len(grid[0]):
#             value_state += (1-success_prob)*value_grid[square[0]][square[1]]
#         else:
#             value_state += (1-success_prob)*100 # it is a brick wall, so value state is 100
#
#     return value_state

def solve_at_coordinate(value, grid, init, goal, cost, failure_prob):
    closed = [[0 for row in range(len(grid[0]))] for col in range(len(grid))]
    closed[init[0]][init[1]] = 1

    x = init[0]
    y = init[1]
    g = 0


    open = [[g, x, y]]

    found = False  # flag that is set when search is complete
    resign = False # flag set if we can't find expand

    left_x = 0
    left_y = 0
    right_x = 0
    right_y = 0

    while not found and not resign:
        if len(open) == 0:
            resign = True
            break
        else:
            open.sort()
            open.reverse()
            next = open.pop()
            x = next[1]
            y = next[2]
            g = next[0]

            if x == goal[0] and y == goal[1]:
                found = True
            else:
                for i in range(len(delta)):
                    x2 = x + delta[i][0]
                    y2 = y + delta[i][1]
                    if x2 >= 0 and x2 < len(grid) and y2 >=0 and y2 < len(grid[0]):
                        if closed[x2][y2] == 0 and grid[x2][y2] == 0:

                            g2 = g + cost

                            if i == 0: #for the up direction
                                left_x = x + delta[1][0]
                                left_y = y + delta[1][1]
                                right_x = x + delta[3][0]
                                right_y = y + delta[3][0]
                            elif i == 1: #for the left direction
                                left_x = x + delta[2][0]
                                left_y = y + delta[2][1]
                                right_x = x + delta[0][0]
                                right_y = y + delta[0][0]
                            elif i == 2: #for the down direction
                                left_x = x + delta[3][0]
                                left_y = y + delta[3][1]
                                right_x = x + delta[1][0]
                                right_y = y + delta[1][0]
                            elif i == 3: #for the right direction
                                left_x = x + delta[0][0]
                                left_y = y + delta[0][1]
                                right_x = x + delta[2][0]
                                right_y = y + delta[2][0]

                            my_neighbors = [[left_x,left_y], [right_x, right_y]]

                            for square in range(len(my_neighbors)):
                                if square[0] >= 0 and square[0] < len(grid) and square[1] >=0 and square[1] < len(grid[0]):
                                    #calculate the value at that spot w/1000
                                else:
                                    #calculate value like normal

                            #g2 = new cost

                            open.append([g2, x2, y2])
                            closed[x2][y2] = 1
    return next[0] # next[0] # this is the g value of the final

def stochastic_value(grid,goal,cost_step,collision_cost,success_prob):
    failure_prob = (1.0 - success_prob)/2.0 # Probability(stepping left) = prob(stepping right) = failure_prob
    value = [[1000 for row in range(len(grid[0]))] for col in range(len(grid))]
    policy = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]

    #solve for value
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 1:
                value[i][j] = 1000
            else:
                value[i][j] = solve_at_coordinate(value, grid, [i, j], goal, cost_step, failure_prob)

    policy = []
    return value, policy

# ---------------------------------------------
#  Use the code below to test your solution
# ---------------------------------------------

grid = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 1, 1, 0]]
goal = [0, len(grid[0])-1] # Goal is in top right corner
cost_step = 1
collision_cost = 100
success_prob = 0.5

value,policy = stochastic_value(grid,goal,cost_step,collision_cost,success_prob)
for row in value:
    print row
for row in policy:
    print row

# Expected outputs:
#
# [57.9029, 40.2784, 26.0665,  0.0000]
# [47.0547, 36.5722, 29.9937, 27.2698]
# [53.1715, 42.0228, 37.7755, 45.0916]
# [77.5858, 1000.00, 1000.00, 73.5458]
#
# ['>', 'v', 'v', '*']
# ['>', '>', '^', '<']
# ['>', '^', '^', '<']
# ['^', ' ', ' ', '^']
