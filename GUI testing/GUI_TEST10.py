from tkinter import *

root = Tk()

introImage = PhotoImage(file="FoSeJeenaa_small.png")
introLabel = Label(root, image=introImage)
introLabel.pack()

nextButton = Button(root, text="Continue", command=root.destroy)
nextButton.pack()

root.mainloop()


def starttest():
    print("Running Trial")


def calibrate():
    print("Now Calibrating...")


def helpme():
    print("Help!")
    help_root = Toplevel()

    help_image = PhotoImage(file="file.png")
    helplabel = Label(help_root, image=help_image)
    helplabel.pack()

    quitbutton = Button(help_root, text="Done", command=help_root.destroy)
    quitbutton.pack()

    help_root.mainloop()


root2 = Tk()

runButton = Button(root2, text="Start Test", command=starttest)
runButton.pack()

calibButton = Button(root2, text="Calibrate", command=calibrate)
calibButton.pack()

helpButton = Button(root2, text="Help!", command=helpme)
helpButton.pack()


root2.mainloop()





