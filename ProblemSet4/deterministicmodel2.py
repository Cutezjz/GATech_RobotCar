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

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>'] # Use these when creating your policy grid.

# ---------------------------------------------
#  Modify the function stochastic_value below
# ---------------------------------------------

def stochastic_value(grid,goal,cost_step,collision_cost,success_prob):
    failure_prob = (1.0 - success_prob)/2.0 # Probability(stepping left) = prob(stepping right) = failure_prob
    value = [[1000 for row in range(len(grid[0]))] for col in range(len(grid))]
    policy = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]

    #calculate value first
    change = True

    while change:
        change = False

        for x in range(len(grid)):
            for y in range(len(grid[0])):
                if goal[0] == x and goal[1] == y:
                    if value[x][y] > 0:
                        value[x][y] = 0
                        policy[x][y] = '*'

                        change = True

                elif grid[x][y] == 0:
                    for a in range(len(delta)):
                        x2 = x + delta[a][0]
                        y2 = y + delta[a][1]

                        if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]) and grid[x2][y2] == 0:

                            if a == 0: #for the up direction
                                left_x = x + delta[1][0]
                                left_y = y + delta[1][1]
                                right_x = x + delta[3][0]
                                right_y = y + delta[3][0]
                            elif a == 1: #for the left direction
                                left_x = x + delta[2][0]
                                left_y = y + delta[2][1]
                                right_x = x + delta[0][0]
                                right_y = y + delta[0][0]
                            elif a == 2: #for the down direction
                                left_x = x + delta[3][0]
                                left_y = y + delta[3][1]
                                right_x = x + delta[1][0]
                                right_y = y + delta[1][0]
                            elif a == 3: #for the right direction
                                left_x = x + delta[0][0]
                                left_y = y + delta[0][1]
                                right_x = x + delta[2][0]
                                right_y = y + delta[2][0]

                            my_neighbors = [[left_x,left_y], [right_x, right_y]]

                            v2 = value[x2][y2]*success_prob + cost_step

                            for i in range(len(my_neighbors)):
                                mysquare = my_neighbors[i]

                                #if it is a legitimate non-colliding, non-blocked square
                                if mysquare[0] >= 0 and mysquare[0] < len(grid) and mysquare[1] >=0 and mysquare[1] < len(grid[0]) and grid[mysquare[0]][mysquare[1]] == 0:
                                    v2 += failure_prob*(value[mysquare[0]][mysquare[1]])
                                else:
                                    v2 += failure_prob*collision_cost

                            if v2 < value[x][y]:
                                change = True
                                value[x][y] = v2
                                policy[x][y] = delta_name[a] #not sure where to put thi

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
