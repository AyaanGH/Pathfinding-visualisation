import tkinter as tk
import random


root = tk.Tk()
sidebar = tk.Frame(root, width=200, height=500, borderwidth=2)

sidebar.pack(expand=False, fill='both', side='right', anchor='nw')


class Cell:

    # Static attributes

    def __init__(self, canvas, x, y, size):
        self.canvas = canvas
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
        self.canvas.itemcget(self.box, "fill")

    def left_press(self, event):

        items = self.canvas.find_closest(event.x, event.y)
        if items:
            rect_id = items[0]
            colour_of_rect = self.canvas.itemcget(rect_id, "fill")

        if colour_of_rect == "red" or colour_of_rect == "green" or colour_of_rect == "pink":
            self.set_colour("white")

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


# root.resizable(False,False)
w = tk.Canvas(root, width=500, height=500)


height = 500

width = 500


square_size = 20


# Create grid and initialise cell


class Grid:

    def __init__(self, width, height, square_size):
        self.grid = []
        for y in range(0, height, square_size):
            temp = []
            for x in range(0, width, square_size):

                temp.append(Cell(w, x, y, square_size))

            self.grid.append(temp)

myGrid = Grid(width, height, square_size)

myGrid.grid[0][10].set_colour('red')
myGrid.grid[10][10].set_colour('green')



w.pack()


root.mainloop()
