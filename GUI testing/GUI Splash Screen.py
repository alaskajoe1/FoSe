"""
Python Tkinter Splash Screen

This script holds the class SplashScreen, which is simply a window without
the top bar/borders of a normal window.

The window width/height can be a factor based on the total screen dimensions
or it can be actual dimensions in pixels. (Just edit the useFactor property)

Very simple to set up, just create an instance of SplashScreen, and use it as
the parent to other widgets inside it.

www.sunjay-varma.com
"""

from tkinter import *

class SplashScreen(Frame):
    def __init__(self, master=None, width=1, height=0.8, useFactor=True):
        Frame.__init__(self, master)
        self.pack(side=TOP, fill=BOTH, expand=YES)

        # get screen width and height
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        w = (useFactor and ws*width) or width
        h = (useFactor and ws*height) or height
        # calculate position x, y
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))

        self.master.overrideredirect(True)
        self.lift()

if __name__ == '__main__':
    root = Tk()

    sp = SplashScreen(root)
    sp.config(bg="#3366ff")

    m = Label(sp, text="FoSe\nJeenaa!")
    m.pack(side=TOP, expand=YES)
    m.config(bg="#3366ff", justify=CENTER, font=("calibri", 29))

    Button(sp, text="Press this button to kill the program", bg='red', command=root.destroy).pack(side=BOTTOM, fill=X)
    root.mainloop()
