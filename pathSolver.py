"""

Generate maze to solve








"""


import random
import copy
import math
import json

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

    

def dijikstra(table,coords,start_x,start_y,end_x,end_y,node_map,size_x,size_y):
     list_of_coordinates = copy.deepcopy(coords)
     stack = []
     visited = []
     stack.append([start_x,start_y])
     visited.append([start_x,start_y])
     distance_counter = 0

     while True:

        holding = []
        
        current_visiting_node = visited[-1]

        # print('cURRENT VISINT NODE: ', current_visiting_node)

        #Check north

        x_val = current_visiting_node[0]
        y_val = current_visiting_node[1]-1

        # print("checking North:")
        # print("Current Visitng node",x_val,",",y_val," " , visited)

        try:
            if table[y_val][x_val] == "." or table[y_val][x_val] == "X":
                if y_val >=0:
                    # print('North is a valid node')
                    holding.append([x_val,y_val])

        except IndexError:
            pass
            # print("North is out of range")


         #Check South

        x_val = current_visiting_node[0]
        y_val = current_visiting_node[1] + 1

        # print("checking South:")
        # print("Current Visitng node", x_val, ",", y_val, " ", visited)

        try:
            if table[y_val][x_val] == "." or table[y_val][x_val] == "X":
                if y_val <= size_y-1:
                    # print('South is a valid node')
                    holding.append([x_val, y_val])

        except IndexError:
            pass
            # print("South is out of range")


        #Check East

        x_val = current_visiting_node[0]+1
        y_val = current_visiting_node[1] 

        # print("checking East:")
        # print("Current Visitng node", x_val, ",", y_val, " ", visited)

        try:
            if table[y_val][x_val] == "." or table[y_val][x_val] == "X":
                if x_val<= size_x-1:
                    # print('East is a valid node')
                    holding.append([x_val, y_val])

        except IndexError:
            # print("East is out of range")
            pass

        #Check WEst

        x_val = current_visiting_node[0] -1
        y_val = current_visiting_node[1] 

        # print("checking West:")
        # print("Current Visitng node", x_val, ",", y_val, " ", visited)

        try:
            if table[y_val][x_val] == "." or table[y_val][x_val] == "X":
                if x_val >= 0:
                    # print('West is a valid node')
                    # print("symbol at west is",table[y_val][x_val])
                    holding.append([x_val, y_val])

        except IndexError:
            pass
            # print("West is out of range")
        
        if holding != []:
            # print("We have found the following visitable nodes around",current_visiting_node)
            # print("Visitable nodes",holding)

            weight_map = {}

            for node in holding:
                # print(node)
                weight_map[str(node)] = node_map[str(node)]['distance_to_end']

                # print('weight map')
                print(weight_map)
                
                #Use dictonary to find ideal weight
           
            minVal = (min(weight_map, key= weight_map.get))

            if  weight_map[minVal] == 0.0:
                # print("shortest found")
                del visited[0]
                return visited


            # print("best node to visit is ", minVal)

            clean_list = json.loads(minVal)
            clean_list_x = clean_list[0]
            clean_list_y = clean_list[1]
            table[clean_list_y][clean_list_x]= '#'

            visited.append(clean_list)

            
        
        else:
            print("There are no visitable nodes ")
            print("Fixing")
            table[y_val][x_val] = "#"

            del visited[-1]
            current_visiting_node = visited[-1]

            

            #Check north

            x_val = current_visiting_node[0]
            y_val = current_visiting_node[1]
            table[y_val][x_val] = "."




        # stack.append
        # cont = input("")


'''
node_dictionary = 


{

"5,3": {value:".", distance_from_start: 5 , from: "6,3", distance_to_end = 3, shortest_found: }


}
'''

def genNodeMap(table,end_x,end_y):

    node_map = {}

    for i in range(len(table)):
        for k in range(len(table[i])):
            end_distance = math.sqrt(((end_x - k)**2 + (end_y - i)**2))
            node_map['['+ str(k)+', '+str(i)+']'] = {"value":str(table[i][k]),"distance_from_start":999, "from":"","distance_to_end": round(end_distance,3),"shortest_found":False}
    
    #print(node_map)
    
    return node_map




def path_table(visits,obstacle_table):
    print(visits)

    for node in visits:

        obstacle_table[node[1]][node[0]] = "@"
        
    return obstacle_table





if __name__ == "__main__":
    x,y = setSize()
    empty_table = construct_table(x,y)
    # print_table(empty_table)
    start_point_table, start_x,start_y,end_x,end_y = startPoint(empty_table,x,y)

    #print_table(start_point_table)
    obstacle_table = obstacle(start_point_table,x , y)

    print_table(obstacle_table)
    coords = genCoordinates(obstacle_table,start_x,start_y,end_x,end_y)
    node_map = genNodeMap(obstacle_table,end_x,end_y)
    visits = dijikstra(obstacle_table,coords,start_x,start_y,end_x,end_y,node_map,x,y)

    print("""
    
    




    















    """)

    print_table( path_table(visits,obstacle_table))

    print(visits)

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
