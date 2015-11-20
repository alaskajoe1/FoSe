from tkinter import *

root = Tk()

def printName(event):
    print("Help!")

button_1 = Button(root, text="Call for help.")
button_1.bind("<Button-1>", printName)
button_1.pack()


root.mainloop()