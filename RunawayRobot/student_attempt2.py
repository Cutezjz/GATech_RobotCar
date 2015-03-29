# ----------
# Part Two
#
# Now we'll make the scenario a bit more realistic. Now Traxbot's
# sensor measurements are a bit noisy (though its motions are still
# completetly noise-free and it still moves in an almost-circle).
# You'll have to write a function that takes as input the next
# noisy (x, y) sensor measurement and outputs the best guess
# for the robot's next position.
#
# ----------
# YOUR JOB
#
# Complete the function estimate_next_pos. You will be considered
# correct if your estimate is within 0.01 stepsizes of Traxbot's next
# true position.
#
# ----------
# GRADING
#
# We will make repeated calls to your estimate_next_pos function. After
# each call, we will compare your estimated position to the robot's true
# position. As soon as you are within 0.01 stepsizes of the true position,
# you will be marked correct and we will tell you how many steps it took
# before your function successfully located the target bot.

# These import steps give you access to libraries which you may (or may
# not) want to use.
from robot import *  # Check the robot.py tab to see how this works.
from math import *
from matrix import * # Check the matrix.py tab to see how this works.

import time
import random

# This is the function you have to write. Note that measurement is a
# single (x, y) point. This function will have to be called multiple
# times before you have enough information to accurately predict the
# next position. The OTHER variable that your function returns will be
# passed back to your function the next time it is called. You can use
# this to keep track of important information over time.
# def estimate_next_pos(measurement, OTHER = None):
#     """Estimate the next (x, y) position of the wandering Traxbot
#     based on noisy (x, y) measurements."""
#
#     # You must return xy_estimate (x, y), and OTHER (even if it is None)
#     # in this order for grading purposes.
#     #xy_estimate = (3.2, 9.1)
#
#
#
#     return xy_estimate, OTHER

def estimate_next_pos(measurement, OTHER = None):

    # helper function to map all angles onto [-pi, pi]
    def angle_truncate(a):
        while a < 0.0:
            a += pi * 2
        return ((a + pi) % (pi * 2)) - pi

    print "true heading"
    print test_target.heading
    I = matrix([[1, 0, 0],
                [0, 1, 0],
                [0, 0, 1]]) #identity matrix




    R = matrix([[measurement_noise, 0], [0, measurement_noise]])

    H = matrix([[0, 1, 0],
                [0, 0, 1]]) #Jacobian of the measurement function

    u = matrix([[0],
                [0],
                [0]])

    F = []

    heading = 0 #WILD ASS GUESS

    if OTHER is not None:
        print "-----------------"
        current_measurement = measurement
        last_measurement = OTHER['last_measurement']
        heading = atan2(measurement[1] - last_measurement[1], measurement[0] - last_measurement[0])
        #heading = angle_truncate(heading)
        #heading = test_target.heading
        #heading = atan2(measurement[0] - last_measurement[0], measurement[1] - last_measurement[1])
        #heading = heading%(2*pi)
        print "calculated heading"
        print heading
        X = OTHER['X']
        P = OTHER['P']

        if 'last_heading' not in OTHER:
            OTHER['last_heading'] = heading
            xy_estimate = [X.value[1][0], X.value[2][0]]
            OTHER['last_measurement'] = measurement
        else:
            print "OTHER is:", OTHER
            turning_angle = heading - OTHER['last_heading']
            print "turning angle:", turning_angle
            print "turning angle actual:", test_target.turning
            #last_heading = OTHER['last_heading']


            #do some guessing
            D = distance_between(measurement, last_measurement)
            print "this is the D"
            print D
            theta = (heading+turning_angle)%(2*pi)
            print "theta:", theta
            print "theta - heading current:", theta - test_target.heading

            #estimation step

            #is it "last heading" or "theta"????
            # X = matrix([[theta],
            #             [X.value[1][0] + D * cos(theta)],
            #             [X.value[2][0] + D * sin(theta)]])

            delta_x = D * cos(theta)
            delta_y = D * sin(theta)

            nextX = measurement[0] + delta_x
            nextY = measurement[1] + delta_y

            # nextX = X.value[1][0] + delta_x
            # nextY = X.value[2][0] + delta_y

            #print "the distance to the next guessed point is:", distance_between([nextX,nextY], measurement)

            X = matrix([[theta],
                         [nextX],
                         [nextY]])

            print "I'm projecting X out to:", X
            print "Note, the current robot stats:", test_target.heading, test_target.x, test_target.y

            F = matrix([[1, 0, 0],
                        [-D*sin(theta), 1, 0],
                        [D*cos(theta), 0, 1]])

            P = OTHER['P']
            #X = OTHER['X']


            H = matrix([[0, 1, 0],
                        [0, 0, 1]])

            # #Prediction
            # X = (F * X) + u
            # P = F * P * F.transpose() # + Q

            P = F * P * F.transpose() # + Q

            #measurement update
            observations = matrix([[measurement[0]],
                         [measurement[1]]]) #truth
            Z = H*X
            Y = observations - Z
            print "this is Y"
            print Y
            S = H * P * H.transpose() + R
            K = P * H.transpose() * S.inverse()
            X = X + (K*Y)

            P = (I - (K * H)) * P

            X.value[0][0] = angle_truncate(X.value[0][0])


            OTHER['X'] = X

            OTHER['P'] = P
            x_estimate = OTHER['X'].value[1][0]
            y_estimate = OTHER['X'].value[2][0]
            print "Currently, the robot state is:", test_target.heading, observations
            print "This is what Kalman thinks X will be:", OTHER['X']
            xy_estimate = [x_estimate, y_estimate]

            OTHER['last_heading'] = heading
            OTHER['last_measurement'] = measurement


    else:
        #x = theta, x, y
        X = matrix([[0.5],
                    [2],
                    [4]])
        #convariance matrix
        P = matrix([[1000, 0, 0],
                    [0, 1000, 0],
                    [0, 0, 1000]])
        OTHER = {'last_measurement': measurement, 'X': X, 'P': P}
        xy_estimate = [X.value[1][0], X.value[2][0]]

    return xy_estimate, OTHER

# A helper function you may find useful.
def distance_between(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)



# This is here to give you a sense for how we will be running and grading
# your code. Note that the OTHER variable allows you to store any
# information that you want.
def demo_grading(estimate_next_pos_fcn, target_bot, OTHER = None):
    localized = False
    distance_tolerance = 0.01 * target_bot.distance
    print "the distance tolerance is:" , distance_tolerance
    ctr = 0
    # if you haven't localized the target bot, make a guess about the next
    # position, then we move the bot and compare your guess to the true
    # next position. When you are close enough, we stop checking.
    errorlist = []
    while not localized and ctr <= 1000:
        ctr += 1
        measurement = target_bot.sense()
        position_guess, OTHER = estimate_next_pos_fcn(measurement, OTHER)
        target_bot.move_in_circle()
        true_position = (target_bot.x, target_bot.y)
        error = distance_between(position_guess, true_position)
        errorlist.append(error)
        print "the DELTA between minimum error and tolerance is:", distance_tolerance - min(errorlist)
        if error <= distance_tolerance:
            print "You got it right! It took you ", ctr, " steps to localize."
            localized = True
        if ctr == 1000:
            print "Sorry, it took you too many steps to localize the target."
    return localized

def demo_grading_visual(estimate_next_pos_fcn, target_bot, OTHER = None):
    localized = False
    distance_tolerance = 0.01 * target_bot.distance
    print "the distance tolerance is:", distance_tolerance
    ctr = 0
    # if you haven't localized the target bot, make a guess about the next
    # position, then we move the bot and compare your guess to the true
    # next position. When you are close enough, we stop checking.
    #For Visualization
    import turtle    #You need to run this locally to use the turtle module
    window = turtle.Screen()
    window.bgcolor('white')
    size_multiplier= 25.0  #change Size of animation
    broken_robot = turtle.Turtle()
    broken_robot.shape('turtle')
    broken_robot.color('green')
    broken_robot.resizemode('user')
    broken_robot.shapesize(0.1, 0.1, 0.1)
    measured_broken_robot = turtle.Turtle()
    measured_broken_robot.shape('circle')
    measured_broken_robot.color('red')
    measured_broken_robot.resizemode('user')
    measured_broken_robot.shapesize(0.1, 0.1, 0.1)
    prediction = turtle.Turtle()
    prediction.shape('arrow')
    prediction.color('blue')
    prediction.resizemode('user')
    prediction.shapesize(0.1, 0.1, 0.1)
    prediction.penup()
    broken_robot.penup()
    measured_broken_robot.penup()
    #End of Visualization
    errorlist = []
    while not localized and ctr <= 100:
        ctr += 1
        measurement = target_bot.sense()
        position_guess, OTHER = estimate_next_pos_fcn(measurement, OTHER)

        target_bot.move_in_circle()
        true_position = (target_bot.x, target_bot.y)
        print "the position guess from my algorithm is:", position_guess
        error = distance_between(position_guess, true_position)
        errorlist.append(error)
        print "the error is:", error
        if error <= distance_tolerance:
            print "You got it right! It took you ", ctr, " steps to localize."
            localized = True
        if ctr == 300:
            print "Sorry, it took you too many steps to localize the target."
        #More Visualization
        measured_broken_robot.setheading(target_bot.heading*180/pi)
        measured_broken_robot.goto(measurement[0]*size_multiplier, measurement[1]*size_multiplier-200)
        measured_broken_robot.stamp()
        broken_robot.setheading(target_bot.heading*180/pi)
        broken_robot.goto(target_bot.x*size_multiplier, target_bot.y*size_multiplier-200)
        broken_robot.stamp()
        prediction.setheading(target_bot.heading*180/pi)
        prediction.goto(position_guess[0]*size_multiplier, position_guess[1]*size_multiplier-200)
        prediction.stamp()
        #End of Visualization
        #turtle.getscreen()._root.mainloop()

        #time.sleep()
        print "the minimum error is so far:", min(errorlist)

    return localized

# This is a demo for what a strategy could look like. This one isn't very good.
def naive_next_pos(measurement, OTHER = None):
    """This strategy records the first reported position of the target and
    assumes that eventually the target bot will eventually return to that
    position, so it always guesses that the first position will be the next."""
    if not OTHER: # this is the first measurement
        OTHER = measurement
    xy_estimate = OTHER
    return xy_estimate, OTHER

# This is how we create a target bot. Check the robot.py file to understand
# How the robot class behaves.
test_target = robot(2.1, 4.3, 0.5, 2*pi / 34.0, 1.5)
measurement_noise = 2 * test_target.distance
test_target.set_noise(0.0, 0.0, measurement_noise)

demo_grading_visual(estimate_next_pos, test_target)




