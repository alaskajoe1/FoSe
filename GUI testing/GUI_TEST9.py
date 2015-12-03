from tkinter import *

root = Tk()

canvas = Canvas(root, width=200, height=100)
canvas.pack()
#start(x,y), end(x,y)
blackLine = canvas.create_line(0, 0, 200, 50)
redLine = canvas.create_line(0, 100, 200, 50, fill="red")

#topLeft(x,y), width, height
greenBox = canvas.create_rectangle(25, 25, 130, 60, fill="green")

#canvas.delete(redLine)
#canvas.delete(ALL)

root.mainloop()