import tkinter as tk


root = tk.Tk()



class Cell:

    def  __init__(self,canvas,x,y,size):
        self.canvas = canvas
        self.box = self.canvas.create_rectangle(x,y,x+size,y+size)
        
    def set_colour(self,colour):
        self.canvas.itemconfigure(self.box,fill=colour)









root.resizable(False,False)

w = tk.Canvas(root, width = 500, height = 500)


w.grid

height = 500

width = 500


square_size = 20


#Create grid and initialise cell

grid = []
for y in range(0,height, square_size):
    temp = []
    for x in range(0, width , square_size):

         temp.append(Cell(w,x,y,20))
    
    grid.append(temp)
         
         





grid[0][10].set_colour('red')

w.pack()


root.mainloop()
