from tkinter import *

root = Tk()

# Creates a frame (invisible container) and adds it to the frame
topFrame = Frame(root)
topFrame.pack()

# Creates another frame and adds it to the bottom
bottomFrame = Frame(root)
bottomFrame.pack(side=BOTTOM)

button1 = Button(topFrame, text="Button 1", fg="red")
button2 = Button(topFrame, text="Button 2", fg="blue")
button3 = Button(topFrame, text="Button 3", fg="green")
button4 = Button(bottomFrame, text="Click me!", fg="purple")

#must pack widgets before they appear
button1.pack(side=LEFT)
button2.pack(side=LEFT)
button3.pack(side=LEFT)
button4.pack(side=BOTTOM)

root.mainloop()