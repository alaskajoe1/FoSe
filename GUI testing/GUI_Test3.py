from tkinter import *

root = Tk()

# bg = background; fg = foreground
one = Label(root, text="One", bg="blue", fg="yellow")
one.pack()

two = Label(root, text="Two", bg="green", fg="black")
two.pack(fill=X) # stretch the label as wide as the parent in the x direction

three = Label(root, text="Three", bg="red", fg="white")
three.pack(side=LEFT, fill=Y)


root.mainloop()