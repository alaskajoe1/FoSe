import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import pyplot as plt
from matplotlib import style
import numpy as np
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as tkFileDialog
from Phidgets.Devices.Bridge import Bridge, BridgeGain
import time
matplotlib.use("TkAgg")

LARGE_FONT = ("Verdana", 12)    # sets a font style
NORM_FONT = ("Verdana", 12)    # sets a font style
SMALL_FONT = ("Verdana", 12)    # sets a font style

style.use("ggplot")             # sets a matplotlib style

# Information Display Function
def displayDeviceInfo():
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (
        bridge.isAttached(), bridge.getDeviceName(), bridge.getSerialNum(), bridge.getDeviceVersion()))
    print("|------------|----------------------------------|--------------|------------|")

    # sets data rate (number of ms between data collection)
    # must be a multiple of 8 ms (125 Hz to 1 Hz)
    bridge.setDataRate(24)
    time.sleep(0.2)
    print(" Data rate set to: %4d ms   %.1f Hz" % (bridge.getDataRate(), 1/(bridge.getDataRate()*0.001)))

    # Gain	Resoluion	Range
    #  1	119 nV/V 	1000 mV/V
    #  8	14.9 nV/V	125 mV/V
    # 16	7.45 nV/V	62.5 mV/V
    # 32	3.72 nV/V	31.25 mV/V
    # 64	1.86 nV/V	15.625 mV/V
    # 128	0.92 nV/V   7.8125 mV/V

    # Force sensor maxes out around 4 mV/V so set gain to 128
    bridge.setGain(1, BridgeGain.PHIDGET_BRIDGE_GAIN_128)
    time.sleep(0.2)
    print("Gain set to: ", bridge.getGain(1))

    # Sensor hooked up to input 1 on the PhidgetBridge
    print("Enabling  Bridge input 1 for reading data...")
    bridge.setEnabled(1, True)
    time.sleep(0.2)


# function that creates the report after a Max Force exercise is completed
def maxForceReport(theArray):

    text = ""

    # adds the label text for each trial
    for i in range(len(theArray)):
        text += "Trial " + str(i+1) + ": {:0.2f}\n".format(theArray[i])

    # adds on the mean, max, and coefficient of variation (CV)
    text += "Average: {:0.3f} \nMax: {:0.2f} \nCV: {:0.4f}".format(float(np.mean(theArray)), max(theArray),
                                                                   float(np.std(theArray)/np.mean(theArray)))

    print(text)
    app.frames[ResultsDisplay].changeText(text)


# function used to switch between exercises
def changeExercise(toWhat):
    global exercise, countdown, xrange, pause, maxForceArray

    pause = True
    exercise = toWhat

    if exercise == "maxForce":
        axis1.set_title("Max Force", fontsize=24)
        countdown_text.set_text("Press Start!")
        rep_text.set_text("Rep 1 of " + str(numReps))
        countdown = 'r'
        axis1.set_xlim(0, 10)
        xrange = 10
        del maxForceArray[:]
        redLine.set_linewidth(0)
        yellowLine.set_linewidth(0)
    elif exercise == "reps":
        axis1.set_title("Reps", fontsize=24)
        countdown_text.set_text("Press Start!")
        rep_text.set_text("Rep 0")
        countdown = 'r'
        axis1.set_xlim(0, 30)
        xrange = 30
        redLine.set_linewidth(3)
        yellowLine.set_linewidth(3)
    elif exercise == "holdForce":
        axis1.set_title("Hold Force", fontsize=24)
        countdown_text.set_text("Press Start!")
        rep_text.set_text("Max: 0 s")
        countdown = 'r'
        axis1.set_xlim(0, 30)
        xrange = 30
        redLine.set_linewidth(3)
        yellowLine.set_linewidth(3)
    else:
        axis1.set_title("Force over Time", fontsize=24)
        countdown_text.set_text("")
        rep_text.set_text("")
        countdown = 'n'
        axis1.set_xlim(0, 20)
        xrange = 20
        redLine.set_linewidth(3)
        yellowLine.set_linewidth(3)

    graphReset()
    app.frames[ForceGraph].changeStartButton("Start")



def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command=popup.destroy)
    B1.pack()
    popup.mainloop()


def helpScreen():
    helpScreen = tk.Toplevel()  #can't use Tk here as you can only have one Tkinter at a time with images
    helpScreen.wm_title("Help!")

    w = 1280 # width for the Tk root
    h = 760 # height for the Tk root
    # calculate x and y coordinates for the Tk root window
    x = 0
    y = 0
    # set the dimensions of the screen
    # and where it is placed
    helpScreen.geometry('%dx%d+%d+%d' % (w, h, x, y))


    imageList = []

    # cycles through to the next image in the help series
    def nextImage():
        global imagePos

        imagePos += 1
        backButton.pack(side='right')

        if imagePos == (len(imageList)):
            imagePos = 1
            helpScreen.destroy()
        else:
            helpLabel.configure(image=imageList[imagePos])
            helpLabel.image = imageList[imagePos]
            if imagePos == (len(imageList)-1):
                forwardButton["text"] = "Done"

    # cycles to the previous image in the series
    def prevImage():
        global imagePos

        forwardButton["text"] = "Next"

        imagePos -= 1
        helpLabel.configure(image=imageList[imagePos])
        helpLabel.image = imageList[imagePos]

        if imagePos == 0:
            backButton.pack_forget()




    # loads help image
    help_image1 = tk.PhotoImage(file="IFU/Slide1.png")
    imageList.append(help_image1)

    help_image2 = tk.PhotoImage(file="IFU/Slide2.PNG")
    imageList.append(help_image2)

    help_image3 = tk.PhotoImage(file="IFU/Slide3.PNG")
    imageList.append(help_image3)

    help_image4 = tk.PhotoImage(file="IFU/Slide4.PNG")
    imageList.append(help_image4)

    help_image5 = tk.PhotoImage(file="IFU/Slide5.PNG")
    imageList.append(help_image5)

    help_image6 = tk.PhotoImage(file="IFU/Slide6.PNG")
    imageList.append(help_image6)

    help_image7 = tk.PhotoImage(file="IFU/Slide7.PNG")
    imageList.append(help_image7)

    help_image8 = tk.PhotoImage(file="IFU/Slide8.PNG")
    imageList.append(help_image8)

    helpLabel = ttk.Button(helpScreen, image=imageList[imagePos], command=nextImage)#, borderwidth=0, relief='flat')
    helpLabel.image = imageList[0]
    helpLabel.pack(side='top')

    bottomFrame = tk.Frame(helpScreen)
    bottomFrame.pack(side='bottom', fill=tk.BOTH, expand=True)

    # button to progress through the images
    forwardButton = ttk.Button(bottomFrame, text="Next", command=nextImage)
    forwardButton.pack(side='right')

    backButton = ttk.Button(bottomFrame, text="Back", command=prevImage)
    backButton.pack(side='right')

    if imagePos == 0:
        backButton.pack_forget()

    if imagePos == (len(imageList)-1):
        forwardButton["text"] = "Done"

    helpScreen.mainloop()


# animate function that updates the graph
def animate(i):
    global maxForce, exercise, countdown, pause, startTime, started, finished, endTimer, repCounter, repReset
    global repTimer, restTimer, maxHoldTime

    # calculates seconds since program started running
    t = time.time() - startTime
    # converts bridge voltage output to lbs
    y = (bridge.getBridgeValue(1) + forceSensorOffset) * 74.3  # lbs/mV

    # gets the current dimensions of the graph
    xmin, xmax = axis1.get_xlim()
    ymin, ymax = axis1.get_ylim()

    # positions the text so that it is always in the same spot
    force_text.set_position(((xmax-xmin)*0.05+xmin, (ymax-ymin)*0.9+ymin))
    max_text.set_position(((xmax-xmin)*0.05+xmin, (ymax-ymin)*0.8+ymin))
    countdown_text.set_position(((xmax-xmin)*0.5+xmin, (ymax-ymin)*0.8+ymin))
    rep_text.set_position(((xmax-xmin)*0.85+xmin, (ymax-ymin)*0.9+ymin))

    print(countdown, pause, started, finished, t)

    if not ignoreOnReset:

        if ((countdown == 'r' and not pause) or (countdown == 's')):

            force_text.set_text("Current Force: 0.0 lbs")

            if countdown == 'r':
                startTime = time.time()
                t = 0

            pause = True
            countdown = 's'

            if 3 < t:
                countdown_text.set_text("   GO!")
                axis1.patch.set_facecolor('#bbffbb')
                pause = False
                countdown = 'n'
                startTime = time.time()
                t = 0

            elif 2 < t < 3:
                countdown_text.set_text("   1")
                axis1.patch.set_facecolor('#ffffbb')
            elif 1 < t < 2:
                countdown_text.set_text("   2")
            elif 0 < t < 1:
                countdown_text.set_text("   3")
                axis1.patch.set_facecolor('#ffbbbb')
        elif countdown == 'n':
            if 3 < t and exercise == "maxForce":
                countdown_text.set_text("")


        if finished:
            time.sleep(2)
            maxForceArray.append(maxForce)
            rep_text.set_text("Rep " + str(len(maxForceArray)+1) + " of " + str(numReps))
            print(maxForceArray)
            graphReset()

            if numReps == len(maxForceArray):
                maxForceReport(maxForceArray)
                app.show_frame(ResultsDisplay)

    # if the graph is not currently paused
    if not pause:

        if exercise == "maxForce":
            # trial is determined to have started when the force is over 2 lbs
            if y > 2 and not started:
                started = True

            # trial is over when force drops below 10% max force for 1 second
            if y < maxForce*0.1 and started:
                if endTimer == 0:
                    endTimer = t

                if (t - endTimer) > 1:
                    finished = True
                    countdown_text.set_text("Good Job!")

            else:
                endTimer = 0

        # append the new data points on to the data
        xData.append(t)
        yData.append(y)

        # data smoothing (averages last two data points)
        if len(yData) > 2:
                yData[len(yData)-1] = (np.mean(yData[(-2):]))
                # print(1/(xData[-1] - xData[-2])) # prints frame rate


        # grabs the current force measurement
        currentForce = yData[-1]

        # updates the maxForce
        if currentForce > maxForce:
            maxForce = currentForce

        # updates the current force and max force text on the screen
        force_text.set_text("Current Force: %.1f" % currentForce + " lbs")

        if exercise == "demo":
            max_text.set_text("Max Force: %.1f" % maxForce + " lbs")

            if currentForce > redLevel:
                axis1.patch.set_facecolor('#ffbbbb')  # red
            elif currentForce > yellowLevel:
                axis1.patch.set_facecolor('#ffffbb')  # yellow
            else:
                axis1.patch.set_facecolor('#bbffbb')  # green

        elif exercise == "reps":
            if currentForce > redLevel:
                axis1.patch.set_facecolor('#ffbbbb')  # red

            elif currentForce > yellowLevel:

                if repReset and (t - repTimer) > repTime:
                    repCounter += 1
                    rep_text.set_text("Rep " + str(repCounter))
                    countdown_text.set_text("Relax")
                    axis1.patch.set_facecolor('#ffffbb')  # yellow
                    restTimer = t
                    repReset = False

                if repReset and (t - repTimer) < repTime:
                    axis1.patch.set_facecolor('#bbbbff')  # blue


            else:
                repTimer = t
                if currentForce < 5 and (t - restTimer) > restTime:
                    repReset = True
                    countdown_text.set_text("Go!")

                if repReset:
                    axis1.patch.set_facecolor('#bbffbb')  # green

        elif exercise == "holdForce":
            if currentForce > redLevel:
                axis1.patch.set_facecolor('#ffbbbb')  # red

            elif currentForce > yellowLevel:

                countdown_text.set_text("{:0.2f} s".format(t - repTimer))
                axis1.patch.set_facecolor('#bbffbb')  # green


                if (t - repTimer) > maxHoldTime:
                    maxHoldTime = (t - repTimer)
                    rep_text.set_text("Max: {:0.2f} s".format(maxHoldTime))


            else:
                repTimer = t
                axis1.patch.set_facecolor('#ffffbb')  # yellow



        # increments the x axis if the line is within 90% of the right side of the graph
        if t >= xmax - xrange*0.1:
            axis1.set_xlim(t-xrange*0.9, t+xrange*0.1)

        # adds the new data to the line
        line1.set_data(xData, yData)





    #returns the updated line
    return line1


# used to zero the force sensor
def calibrate():
    global forceSensorOffset
    # offset equals opposite of current value
    forceSensorOffset = -bridge.getBridgeValue(1)
    force_text.set_text("Current Force: %.1f" % 0 + " lbs")


# used to reset the graph
def graphReset():
    global startTime, pause, maxForce, countdown, started, finished, ignoreOnReset, repReset, restTimer, repTimer
    global maxHoldTime, repCounter, exercise
    startTime = time.time()     # updates the start time to the currentTime
    maxForce = 0                # resets the maxForce to zero
    del xData[:]                # deletes all the x data
    del yData[:]                # deletes all the y data
    axis1.set_ylim(yrange[0], yrange[1])    # resets the y bounds
    axis1.set_xlim(0, xrange)   # resets the x bounds
    pause = False               # lifts the pause so the graph can be cleared
    finished = False            # resets finished to prevent recursive call
    repReset = True
    repCounter = 0
    restTimer = 0
    repTimer = 0
    maxHoldTime = 0
    started = False
    ignoreOnReset = True
    force_text.set_text("Current Force: 0.0 lbs")
    print("Graph Reset!")
    animate(0)                  # calls the animate function once to clear the graph
    ignoreOnReset = False
    pause = True                # sets the graph as paused


    countdown_text.set_text("Press Start!")
    countdown = 'r'
    app.frames[ForceGraph].changeStartButton("Start")




# pauses data collection
def pauseGraph():
    global pause
    pause = True

# resumes the graph after it is paused
def resumeGraph():
    global pause, startTime, maxForce
    pause = False
    if len(xData) > 0:
        # adjust the start time so the graph picks up where it left off
        startTime = time.time() - xData[-1]
    else:
        # if we're resuming from a reset initializes the start time
        startTime = time.time()


def changeXRange():
    xRangeWindow = tk.Tk()
    xRangeWindow.wm_title("X Range")

    label = ttk.Label(xRangeWindow, text="Please enter new x range (s): ", font=NORM_FONT)
    label.grid(column=0, row=0, padx=10, pady=20)

    entry = tk.Entry(xRangeWindow)
    entry.insert(tk.END, str(xrange))
    entry.grid(column=1, row=0, padx=0, pady=20)
    entry.focus_set()

    def callback():
        global xrange
        xrange = float(entry.get())
        axis1.set_xlim(0, xrange)   # resets the x bounds
        xRangeWindow.destroy()

    B1 = ttk.Button(xRangeWindow, text="Okay", command=callback)
    B1.grid(column=2, row=0, padx=10, pady=20)
    xRangeWindow.mainloop()

def changeRestTime():
    restTimeWindow = tk.Tk()
    restTimeWindow.wm_title("Rest Time")

    label = ttk.Label(restTimeWindow, text="Please enter new rest time (s): ", font=NORM_FONT)
    label.grid(column=0, row=0, padx=10, pady=20)

    entry = tk.Entry(restTimeWindow)
    entry.insert(tk.END, str(restTime))
    entry.grid(column=1, row=0, padx=0, pady=20)
    entry.focus_set()

    def callback():
        global restTime
        restTime = float(entry.get())
        restTimeWindow.destroy()

    B1 = ttk.Button(restTimeWindow, text="Okay", command=callback)
    B1.grid(column=2, row=0, padx=10, pady=20)
    restTimeWindow.mainloop()

def changeRepTime():
    repTimeWindow = tk.Tk()
    repTimeWindow.wm_title("Rest Time")

    label = ttk.Label(repTimeWindow, text="Please enter new rep time (s): ", font=NORM_FONT)
    label.grid(column=0, row=0, padx=10, pady=20)

    entry = tk.Entry(repTimeWindow)
    entry.insert(tk.END, str(repTime))
    entry.grid(column=1, row=0, padx=0, pady=20)
    entry.focus_set()

    def callback():
        global repTime
        repTime = float(entry.get())
        repTimeWindow.destroy()

    B1 = ttk.Button(repTimeWindow, text="Okay", command=callback)
    B1.grid(column=2, row=0, padx=10, pady=20)
    repTimeWindow.mainloop()

def changeYRange():
    yRangeWindow = tk.Tk()
    yRangeWindow.wm_title("Y Range")

    label1 = ttk.Label(yRangeWindow, text="Please enter new y max (lbs): ", font=NORM_FONT)
    label1.grid(column=0, row=0)

    label2 = ttk.Label(yRangeWindow, text="Please enter new y min (lbs): ", font=NORM_FONT)
    label2.grid(column=0, row=1)

    entry1 = tk.Entry(yRangeWindow)
    entry1.insert(tk.END, str(yrange[0]))
    entry1.grid(column=1, row=0)
    entry1.focus_set()

    entry2 = tk.Entry(yRangeWindow)
    entry2.insert(tk.END, str(yrange[1]))
    entry2.grid(column=1, row=1)
    entry2.focus_set()

    def callback():
        global yrange

        yrange1 = float(entry1.get())
        yrange2 = float(entry2.get())
        yrange[1] = min([yrange1, yrange2])
        yrange[0] = max([yrange1, yrange2])
        axis1.set_ylim(yrange[0], yrange[1])    # resets the y bounds
        yRangeWindow.destroy()

    B1 = ttk.Button(yRangeWindow, text="Okay", command=callback)
    B1.grid(column=0, row=2, columnspan=2)
    yRangeWindow.mainloop()

def changeReps():
    repsWindow = tk.Tk()
    repsWindow.wm_title("Number of Reps")

    label1 = ttk.Label(repsWindow, text="Please enter new number of reps: ", font=NORM_FONT)
    label1.grid(column=0, row=0, padx=10, pady=20)

    entry = tk.Entry(repsWindow)
    entry.insert(tk.END, str(numReps))
    entry.grid(column=1, row=0, padx=0, pady=20)
    entry.focus_set()

    def callback():
        global numReps
        numReps = int(entry.get())
        repsWindow.destroy()

    B1 = ttk.Button(repsWindow, text="Okay", command=callback)
    B1.grid(column=3, row=0, padx=10, pady=20)
    repsWindow.mainloop()


def settingsPage():
    settingsWindow = tk.Tk()
    settingsWindow.wm_title("Settings")

    changeLineButton = ttk.Button(settingsWindow, text="Line Levels", command=changeLevels)
    changeLineButton.pack()

    changeXRangeButton = ttk.Button(settingsWindow, text="X Range", command=changeXRange)
    changeXRangeButton.pack()

    changeYRangeButton = ttk.Button(settingsWindow, text="Y Range", command=changeYRange)
    changeYRangeButton.pack()

    changeNumRepsButton = ttk.Button(settingsWindow, text="Num Reps", command=changeReps)
    changeNumRepsButton.pack()

    changeRestButton = ttk.Button(settingsWindow, text="Rest Time", command=changeRestTime)
    changeRestButton.pack()

    changeRepTimeButton = ttk.Button(settingsWindow, text="Rep Time", command=changeRepTime)
    changeRepTimeButton.pack()

    doneButton = ttk.Button(settingsWindow, text="Done", command=lambda: settingsWindow.destroy())
    doneButton.pack()

    settingsWindow.mainloop()


# change the levels of the red and yellow lines
def changeLevels():
    levelWindow = tk.Tk()
    levelWindow.wm_title("Line Levels")

    label = ttk.Label(levelWindow, text="Please enter red line level in lbs: ", font=NORM_FONT)
    label.grid(column=0, row=0)

    rEntry = tk.Entry(levelWindow, background='#ffbbbb')
    rEntry.insert(tk.END, str(redLevel))
    rEntry.grid(column=1, row=0)
    rEntry.focus_set()

    label = ttk.Label(levelWindow, text="Please enter yellow line level in lbs: ", font=NORM_FONT)
    label.grid(column=0, row=1)

    yEntry = tk.Entry(levelWindow, background='#ffffbb')
    yEntry.insert(tk.END, str(yellowLevel))
    yEntry.grid(column=1, row=1)
    yEntry.focus_set()

    def callback():
        global yellowLine, redLine, yellowLevel, redLevel

        redLevel = float(rEntry.get())
        yellowLevel = float(yEntry.get())
        redLine.set_ydata([redLevel, redLevel])
        yellowLine.set_ydata([yellowLevel, yellowLevel])
        levelWindow.destroy()


    B1 = ttk.Button(levelWindow, text="Okay", command=callback)
    B1.grid(column=0, row=2, columnspan=2)
    levelWindow.mainloop()



# inheritance go inside parenthesis
class FosEAppMain(tk.Tk):

    # initialize method
    # *args = arguments (whatever variable you want to pass
    # *kwargs = keyword args (pass through dictionaries)
    def __init__(self, *args, **kwargs):
        # initialize tkinter
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default="FoSe.ico")  # changes the program icon
        tk.Tk.wm_title(self, "FoSe Jeenaa")         # change the window title
        # tk.Tk.wm_state(self, "zoomed")            # makes the window fullscreen

        # Frame is a window
        container = tk.Frame(self)

        # fill will fill in the space allotted to the pack
        # expand expands to fill the window
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save Settings", command=lambda: popupmsg("Not supported yet!"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)

        exerciseChoice = tk.Menu(menubar, tearoff=1)
        exerciseChoice.add_command(label="Max Force",
                                   command=lambda: changeExercise("maxForce"))
        exerciseChoice.add_command(label="Hold Force",
                                   command=lambda: changeExercise("holdForce"))
        exerciseChoice.add_command(label="Repetitions",
                                   command=lambda: changeExercise("reps"))
        exerciseChoice.add_command(label="Demo",
                                   command=lambda: changeExercise("demo"))

        menubar.add_cascade(label="Change Exercise", menu=exerciseChoice)

        tk.Tk.config(self, menu=menubar)

        # initializes an array of frames
        self.frames = {}

        # loads all of our frames into existence
        for F in (StartPage, ResultsDisplay, ForceGraph):
            frame = F(container, self)
            self.frames[F] = frame

            # sticky is the alignment + stretch
            frame.grid(row=0, column = 0, sticky="nsew")

        # shows the start page
        self.show_frame(StartPage)

    # brings the identified frame to the front where it can be seen
    def show_frame(self, cont):
        frame = self.frames[cont]

        #if the Force Graph is brought to the front, reset it
        if cont == ForceGraph:
            graphReset()

        # raises it to the front
        frame.tkraise()


# start page (splash screen)
class StartPage(tk.Frame):

    # initialization function
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # loads intro image
        introImage = tk.PhotoImage(file="FoSeLogo_crop.png")
        introLabel = tk.Label(self, image=introImage)
        introLabel.image = introImage
        introLabel.pack()

        # loads intro text
        label = tk.Label(self,
        text=
    """   This physical therapy application is still in development. Use at your own risk. Always consult with
    your physical therapist before starting this or any other rehabilitation program to determine if it is
    right for your needs. If you experience faintness, dizziness, pain or shortness of breath at any time
    while using this device you should stop immediately.""",
        font=LARGE_FONT, justify='left'
                         )
        label.pack(pady=10, padx=10)

        # adds the agree button
        button1 = ttk.Button(self, text="I Agree",
                            command=lambda: controller.show_frame(ForceGraph))
        button1.pack()

        # adds the disagree button
        button2 = ttk.Button(self, text="I Disagree", command=quit)
        button2.pack()

# Blank page for future use
class ResultsDisplay(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global maxForceArray

        labelText = ""

        # function for saving a file
        def saveFile():
            writeFile = tkFileDialog.asksaveasfile(mode='w')
            writeFile.write(self.label1["text"])
            writeFile.close()

        def quitAndReset():
            changeExercise("maxForce")
            controller.show_frame(ForceGraph)

        # adds this text to the screen
        self.label1 = ttk.Label(self, text=labelText)
        self.label1.pack()

        # adds the save button
        saveButton = ttk.Button(self, text="Save", command=saveFile)
        saveButton.pack()

        # adds the exit button
        exitButton = ttk.Button(self, text="Done", command=quitAndReset)
        exitButton.pack()

     # allows for outside modification of the text
    def changeText(self, newText):
        self.label1.config(text=newText)



# the class that displays the live, updating graph
class ForceGraph(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # function that is called when the pause/resume button is pressed
        def pauseHelper():
            if self.startButton["text"] == "Pause":
                pauseGraph()
                self.startButton["text"] = "Resume"
            else:
                resumeGraph()
                self.startButton["text"] = "Pause"

        # function that is called when the reset button is pressed
        def resetHelper():
            self.startButton["text"] = "Start"
            changeExercise(exercise)

        topFrame = tk.Frame(self)
        topFrame.pack(side='top')

        bottomFrame = tk.Frame(self)
        bottomFrame.pack(side='bottom', fill=tk.BOTH, expand=True)

        # adds the calibrate button
        zeroButton = ttk.Button(topFrame, text="Zero Force Sensor", command=calibrate)
        zeroButton.pack(side='left')

        #adds the reset button
        resetButton = ttk.Button(topFrame, text="Reset", command=resetHelper)
        resetButton.pack(side='left')

        # adds the start/pause/resume button
        self.startButton = ttk.Button(topFrame, text="Start", command=pauseHelper)
        self.startButton.pack(side='left')

        # adds settings button
        settingsButton = ttk.Button(topFrame, text="Settings", command=settingsPage)
        settingsButton.pack(side='left')

        # adds the help button
        helpButton = ttk.Button(topFrame, text="Help!", command=helpScreen)
        helpButton.pack(side='left')


        # adds the plot to the window
        canvas = FigureCanvasTkAgg(fig, bottomFrame)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)


        # adds the matplotlib toolbar to the window
        toolbar = NavigationToolbar2TkAgg(canvas, bottomFrame)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # allows for outside modification of the start button text
    def changeStartButton(self, newText):
        self.startButton.config(text=newText)


fig = Figure()   # creates the graph figure
axis1 = fig.add_subplot(111)            # axis 1 is in the first slot of the 1 by 1 subplot
yellowLevel = 30
redLevel = 50

yellowLine = axis1.axhline(yellowLevel, color='y', linestyle='-')     # sets yellow horizontal line
redLine = axis1.axhline(redLevel, color='r', linestyle='-')        # sets red horizontal line
axis1.grid(color='gray', linestyle='-', linewidth=.25)      # sets up the grid
axis1.set_ylabel("Force (lbs)", fontsize=18)
axis1.set_xlabel("Time (s)", fontsize=18)
line1, = axis1.plot([], [], 'k', lw=3)       # creates a line on the axis with no datapoints and width of 2
axis1.tick_params(axis='both', which='major', labelsize=16)


print("Opening phidget object....")
bridge = Bridge()            # Creates PhidgetBridge object
bridge.openPhidget()         # Opens Phidgetbridge
bridge.waitForAttach(10000)  # waits 10000 ms (10s) for bridge to connect


# variable initializations
xData = []
yData = []
startTime = time.time()
maxForce = 0
maxForceArray = []
imagePos = 0
xrange = 20
yrange = [-10, 140]
repCounter = 0
numReps = 3

'''
pause = True
exerciseName = "maxForce"
countdown = False
'''

ignoreOnReset = False
started = False
finished = False
repReset = True
repTime = 1
restTime = 3
restTimer = 0
repTimer = 0
endTimer = 0
maxHoldTime = 0
force_text = axis1.text(0.5, 125, "", fontsize=25)
max_text = axis1.text(0.5, 110, "", fontsize=25)
countdown_text = axis1.text(9, 90, "", fontsize=40)
rep_text = axis1.text(10, 110, "", fontsize=25)

time.sleep(1)
displayDeviceInfo()
forceSensorOffset = -bridge.getBridgeValue(1)




app = FosEAppMain()

s = ttk.Style()
s.configure('.', font=('Times New Roman', 16))

w = 1280 # width for the Tk root
h = 720 # height for the Tk root

# get screen width and height
ws = app.winfo_screenwidth() # width of the screen
hs = app.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = 0

# set the dimensions of the screen
# and where it is placed
app.geometry('%dx%d+%d+%d' % (w, h, x, y))
changeExercise("reps")

#figure, animation function, how long between updates in ms
ani = animation.FuncAnimation(fig, animate, interval=1)

app.mainloop()
