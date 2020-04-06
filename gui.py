import tkinter as tk


root = tk.Tk()



class cell:

   def  __init__(self,x,y,ox,oy):

        self.x = x

        self.y =  y

        self.ox = ox

        self.oy = oy







root.resizable(False,False)

w = tk.Canvas(root, width = 500, height = 500)


height = 500

width = 500


square_size = 20






for y in range(0,height, square_size):
    for x in range(0, width , square_size):

         w.create_rectangle((x,y,x+square_size,y+square_size))
         




w.pack()


root.mainloop()
