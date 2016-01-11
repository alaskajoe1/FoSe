import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import pyplot as plt
from matplotlib import style
import numpy as np
import tkinter as tk
from tkinter import ttk
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

    def prevImage():
        global imagePos

        forwardButton["text"] = "Next"

        imagePos -= 1
        helpLabel.configure(image=imageList[imagePos])
        helpLabel.image = imageList[imagePos]

        if imagePos == 0:
            backButton.pack_forget()




    # loads help image
    # help_image0 = tk.PhotoImage(file="IFU/Parts List.PNG")
    # imageList.append(help_image0)

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
    global maxForce
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

    # if the graph is not currently paused
    if not pause:
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
        max_text.set_text("Max Force: %.1f" % maxForce + " lbs")

        # increments the x axis if the line is within two seconds of the right side of the graph
        if t >= xmax - 2:
            axis1.set_xlim(t-18, t+2)

        # adds the new data to the line
        line1.set_data(xData, yData)

        if currentForce > redLevel:
            axis1.patch.set_facecolor('#ffbbbb')
        elif currentForce > yellowLevel:
            axis1.patch.set_facecolor('#ffffbb')
        else:
            axis1.patch.set_facecolor('#bbffbb')



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
    global startTime, pause, maxForce
    startTime = time.time()     # updates the start time to the currentTime
    maxForce = 0                # resets the maxForce to zero
    del xData[:]                # deletes all the x data
    del yData[:]                # deletes all the y data
    axis1.set_ylim(-10, 140)    # resets the y bounds
    axis1.set_xlim(0, 20)       # resets the x bounds
    pause = False               # lifts the pause so the graph can be cleared
    animate(0)                  # calls the animate function once to clear the graph
    pause = True                # sets the graph as paused


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


def changeLevels():
    levelWindow = tk.Tk()
    levelWindow.wm_title("Line Levels")

    label = ttk.Label(levelWindow, text="Please enter red line level in lbs: ", font=NORM_FONT)
    label.grid(column=0, row=0)

    rEntry = tk.Entry(levelWindow, background='#ffbbbb')
    rEntry.grid(column=1, row=0)
    rEntry.focus_set()

    label = ttk.Label(levelWindow, text="Please enter yellow line level in lbs: ", font=NORM_FONT)
    label.grid(column=0, row=1)

    yEntry = tk.Entry(levelWindow, background='#ffffbb')
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



        tk.Tk.config(self, menu=menubar)

        # initializes an array of frames
        self.frames = {}

        # loads all of our frames into existence
        for F in (StartPage, PageOne, ForceGraph):
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
class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()


# the class that displays the live, updating graph
class ForceGraph(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # function that is called when the pause/resume button is pressed
        def pauseHelper():
            if startButton["text"] == "Pause":
                pauseGraph()
                startButton["text"] = "Resume"
            else:
                resumeGraph()
                startButton["text"] = "Pause"

        # function that is called when the reset button is pressed
        def resetHelper():
            startButton["text"] = "Start"
            graphReset()


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
        startButton = ttk.Button(topFrame, text="Start", command=pauseHelper)
        startButton.pack(side='left')

        # adds goal button
        goalButton = ttk.Button(topFrame, text="Edit Goals", command=changeLevels)
        goalButton.pack(side='left')

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



fig = Figure()   # creates the graph figure
axis1 = fig.add_subplot(111)            # axis 1 is in the first slot of the 1 by 1 subplot
axis1.set_title("Force over Time")
yellowLevel = 60
redLevel = 80

yellowLine = axis1.axhline(yellowLevel, color='y', linestyle='-')     # sets yellow horizontal line
redLine = axis1.axhline(redLevel, color='r', linestyle='-')        # sets red horizontal line
axis1.grid(color='gray', linestyle='-', linewidth=.25)      # sets up the grid
axis1.set_ylabel("Force (lbs)")
axis1.set_xlabel("Time (s)")
line1, = axis1.plot([], [], 'k', lw=3)       # creates a line on the axis with no datapoints and width of 2


print("Opening phidget object....")
bridge = Bridge()            # Creates PhidgetBridge object
bridge.openPhidget()         # Opens Phidgetbridge
bridge.waitForAttach(10000)  # waits 10000 ms (10s) for bridge to connect


# variable initializations
xData = []
yData = []
startTime = time.time()
maxForce = 0
imagePos = 0
pause = True
force_text = axis1.text(0.5, 125, "0", fontsize=25)
max_text = axis1.text(0.5, 110, "0", fontsize=25)

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

#figure, animation function, how long between updates in ms
ani = animation.FuncAnimation(fig, animate, interval=1)
app.mainloop()
