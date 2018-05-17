from Tkinter import *
 
root = Tk()
root.title('Python Tk Examples @ pythonspot.com')
 
var = StringVar()
textbox = Entry(root, textvariable=var)
textbox.focus_set()
textbox.pack(pady=10, padx=10)
 
root.mainloop()
