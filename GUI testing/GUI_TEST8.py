from tkinter import *
import tkinter.messagebox

root = Tk()

tkinter.messagebox.showinfo("Window Title", "This is the main body text.")

answer = tkinter.messagebox.askquestion("Question 1", "Have you ever torn your ACL?")

if answer == "yes":
    print(":(")
else:
    print(":)")

root.mainloop()