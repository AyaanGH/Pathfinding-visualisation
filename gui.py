import tkinter as tk
import random
import json
import math
import copy
import queue


class Grid:

    def __init__(self, width, height, square_size):
        self.grid = []
        self.start_cell = None
        self.end_cell = None

        self.red_set = False
        self.green_set = False
        for y in range(0, height, square_size):
            temp = []
            for x in range(0, width, square_size):
                temp.append(Cell(w, x, y, square_size))

            self.grid.append(temp)

    def update_cell(self):

        for i in range(len(self.grid)):
            for k in range(len(self.grid[i])):

                if self.grid[i][k].get_colour() == "green":
                    self.start_cell = self.grid[i][k]

                elif self.grid[i][k].get_colour() == "red":
                    self.end_cell = self.grid[i][k]

    def clear_solve(self):
        for i in range(len(self.grid)):
            for k in range(len(self.grid[i])):

                if self.grid[i][k].get_colour() != "green" and self.grid[i][k].get_colour() != "red" and self.grid[i][
                    k].get_colour() != "pink":
                    self.grid[i][k].set_colour("white")


class Cell:

    # Static attributes

    def __init__(self, canvas, x, y, size):
        self.canvas = canvas

        self.x = int(x / size)
        self.y = int(y / size)

        self.neighbours = []

        self.viable = True
        self.box = self.canvas.create_rectangle(
            x, y, x + size, y + size, fill="white")
        # self.canvas.tag_bind(self.box,"<Motion><B1-Motion>",lambda x: self.set_colour("pink"))
        # self.colour = ""
        self.dragging = False

        self.canvas.tag_bind(self.box, "<1>", self.left_press)
        # Create obstacles
        self.canvas.bind("<ButtonPress-3>", self.on_click)
        self.canvas.bind("<B3-Motion>", self.on_move)
        self.canvas.bind("<ButtonRelease-3>", self.on_release)

    def set_colour(self, colour):
        self.canvas.itemconfigure(self.box, fill=colour)

    def get_colour(self):
        return self.canvas.itemcget(self.box, "fill")

    def left_press(self, event):

        # items = self.canvas.find_closest(event.x, event.y)
        # if items:
        #     rect_id = items[0]
        #     colour_of_rect = self.canvas.itemcget(rect_id, "fill")

        red_set = myGrid.red_set
        green_set = myGrid.green_set

        colour_of_rect = self.get_colour()

        if colour_of_rect == "red":
            self.set_colour("white")
            myGrid.red_set = False

        elif colour_of_rect == "green":
            self.set_colour("white")
            myGrid.green_set = False

        elif colour_of_rect == "white":
            if green_set == False and red_set == False:
                self.set_colour("green")
                myGrid.green_set = True

            elif green_set == True and red_set == False:
                self.set_colour("red")
                myGrid.red_set = True

            elif green_set == False and red_set == True:
                self.set_colour("green")
                myGrid.green_set = True

        myGrid.update_cell()

    def on_click(self, event):
        self.dragging = True
        self.on_move(event)

    def on_move(self, event):
        if self.dragging:
            items = self.canvas.find_closest(event.x, event.y)
            if items:
                rect_id = items[0]
                if self.canvas.itemcget(rect_id, "fill") == "red" or self.canvas.itemcget(rect_id, "fill") == "green":
                    pass
                else:
                    self.canvas.itemconfigure(rect_id, fill="pink")

    def on_release(self, event):
        self.dragging = False

    def is_closed(self):

        # todo Add orange colour
        return self.get_colour() == "orange"

    def is_open(self):
        # todo Add blue colour
        return self.get_colour() == "blue"

    def is_barrier(self):
        return self.get_colour() == "pink"

    def is_start(self):
        return self.get_colour() == "green"

    def is_end(self):
        return self.get_colour() == "red"

    def reset(self):
        self.set_colour("white")

    def make_closed(self):

        # todo Add orange colour
        self.set_colour("orange")

    def make_open(self):
        # todo Add blue colour
        return self.set_colour("blue")

    def update_neighbours(self, Grid):
        self.neighbours = []

        # Down
        if self.y < Grid.height - 1 and not Grid.grid[self.x][self.y + 1].is_barrier():
            self.neighbours.append(Grid.grid[self.x][self.y + 1])

        # Up
        if self.y > 0 and not Grid.grid[self.x][self.y - 1].is_barrier():
            self.neighbours.append(Grid.grid[self.x][self.y - 1])

        # Left
        if self.x > 0 and not Grid.grid[self.x - 1][self.y].is_barrier():
            self.neighbours.append(Grid.grid[self.x - 1][self.y])

        # right
        if self.x < Grid.width and not Grid.grid[self.x - 1][self.y].is_barrier():
            self.neighbours.append(Grid.grid[self.x + 1][self.y])


def init_a_star():
    pass


def init_weighted_search():
    clear_solve()
    size_y = len(myGrid.grid)
    size_x = len(myGrid.grid[0])
    visited = []
    visited.append([myGrid.start_cell.x, myGrid.start_cell.y])

    def weighted_search():

        end_loop = False

        if myGrid.green_set == False:
            end_loop = True

        holding = []
        # print(myGrid.start_cell.x, myGrid.start_cell.y)
        current_visiting_node = visited[-1]
        # Check north

        x_val = current_visiting_node[0]
        y_val = current_visiting_node[1] - 1

        # print("checking North:")
        # print("Current Visitng node",x_val,",",y_val," " , visited)

        try:
            if myGrid.grid[y_val][x_val].get_colour() == "white" or myGrid.grid[y_val][x_val].get_colour() == "red":

                if y_val <= size_y - 1 and y_val >= 0 and x_val >= 0:
                    # print('South is a valid node')
                    holding.append([x_val, y_val])

        except IndexError:
            pass
            # print("South is out of range")
        # Check East

        x_val = current_visiting_node[0] + 1
        y_val = current_visiting_node[1]

        # print("checking East:")
        # print("Current Visitng node", x_val, ",", y_val, " ", visited)

        try:
            if myGrid.grid[y_val][x_val].get_colour() == "white" or myGrid.grid[y_val][x_val].get_colour() == "red":
                if y_val >= 0 and y_val >= 0 and x_val >= 0:
                    # print('North is a valid node')
                    holding.append([x_val, y_val])

        except IndexError:
            pass

        x_val = current_visiting_node[0]
        y_val = current_visiting_node[1] + 1

        try:
            if myGrid.grid[y_val][x_val].get_colour() == "white" or myGrid.grid[y_val][x_val].get_colour() == "red":
                if y_val <= size_y - 1 and y_val >= 0 and x_val >= 0:
                    # print('South is a valid node')
                    holding.append([x_val, y_val])

        except IndexError:
            pass
            # print("South is out of range")
        # Check East

        x_val = current_visiting_node[0] + 1
        y_val = current_visiting_node[1]

        # print("checking East:")
        # print("Current Visitng node", x_val, ",", y_val, " ", visited)

        try:
            if myGrid.grid[y_val][x_val].get_colour() == "white" or myGrid.grid[y_val][x_val].get_colour() == "red":
                if x_val <= size_x - 1 and y_val >= 0 and x_val >= 0:
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
            if myGrid.grid[y_val][x_val].get_colour() == "white" or myGrid.grid[y_val][x_val].get_colour() == "red":
                if x_val >= 0 and y_val >= 0 and x_val >= 0:
                    # print('West is a valid node')
                    # print("symbol at west is",myGrid.grid[y_val][x_val])
                    holding.append([x_val, y_val])

        except IndexError:
            pass
            print("West is out of range")

        if holding != []:
            # print("We have found the following visitable nodes around",current_visiting_node)
            # print("Visitable nodes",holding)

            weight_map = {}

            for node in holding:
                # print(node)
                weight_map[str(node)] = math.sqrt(
                    ((myGrid.end_cell.x - node[0]) ** 2 + (myGrid.end_cell.y - node[1]) ** 2))

                # print('weight map')
                # print(weight_map)

                # Use dictonary to find ideal weight

            minVal = (min(weight_map, key=weight_map.get))

            if weight_map[minVal] == 0.0:
                # print("shortest found")
                del visited[0]
                # return visited
                end_loop = True

            # print("best node to visit is ", minVal)

            clean_list = json.loads(minVal)
            clean_list_x = clean_list[0]
            clean_list_y = clean_list[1]

            if end_loop:
                pass
            else:
                myGrid.grid[clean_list_y][clean_list_x].set_colour('blue')

            visited.append(clean_list)

        else:
            # print("There are no visitable nodes ")
            # print("Fixing")
            if (myGrid.grid[y_val][x_val].get_colour() == "green" or myGrid.grid[y_val][x_val].get_colour() == "pink"):
                pass

            else:
                myGrid.grid[y_val][x_val].set_colour('blue')

            if len(visited) > size_x * size_y + 1:
                return False

            if (myGrid.grid[visited[-1][1]][visited[-1][0]].get_colour() == "green"):
                pass

            else:
                myGrid.grid[visited[-1][1]][visited[-1][0]].set_colour("gray")

            del visited[-1]

            if len(visited) == 0:
                end_loop = True
            else:
                current_visiting_node = visited[-1]

            # Check north

            x_val = current_visiting_node[0]
            y_val = current_visiting_node[1]

            if (myGrid.grid[y_val][x_val].get_colour() == "green"):
                pass

            else:
                myGrid.grid[y_val][x_val].set_colour('white')

        # print("=========================")

        if end_loop == True:

            for node in visited[:-1]:
                myGrid.grid[node[1]][node[0]].set_colour("orange")

            myGrid.start_cell.set_colour('green')
        else:
            root.after(10, weighted_search)

    weighted_search()

    # print("Visited")
    # print(visited)
    # for node in visited:
    #     myGrid.grid[node[1]][node[0]].set_colour("yellow")
    #     root.after(100)


def init_bfs():
    size_y = len(myGrid.grid)
    size_x = len(myGrid.grid[0])

    queue = []
    queue.append([[myGrid.start_cell.x, myGrid.start_cell.y]])
    queue.append([[myGrid.start_cell.x, myGrid.start_cell.y]])

    def bfs():
        end_loop = False
        del queue[0]
        dequeued = queue[0]

        frontier_colour = "purple"

        for i in range(len(myGrid.grid)):
            for k in range(len(myGrid.grid[i])):

                if myGrid.grid[i][k].get_colour() == frontier_colour:
                    myGrid.grid[i][k].set_colour("blue")

        if myGrid.green_set == False:
            end_loop = True
        current_visiting_node = dequeued[-1]
        # Check north

        print(current_visiting_node)
        x_val = dequeued[-1][0]
        y_val = dequeued[-1][1] - 1

        # print("checking North:")
        # print("Current Visitng node",x_val,",",y_val," " , visited)

        try:
            if myGrid.grid[y_val][x_val].get_colour() == "white" or myGrid.grid[y_val][x_val].get_colour() == "red":

                if y_val <= size_y - 1 and y_val >= 0 and x_val >= 0:
                    # print('South is a valid node')
                    myGrid.grid[y_val][x_val].set_colour(frontier_colour)

                    dequeued_copy = copy.deepcopy(dequeued)
                    dequeued_copy.append([x_val, y_val])
                    queue.append(dequeued_copy)
                    # queue.append(dequeued,[x_val, y_val])

        except IndexError:
            pass
            # print("South is out of range")
        # Check East

        x_val = current_visiting_node[0] + 1
        y_val = current_visiting_node[1]

        # print("checking East:")
        # print("Current Visitng node", x_val, ",", y_val, " ", visited)

        try:
            if myGrid.grid[y_val][x_val].get_colour() == "white" or myGrid.grid[y_val][x_val].get_colour() == "red":
                if y_val >= 0 and y_val >= 0 and x_val >= 0:
                    # print('North is a valid node')
                    myGrid.grid[y_val][x_val].set_colour(frontier_colour)
                    # queue.append(dequeued,[x_val, y_val])
                    dequeued_copy = copy.deepcopy(dequeued)
                    dequeued_copy.append([x_val, y_val])
                    queue.append(dequeued_copy)

        except IndexError:
            pass

        x_val = current_visiting_node[0]
        y_val = current_visiting_node[1] + 1

        try:
            if myGrid.grid[y_val][x_val].get_colour() == "white" or myGrid.grid[y_val][x_val].get_colour() == "red":
                if y_val <= size_y - 1 and y_val >= 0 and x_val >= 0:
                    # print('South is a valid node')
                    myGrid.grid[y_val][x_val].set_colour(frontier_colour)
                    # queue.append(dequeued,[x_val, y_val])
                    dequeued_copy = copy.deepcopy(dequeued)
                    dequeued_copy.append([x_val, y_val])
                    queue.append(dequeued_copy)

        except IndexError:
            pass
            # print("South is out of range")
        # Check East

        x_val = current_visiting_node[0] + 1
        y_val = current_visiting_node[1]

        # print("checking East:")
        # print("Current Visitng node", x_val, ",", y_val, " ", visited)

        try:
            if myGrid.grid[y_val][x_val].get_colour() == "white" or myGrid.grid[y_val][x_val].get_colour() == "red":
                if x_val <= size_x - 1 and y_val >= 0 and x_val >= 0:
                    # print('East is a valid node')
                    myGrid.grid[y_val][x_val].set_colour(frontier_colour)
                    # queue.append(dequeued,[x_val, y_val])
                    dequeued_copy = copy.deepcopy(dequeued)
                    dequeued_copy.append([x_val, y_val])
                    queue.append(dequeued_copy)

        except IndexError:
            # print("East is out of range")
            pass

        # Check WEst

        x_val = current_visiting_node[0] - 1
        y_val = current_visiting_node[1]

        # print("checking West:")
        # print("Current Visitng node", x_val, ",", y_val, " ", visited)

        try:
            if myGrid.grid[y_val][x_val].get_colour() == "white" or myGrid.grid[y_val][x_val].get_colour() == "red":
                if x_val >= 0 and y_val >= 0 and x_val >= 0:
                    # print('West is a valid node')
                    # print("symbol at west is",myGrid.grid[y_val][x_val])
                    myGrid.grid[y_val][x_val].set_colour(frontier_colour)
                    # queue.append(dequeued,[x_val, y_val])
                    dequeued_copy = copy.deepcopy(dequeued)
                    dequeued_copy.append([x_val, y_val])
                    queue.append(dequeued_copy)

        except IndexError:
            pass
            print("West is out of range")

        coord = dequeued

        k = coord[-1][0]
        i = coord[-1][1]
        end_distance = math.sqrt(
            ((myGrid.end_cell.x - k) ** 2 + (myGrid.end_cell.y - i) ** 2))

        # print("End distance",end_distance)

        if end_distance == 1 or end_distance == 1.0:
            end_loop = True

        if end_loop == True:
            # print(dequeued)
            for node in dequeued:
                myGrid.grid[node[1]][node[0]].set_colour("orange")

            myGrid.start_cell.set_colour('green')
            myGrid.end_cell.set_colour('red')


        else:
            root.after(30, bfs)

    bfs()


def manhattan_distance(cell1, cell2):
    x1, y1 = cell1
    x2, y2 = cell2

    return abs(x1 - x2) + abs(y1 - y2)


def clear_solve():
    myGrid.clear_solve()


def drop_down_select():
    if clicked == "Pathfinding Algorithm":
        clicked.set("Pathfinding Algorithm")
    elif clicked == "Weighted Search":
        clicked.set("Weighted Search")

    elif clicked == "Breath First Search":
        clicked.set("Breath First Search")


def clear_all():
    for i in range(len(myGrid.grid)):
        for k in range(len(myGrid.grid[i])):
            myGrid.grid[i][k].set_colour('white')

    myGrid.red_set = False
    myGrid.green_set = False


def run_alg():
    func_map = {
        "Pathfinding Algorithm": None,
        "Weighted Search": init_weighted_search,
        "Breath First Search": init_bfs,
    }
    # using the map, get the function
    function = func_map[clicked.get()]

    # call the function
    function()


root = tk.Tk()

window_width = 700
window_height = 700

square_size = 20

sidebar = tk.Frame(root, width=200, height=window_height, borderwidth=2)

start_button = tk.Button(sidebar, text="Start",
                         width=200 // 5, command=run_alg)
clear_solve_button = tk.Button(
    sidebar, text="Clear Solve", width=200 // 5, command=clear_solve)
clear_all_button = tk.Button(
    sidebar, text="Clear All", width=200 // 5, command=clear_all)

clicked = tk.StringVar()
clicked.set("Pathfinding Algorithm")
drop_down = tk.OptionMenu(
    sidebar, clicked, "Weighted Search", "Breath First Search")

start_button.grid(row=0)
clear_solve_button.grid(row=2)
clear_all_button.grid(row=3)

drop_down.grid(row=4)
sidebar.pack(expand=False, fill='both', side='right', anchor='nw')

# root.resizable(False,False)
w = tk.Canvas(root, width=window_width, height=window_height)

# Create grid and initialise cell

myGrid = Grid(window_width, window_height, square_size)

# myGrid.start()

w.pack()

root.mainloop()
