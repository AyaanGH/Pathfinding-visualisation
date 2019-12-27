"""

Generate maze to solve

"""


import random
import copy
import math

def setSize():
    size_x = int(input('X size\n'))
    size_y = int(input('Y size\n'))

    return size_x,size_y

def construct_table(size_x,size_y):

    table = []

    
    for i in range(size_y):
        row = []
        for k in range(size_x):
            row.append(".")
        table.append(row)
    
    return table


def print_table(table):

    for row in table:
       print(' '.join(row))


def startPoint(table,xLen,yLen):
    start_x = random.randint(0,xLen-1)
    start_y = random.randint(0,yLen-1)

    # print(start_x,start_y)

    table[start_y][start_x] = 'O'

    while True :
        end_x = random.randint(0, xLen-1)
        end_y = random.randint(0, yLen-1)

        if end_x == start_x  or end_y == start_y:
            continue

        table[end_y][end_x ] = 'X'
        
        break 
    # print(end_x,end_y)

    return table,start_x,start_y,end_x,end_y

def obstacle(table,x,y):
    obstacle_quantity = int(0.2*x*y)
    # print(obstacle_quantity,"obstacle amount")

    obstacles_generated = 0
    obstacle_y = 0
    obstacle_x = 0
   

    while True:
        obstacle_x = random.randint(0, x - 1)
        obstacle_y = random.randint(0, y - 1)
        coordinate = table[obstacle_y][obstacle_x]
        # print(obstacles_generated)
        # print(coordinate,obstacle_x,obstacle_y)

        if obstacle_quantity == obstacles_generated:
            break

        elif  coordinate == ".":
             table[obstacle_y][obstacle_x] = "#"
             obstacles_generated += 1 
    
    return table

def genCoordinates(table,start_x,start_y,end_x,end_y):

    coordinates = []

    for i in range(len(table)):
        for k in range(len(table[i])):
            weights =  math.sqrt(((end_x - i)**2 + (end_y - k)**2))
            
    
            coordinates.append([i,k,round(weights,4)])

    return coordinates

    

def dijikstra(table,coords,start_x,start_y,end_x,end_y):
    stack = copy.deepcopy(coords)
    print(stack)
    print(len(stack))
    print("=============================")

    #print(table)

    for coord_pair in stack:
        table_value = table[coord_pair[1]][coord_pair[0]]

        if table_value == "#":
            print("removing", coord_pair)
            stack.remove(coord_pair)
        # if table[coord_pair[0][coord_pair[1]]] == "#":
        #     stack.remove(coord_pair)
    
    print(stack)
    print(len(stack))



if __name__ == "__main__":
    x,y = setSize()
    empty_table = construct_table(x,y)
    # print_table(empty_table)
    start_point_table, start_x,start_y,end_x,end_y = startPoint(empty_table,x,y)

    #print_table(start_point_table)
    obstacle_table = obstacle(start_point_table,x , y)

    print_table(obstacle_table)
    coords = genCoordinates(obstacle_table,start_x,start_y,end_x,end_y)
    dijikstra(obstacle_table,coords,start_x,start_y,end_x,end_y)

    #print(coords)

    # while True:
    #     temp = input("")
    #     fresh_obstacle_table = copy.deepcopy(start_point_table)
    #     test = obstacle(fresh_obstacle_table, x, y)
    #     print_table(test)

"""
 . . . . . . . . . . . . . . . . .
 . . . . . . . . . . . # . . . . .
 . . . . . . . . . . . # - B . . .
 . . . . . . . . . . . # . . . . .
 . . . . . . . . . . . # . . . . .
 . . A - - - - - - - - # . . . . .
 . . . . . . . . . . . . # . . . .
 . . . . . . . . . . . . . . . . .



|
|
|
|
|
|



"""
