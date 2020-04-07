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


class Cell:

    # Static attributes

    def __init__(self, canvas, x, y, size):
        self.canvas = canvas
        self.x = int(x /size)
        self.y = int(y /size)

        self.viable = True
        self.box = self.canvas.create_rectangle(x, y, x+size, y+size, fill="white")
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
                
                self.canvas.itemconfigure(rect_id, fill="pink")


    def on_release(self, event):
        self.dragging = False



def init_weighted_search():


    #Check NESW for cell closest to end
    # root.after()
    size_y = len(myGrid.grid)
    size_x = len(myGrid.grid[0])
    holding = []
    visited = []
    visited.append([myGrid.start_cell.x,myGrid.start_cell.y])
    
    def weighted_search():

        print(myGrid.start_cell.x, myGrid.start_cell.y)
        current_visiting_node = visited[-1]
        # Check north

        x_val = current_visiting_node[0]
        y_val = current_visiting_node[1]-1

        # print("checking North:")
        # print("Current Visitng node",x_val,",",y_val," " , visited)

        try:
            if myGrid.grid[y_val][x_val].get_colour() == "white" or myGrid.grid[y_val][x_val].get_colour() == "red":
                if y_val >= 0:
                    print('North is a valid node')
                    holding.append([x_val, y_val])

        except IndexError:
            pass

        x_val = current_visiting_node[0]
        y_val = current_visiting_node[1] + 1


        try:
            if myGrid.grid[y_val][x_val].get_colour() == "white" or myGrid.grid[y_val][x_val].get_colour() == "red":
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
            if myGrid.grid[y_val][x_val].get_colour() == "white" or myGrid.grid[y_val][x_val].get_colour() == "red":
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
            if myGrid.grid[y_val][x_val].get_colour() == "white" or myGrid.grid[y_val][x_val].get_colour() == "red":
                if x_val >= 0:
                    # print('West is a valid node')
                    # print("symbol at west is",myGrid.grid[y_val][x_val])
                    holding.append([x_val, y_val])

        except IndexError:
            pass
            # print("West is out of range")

        if holding != []:
            print("We have found the following visitable nodes around",current_visiting_node)
            print("Visitable nodes",holding)

            weight_map = {}

            for node in holding:
                # print(node)
                weight_map[str(node)] = math.sqrt(((myGrid.end_cell.x - node[0])**2 + (myGrid.end_cell.y - node[1])**2))

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
            myGrid.grid[clean_list_y][clean_list_x].set_colour('blue')

            visited.append(clean_list)

        else:
            print("There are no visitable nodes ")
            print("Fixing")
            myGrid.grid[y_val][x_val].set_colour('blue')

            if len(visited) > size_x * size_y + 1:
                return False

            del visited[-1]
            current_visiting_node = visited[-1]

            # Check north

            x_val = current_visiting_node[0]
            y_val = current_visiting_node[1]
            myGrid.grid[y_val][x_val].set_colour('white')


        # myGrid.grid[myGrid.start_cell.x][myGrid.start_cell.y] 



        root.after(100,weighted_search)
    weighted_search()



root = tk.Tk()
sidebar = tk.Frame(root, width=200, height=500, borderwidth=2)

start_button  = tk.Button(sidebar, text = "Start", width = 200//5,command = init_weighted_search )
stop_button  = tk.Button(sidebar, text = "Stop", width = 200//5)
clear_button  = tk.Button(sidebar, text = "Clear", width = 200//5)


clicked = tk.StringVar()
clicked.set("Pathfinding Algorithm")
drop_down = tk.OptionMenu(sidebar, clicked, "Weighted Search", "Breath First Search")


start_button.grid(row = 0)
stop_button.grid(row = 1)
clear_button.grid(row = 2)

drop_down.grid(row=3)
sidebar.pack(expand=False, fill='both', side='right', anchor='nw')

# root.resizable(False,False)
w = tk.Canvas(root, width=500, height=500)


height = 500

width = 500


square_size = 20


# Create grid and initialise cell
    
myGrid = Grid(width, height, square_size)




# myGrid.start()

w.pack()



root.mainloop()
