from Tkinter import *
import Tkinter, Tkconstants, tkFileDialog
 
root = Tk()
root.filename = tkFileDialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
print (root.filename)
