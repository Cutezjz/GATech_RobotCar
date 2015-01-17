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

sensor_right = 0.7
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
    mySum = 0
    for row in matrix:
        mySum += sum(row)
    return mySum

#####################################

pRed = 15./20
pGreen = 5./20

#TODO: Build the sense function

# p = 4x5 matrix of probabilities
# Z = Measurement color (singular; not an array)
def sense(p,Z):
    qMatrix = zeroes(len(p), len(p[0]))
    print qMatrix
    for i in range(len(p)): #len(p) is the # of rows
            q=[]
            myRow = colors[i]  #get the appropriate row of colors
            for j in range(len(myRow)):
                hitRed = (Z == myRow[j])
                if hitRed:
                    q.append(p[i][j]*pRed*sensor_right + p[i][j]*pGreen*(1-sensor_right))
                else:
                    q.append(p[i][j]*pGreen*sensor_right + p[i][j]*pRed*(1-sensor_right))
                #q.append(p[i][j] * (hit * pRed + (1-hit) * pGreen))
            qMatrix[i] = q
            print qMatrix
        #s = sum(q)
    sum_q = sumMatrix(qMatrix)
    for a in range(len(qMatrix)):
        for b in range(len(qMatrix[0])):
            qMatrix[a][b] = qMatrix[a][b] / sum_q
    return qMatrix

p = sense(p,'green')


#TODO: Build movement system which rolls the rows and columns correctly




#Your probability array must be printed
#with the following code.

show(p)