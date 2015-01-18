colors = [['red', 'green', 'green',   'red', 'red'],
          ['red',   'red', 'green',   'red', 'red'],
          ['red',   'red', 'green', 'green', 'red'],
          ['red',   'red',   'red',   'red', 'red']]

measurements = ['green', 'green', 'green' ,'green', 'green']

p = [[1./20, 1./20, 1./20, 1./20, 1./20],
     [1./20, 1./20, 1./20, 1./20, 1./20],
     [1./20, 1./20, 1./20, 1./20, 1./20],
     [1./20, 1./20, 1./20, 1./20, 1./20]]

motions = [[0,0],[0,1],[1,0],[1,0],[0,1]]
#motions = [[0,0],[0,0],[0,0],[0,0],[0,0]]

sensor_right = 0.7 #same as pHit
p_move = 0.8

def show(p):
    for i in range(len(p)):
        print p[i]

#Do not delete this comment!
#Do not use any import statements.
#Adding or changing any code above may
#cause the assignment to be graded incorrectly.

#Enter your code here:

import numpy as np
import copy

#Helper Functions because for some bloody reason they won't let us use effing Numpy

def getColumn(matrix, i):
    return [row[i-1] for row in matrix]

def getRow(matrix,i):
    return matrix[i-1]

#get me something at Row X and Column Y
def getElement(matrix,row,column):
    return matrix[row-1][column-1]

#build a matrix of 0s of dimension ixj (i = rows, j = columns)
def zeroes(i,j):
    return [ [ 0 for columns in range(j) ] for rows in range(i) ]

#I want it to roll right by i
#def rollColumn(matrix,i):

#I want it to roll all the rows down by i
#def rollRow(matrix,i):

#sum all values in a matrix
def sumMatrix(matrix):
    matrix = np.array(matrix)
    return matrix.sum()

#####################################

pRed = 15./20
pGreen = 5./20
pHit = sensor_right

#numpyColors = np.array(colors) #create a numpy version of the colors

#TODO: Build the sense function

# p = 4x5 matrix of probabilities
# Z = Measurement color (singular; not an array)
def sense(p,Z):
    qMatrix = zeroes(len(p), len(p[0]))
    for i in range(len(p)): #len(p) is the # of rows
        q=[]
        myRow = colors[i]  #get the appropriate row of colors
        for j in range(len(myRow)):
            hit = (Z == myRow[j])
            q.append(p[i][j] * (hit * pHit + (1-hit) * (1-pHit)))
                # if Z == 'red':
                #     q.append(p[i][j]*pRed*sensor_right + p[i][j]*pGreen*(1-sensor_right))
                # else:
                #     q.append(p[i][j]*pGreen*sensor_right + p[i][j]*pRed*(1-sensor_right))

            qMatrix[i] = q
    sum_q = sumMatrix(qMatrix)
    qMatrix = np.array(qMatrix)
    qMatrix = qMatrix/sum_q

    print "the sum of qMatrix is %s" % qMatrix.sum()
    return qMatrix


#TODO: Build movement system which rolls the rows and columns correctly

# Z is the movement array, p is the probability matrix
def move (p,Z):
    qmatrix = np.zeros(shape=(len(p), len(p[0])))
    p = np.array(p) # convert arrays to Numpy
    #Z = np.array(Z)
    p_old = copy.deepcopy(p)

    # create formula for horizontal movement; assumes movement is never more than 1
    horizMovement = Z[1]
    if horizMovement != 0:
        p = np.roll(p,horizMovement, 1)

    # create formula for vertical movement
    vertMovement = Z[0]
    if vertMovement != 0:
        p = np.roll(p,vertMovement, 0)

    qmatrix = p_move*p + (1-p_move)*p_old #factor in the probability that we fail to move
    qmatrix = qmatrix/qmatrix.sum()

#qmatrix = qmatrix/qmatrix.sum()

    return qmatrix

#Your probability array must be printed
#with the following code.

#test cases
#p = move(p, [0,1])
#p = sense(p,'green')

for k in range(len(measurements)):
    p = move(p, motions[k])
    p = sense(p, measurements[k])


show(p)