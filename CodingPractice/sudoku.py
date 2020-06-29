import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot, draw, show
import time
from timer import Timer
import timeit





grid  = [[0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0]]

iterations = 0
counts = []





def possible(y,x,n):
    global grid
    for i in range(0,9):
        if grid[y][i] == n:
             return False
    for i in range(0,9):
        if grid[i][x] == n:
            return False
    x0 = (x//3)*3
    y0 = (y//3)*3
    for i in range(0,3):
        for j in range(0,3):
            if grid[y0+i][x0+j] == n:
                return False
    return True


def solve():
    global grid
    global iterations
    global counts
    for y in range(9):
        for x in range(9):
            if grid[y][x] ==0:
                for n in range(1,10):
                    if possible(y,x,n):
                        
                        grid[y][x] = n
                        solve()
                        grid[y][x] = 0
                #print(np.matrix(grid)) 
                return
    iterations +=1
    #print(np.matrix(grid),iterations)
    #print(iterations)
    #counts.append(iterations)
    #print(counts)
    #plt.plot(counts)
    #input("more?")
    #show(block=False)

def test():
    "-".join(map(str, range(100)))

print(timeit.timeit(solve, number = 1))

#print(iterations)
#print(np.matrix(grid))


















