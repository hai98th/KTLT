from  Tkinter import *
import Tkinter, Tkconstants, tkFileDialog
root = Tk()
root.directory = tkFileDialog.askdirectory()
print (root.directory)
