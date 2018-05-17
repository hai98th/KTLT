from Tkinter import *
 
master = Tk()
master.minsize(300,100)
master.geometry("320x100")
 
def callback():
    print "click!"
 
 
photo=PhotoImage(file="add.png")
b = Button(master,image=photo, text="OK", command=callback, height=50, width=150, compound=LEFT)
b.place(x = 20, y = 20)
 
mainloop()
