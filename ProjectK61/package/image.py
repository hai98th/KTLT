from Tkinter import *
import os
 
root = Tk()
img = PhotoImage(file="add.png")
panel = Label(root, image = img)
panel.pack(side = "bottom", fill = "both", expand = "yes")
root.mainloop()
