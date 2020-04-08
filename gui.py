import tkinter as tk
import random
import json
import math


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

                if self.grid[i][k].get_colour() != "green" and self.grid[i][k].get_colour() != "red" and self.grid[i][k].get_colour() != "pink":
                    self.grid[i][k].set_colour("white")


class Cell:

    # Static attributes

    def __init__(self, canvas, x, y, size):
        self.canvas = canvas
        self.x = int(x / size)
        self.y = int(y / size)

        self.viable = True
        self.box = self.canvas.create_rectangle(
            x, y, x+size, y+size, fill="white")
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


def init_weighted_search():
    size_y = len(myGrid.grid)
    size_x = len(myGrid.grid[0])
    visited = []
    visited.append([myGrid.start_cell.x, myGrid.start_cell.y])

    def weighted_search():

        end_loop = False
        holding = []
        # print(myGrid.start_cell.x, myGrid.start_cell.y)
        current_visiting_node = visited[-1]
        # Check north

        x_val = current_visiting_node[0]
        y_val = current_visiting_node[1]-1

        # print("checking North:")
        # print("Current Visitng node",x_val,",",y_val," " , visited)

        if x_val < 0 or y_val < 0 or x_val > size_x-1 or y_val > size_y-1:
            pass

        else:
            if myGrid.grid[y_val][x_val].get_colour() == "white" or myGrid.grid[y_val][x_val].get_colour() == "red":

                print('North is a valid node')
                holding.append([x_val, y_val])

            x_val = current_visiting_node[0]
            y_val = current_visiting_node[1] + 1

            if myGrid.grid[y_val][x_val].get_colour() == "white" or myGrid.grid[y_val][x_val].get_colour() == "red":

                # print('South is a valid node')
                holding.append([x_val, y_val])

            # print("South is out of range")
            # Check East

            x_val = current_visiting_node[0]+1
            y_val = current_visiting_node[1]

            # print("checking East:")
            # print("Current Visitng node", x_val, ",", y_val, " ", visited)

            if myGrid.grid[y_val][x_val].get_colour() == "white" or myGrid.grid[y_val][x_val].get_colour() == "red":

                # print('East is a vali d node')
                holding.append([x_val, y_val])

            # print("East is out of range")

            # Check WEst

            x_val = current_visiting_node[0] - 1
            y_val = current_visiting_node[1]

            # print("checking West:")
            # print("Current Visitng node", x_val, ",", y_val, " ", visited)

            if myGrid.grid[y_val][x_val].get_colour() == "white" or myGrid.grid[y_val][x_val].get_colour() == "red":

                # print('West is a valid node')
                # print("symbol at west is",myGrid.grid[y_val][x_val])
                holding.append([x_val, y_val])

        if holding != []:
            # print("We have found the following visitable nodes around",current_visiting_node)
            # print("Visitable nodes",holding)

            weight_map = {}

            for node in holding:
                # print(node)
                weight_map[str(node)] = math.sqrt(
                    ((myGrid.end_cell.x - node[0])**2 + (myGrid.end_cell.y - node[1])**2))

                # print('weight map')
                # print(weight_map)

                # Use dictonary to find ideal weight

            minVal = (min(weight_map, key=weight_map.get))
            print(minVal)
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

            print("Appending")
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


def clear_solve():
    myGrid.clear_solve()


root = tk.Tk()
sidebar = tk.Frame(root, width=200, height=500, borderwidth=2)

start_button = tk.Button(sidebar, text="Start",
                         width=200//5, command=init_weighted_search)
stop_button = tk.Button(sidebar, text="Stop", width=200//5)
clear_solve_button = tk.Button(
    sidebar, text="Clear Solve", width=200//5, command=clear_solve)


clicked = tk.StringVar()
clicked.set("Pathfinding Algorithm")
drop_down = tk.OptionMenu(
    sidebar, clicked, "Weighted Search", "Breath First Search")


start_button.grid(row=0)
stop_button.grid(row=1)
clear_solve_button.grid(row=2)

drop_down.grid(row=3)
sidebar.pack(expand=False, fill='both', side='right', anchor='nw')

# root.resizable(False,False)
w = tk.Canvas(root, width=500, height=500)


height = 500

width = 500


square_size = 10


# Create grid and initialise cell

myGrid = Grid(width, height, square_size)


# myGrid.start()

w.pack()


root.mainloop()
