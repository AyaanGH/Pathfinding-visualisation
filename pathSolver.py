"""

Generate maze to solve



"""


import random
import copy
import math
import json
import time
import os


def setSize():
    size_x = int(input('X size\n'))
    size_y = int(input('Y size\n'))

    return size_x, size_y


def construct_table(size_x, size_y):

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


def startPoint(table, xLen, yLen):
    start_x = random.randint(0, xLen-1)
    start_y = random.randint(0, yLen-1)

    # print(start_x,start_y)

    table[start_y][start_x] = 'O'

    while True:
        end_x = random.randint(0, xLen-1)
        end_y = random.randint(0, yLen-1)

        if end_x == start_x or end_y == start_y:
            continue

        table[end_y][end_x] = 'X'

        break
    # print(end_x,end_y)

    return table, start_x, start_y, end_x, end_y


def obstacle(table, x, y):
    percent_obs = 0.2
    obstacle_quantity = int(percent_obs*x*y)
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

        elif coordinate == ".":
            table[obstacle_y][obstacle_x] = "#"
            obstacles_generated += 1

    return table


def genCoordinates(table, start_x, start_y, end_x, end_y):

    coordinates = []

    for i in range(len(table)):
        for k in range(len(table[i])):
            weights = math.sqrt(((end_x - i)**2 + (end_y - k)**2))

            coordinates.append([i, k, round(weights, 4)])

    return coordinates


def weighted_search(table, coords, start_x, start_y, end_x, end_y, node_map, size_x, size_y):
    list_of_coordinates = copy.deepcopy(coords)
    stack = []
    visited = []
    stack.append([start_x, start_y])
    visited.append([start_x, start_y])
    distance_counter = 0

    while True:

        holding = []

        current_visiting_node = visited[-1]

        # print('cURRENT VISINT NODE: ', current_visiting_node)

        # Check north

        x_val = current_visiting_node[0]
        y_val = current_visiting_node[1]-1

        # print("checking North:")
        # print("Current Visitng node",x_val,",",y_val," " , visited)

        try:
            if table[y_val][x_val] == "." or table[y_val][x_val] == "X":
                if y_val >= 0:
                    # print('North is a valid node')
                    holding.append([x_val, y_val])

        except IndexError:
            pass
            # print("North is out of range")
         # Check South

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
        # Check East

        x_val = current_visiting_node[0]+1
        y_val = current_visiting_node[1]

        # print("checking East:")
        # print("Current Visitng node", x_val, ",", y_val, " ", visited)

        try:
            if table[y_val][x_val] == "." or table[y_val][x_val] == "X":
                if x_val <= size_x-1:
                    # print('East is a valid node')
                    holding.append([x_val, y_val])

        except IndexError:
            # print("East is out of range")
            pass

        # Check WEst

        x_val = current_visiting_node[0] - 1
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

                # Use dictonary to find ideal weight

            minVal = (min(weight_map, key=weight_map.get))

            if weight_map[minVal] == 0.0:
                # print("shortest found")
                del visited[0]
                return visited

            # print("best node to visit is ", minVal)

            clean_list = json.loads(minVal)
            clean_list_x = clean_list[0]
            clean_list_y = clean_list[1]
            table[clean_list_y][clean_list_x] = '#'

            visited.append(clean_list)

        else:
            print("There are no visitable nodes ")
            print("Fixing")
            table[y_val][x_val] = "#"

            if len(visited) > size_x * size_y + 1:
                return False

            del visited[-1]
            current_visiting_node = visited[-1]

            # Check north

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


def genNodeMap(table, end_x, end_y):

    node_map = {}

    for i in range(len(table)):
        for k in range(len(table[i])):
            end_distance = math.sqrt(((end_x - k)**2 + (end_y - i)**2))
            node_map['[' + str(k)+', '+str(i)+']'] = {"value": str(table[i][k]), "distance_from_start": 999,
                                                      "from": "", "distance_to_end": round(end_distance, 3), "shortest_found": False}

    # print(node_map)

    return node_map

def foundEnd(coord, end_x, end_y):

   # print("Debug, printing Coord",coord)
    k = coord[-1][0]
    i = coord[-1][1]
    end_distance = math.sqrt(((end_x - k)**2 + (end_y - i)**2))

    #print("End distance",end_distance)

    if end_distance == 1 or end_distance == 1.0:
        return True

    else:
        return False

def check_valid_north(table, coordinate, size_x, size_y):

    x_val = coordinate[0]
    y_val = coordinate[1] - 1

    try:
        if table[y_val][x_val] == "." or table[y_val][x_val] == "X":
            if y_val >= 0:
                # print('North is a valid node')

                return [x_val, y_val]

            else:
               # print('North is NOT a valid node')

                return False

    except IndexError:
        # print("North is out of range")
        return False


def check_valid_south(table, coordinate, size_x, size_y):
    x_val = coordinate[0]
    y_val = coordinate[1] + 1

    try:
        if table[y_val][x_val] == "." or table[y_val][x_val] == "X":
            if y_val <= size_y-1:
                #print('South is a valid node')

                return [x_val, y_val]

            else:
                print('South is NOT a valid node')

                return False

    except IndexError:
        # print("South is out of range")
        return False


def check_valid_east(table, coordinate, size_x, size_y):
    x_val = coordinate[0]+1
    y_val = coordinate[1]

    try:
        if table[y_val][x_val] == "." or table[y_val][x_val] == "X":
            if x_val <= size_x - 1:
                #print('east is a valid node')

                return [x_val, y_val]

            else:
               # print('east is NOT a valid node')

                return False

    except IndexError:
        #print("east is out of range")

        return False


def check_valid_west(table, coordinate, size_x, size_y):
    x_val = coordinate[0] - 1
    y_val = coordinate[1]

    try:
        if table[y_val][x_val] == "." or table[y_val][x_val] == "X":
            if x_val >= 0:
                # print('west is a valid node')

                return [x_val, y_val]

            else:
               # print('west is NOT a valid node')

                return False

    except IndexError:
        #print("west is out of range")
        return False


def valid(action, table, deque, size_x, size_y):


    if action == "N":
        return check_valid_north(table, deque, size_x, size_y)

    elif action == "S":
        return check_valid_south(table, deque, size_x, size_y)

    elif action == "E":
        return check_valid_east(table, deque, size_x, size_y)

    elif action == "W":
        return check_valid_west(table, deque, size_x, size_y)


def vibrant_table(table):
    for i in range(len(table)):
        for k in range(len(table)):

            if table[k][i] == "X":
                table[k][i] = "⛳"

            if table[k][i] == "#":
                table[k][i] = "⚪"
                #table[k][i] = "⛰️"

            if table[k][i] == ".":
                table[k][i] = "⚫"

            if table[k][i] == "O":
                table[k][i] = "⛹"

    return table


def bfs(coords, table, start_x, start_y, end_x, end_y, size_x, size_y):

    table = copy.deepcopy(table)
    pretty_table = copy.deepcopy(table)

    pretty_table = vibrant_table(pretty_table)

    print_table(pretty_table)
    input("")
    queue = []
    action_list = []
    queue.append([[start_x, start_y]])
    dequeued = queue[0]

    #last_queue_coord = queue[0][-1]

    while foundEnd(dequeued, end_x, end_y) is False:
        #print("Queue: ", queue)
        #print("Distance to end", foundEnd(dequeued, end_x, end_y))
        dequeued = queue[0]
        # TODO when on second round, it keeps checking first value of queue

        # print("Dequed Sequence: ", dequeued)
        del queue[0]
        #print("Queue remaining: ", queue)

        last_coord_of_dequed = dequeued[-1]

        for actions in ["N", "S", "E", "W"]:

           # print("in for loop, printing dequed and then 'dequed[-1]' ",dequeued)
           # print(dequeued[-1])

            check_actions = valid(
                actions, table, last_coord_of_dequed, size_x, size_y)

            # TODO check logic of adding new value to dequed or queue

            if check_actions is False or check_actions is None:
               # print(actions,"is not viable")
                continue

            dequeued_copy = copy.deepcopy(dequeued)
            dequeued_copy.append(check_actions)

            # print(add_to_dequeued)

            # TODO problem appears to be here
            queue.append(dequeued_copy)
           # print("The Queue", queue)

            #print("printing check actions ", check_actions)

            table[check_actions[1]][check_actions[0]] = "#"
            pretty_table[check_actions[1]][check_actions[0]] = "✔"
            os.system('cls')
            # print('==============================================')
            # time.sleep(0.001)
            print_table(pretty_table)

    print("FOUND END")
    print(dequeued)

    return dequeued
    # if  is True:


def path_table(visits, obstacle_table):
    print(visits)

    for node in visits:

        obstacle_table[node[1]][node[0]] = "✔️"
    obstacle_table = vibrant_table(obstacle_table)

    return obstacle_table



if __name__ == "__main__":
    while True:
        x, y = setSize()
        empty_table = construct_table(x, y)
        # print_table(empty_table)
        start_point_table, start_x, start_y, end_x, end_y = startPoint(
            empty_table, x, y)

        # print_table(start_point_table)
        obstacle_table = obstacle(start_point_table, x, y)

        print_table(obstacle_table)

        coords = genCoordinates(obstacle_table, start_x, start_y, end_x, end_y)
        node_map = genNodeMap(obstacle_table, end_x, end_y)

        weighted_search_result_table = copy.deepcopy(obstacle_table)
        weighted_search_result = weighted_search(
            weighted_search_result_table, coords, start_x, start_y, end_x, end_y, node_map, x, y)

        if weighted_search_result is False:
            print('\nNo Solution')
            continue

        print("""
        
        ======================Weighted Search=============================



        """)

        print_table(path_table(weighted_search_result,
                               weighted_search_result_table))

        print(weighted_search_result)
        print("Distance is ", len(weighted_search_result))

        cont = input("")

        print("==============BREATH FIRST SEARCH==========")

        bfs_table = copy.deepcopy(obstacle_table)

        bfs_result = bfs(coords, bfs_table, start_x,
                         start_y, end_x, end_y, x, y)

        bfs_result = bfs_result[1:]


        print_table(path_table(bfs_result, bfs_table))
        print(bfs_result)
        print("Distance is ", len(bfs_result))
    # print(coords)

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
