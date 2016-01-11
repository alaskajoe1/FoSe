import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import tkinter as tk
from tkinter import ttk
from Phidgets.Devices.Bridge import Bridge, BridgeGain
import time
matplotlib.use("TkAgg")


LARGE_FONT = ("Verdana", 12)
style.use("ggplot")

fig = Figure(figsize=(5, 5), dpi=100)
# 1 by 1 of 1
axis1 = fig.add_subplot(111)
line1, = axis1.plot([], [], lw=2)

print("Opening phidget object....")

# Creates bridge object
bridge = Bridge()
# Opens phidget
bridge.openPhidget()
# waits 10000 ms (10s) for bridge to connect
bridge.waitForAttach(10000)


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
    time.sleep(.2)
    print("Data rate set to: ", bridge.getDataRate(), "ms    ", 1 / (bridge.getDataRate() * 0.001), " Hz")

    # Gain	Resoluion	Range
    #  1	119 nV/V 	1000 mV/V
    #  8	14.9 nV/V	125 mV/V
    # 16	7.45 nV/V	62.5 mV/V
    # 32	3.72 nV/V	31.25 mV/V
    # 64	1.86 nV/V	15.625 mV/V
    # 128	0.92 nV/V   7.8125 mV/V

    # Force sensor maxes out around 4 mV/V so set gain to 128
    bridge.setGain(1, BridgeGain.PHIDGET_BRIDGE_GAIN_128)
    time.sleep(.2)
    print("Gain set to: ", bridge.getGain(1))

    # Sensor hooked up to input 1 on the PhidgetBridge
    print("Enabling  Bridge input 1 for reading data...")
    bridge.setEnabled(1, True)
    time.sleep(.2)


def init():
    axis1.set_ylim(-10, 140)
    axis1.set_xlim(0, 20)
    line1.set_data(xData, yData)


def animate(i):
    global maxForce
    # calculates seconds since program started running
    t = time.time() - startTime
    # converts bridge voltage output to lbs
    y = (bridge.getBridgeValue(1) + forceSensorOffset) * 74.3  # lbs/mV

    xmin, xmax = axis1.get_xlim()
    ymin, ymax = axis1.get_ylim()

    force_text.set_position(((xmax-xmin)*0.05+xmin, (ymax-ymin)*0.9+ymin))
    max_text.set_position(((xmax-xmin)*0.05+xmin, (ymax-ymin)*0.8+ymin))

    if not pause:
        xData.append(t)
        yData.append(y)

        if len(yData) > 5:
                yData[len(yData)-1] = (np.mean(yData[(len(yData) - 2):]))

        currentForce = yData[len(yData)-1]

        if currentForce > maxForce:
            maxForce = currentForce

        force_text.set_text("Current Force: %.1f" % currentForce + " lbs")
        max_text.set_text("Max Force: %.1f" % maxForce + " lbs")



        if t >= xmax - 2:
            axis1.set_xlim(t-18, t+2)   # increment the x-axis


        line1.set_data(xData, yData)

    return line1

# used to zero the force sensor
def calibrate():
    global forceSensorOffset
    #offset equals opposite of current value
    forceSensorOffset = -bridge.getBridgeValue(1)


def graphReset():
    global startTime, pause, maxForce
    startTime = time.time()
    maxForce = 0
    del xData[:]
    del yData[:]
    axis1.set_ylim(-10, 140)
    axis1.set_xlim(0, 20)
    pause = False


def pauseGraph():
    global pause
    pause = True

def resumeGraph():
    global pause, startTime, maxForce
    pause = False
    startTime = time.time() - xData[len(xData)-1]



# inheritance go inside parenthesis
class SeaofBTCapp(tk.Tk):

    # initialize method
    # *args = arguments (whatever variable you want to pass
    # *kwargs = keyword args (pass through dictionaries)
    def __init__(self, *args, **kwargs):
        # initialize tkinter
        tk.Tk.__init__(self, *args, **kwargs)

        # changes the program icon
        tk.Tk.iconbitmap(self, default="FoSe.ico")

        # change the window title
        tk.Tk.wm_title(self, "FoSe Jeenaa")

        # makes the window fullscreen
        tk.Tk.wm_state(self, "zoomed")

        # Frame is a window
        container = tk.Frame(self)

        # fill will fill in the space allotted to the pack
        # expand expands to fill the window
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, ForceGraph):

            frame = F(container, self)

            self.frames[F] = frame

            # sticky is the alignment + stretch
            frame.grid(row=0, column = 0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]

        print(cont)
        if cont == ForceGraph:
            graphReset()

        # raises it to the front
        frame.tkraise()



class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

         # loads intro image
        introImage = tk.PhotoImage(file="FoSeJeenaa_med.png")
        introLabel = ttk.Label(self, image=introImage)
        introLabel.image = introImage
        introLabel.pack()


        label = tk.Label(self,
        text=
    """   This physical therapy application is still in development. Use at your own risk. Always consult with
    your physical therapist before starting this or any other rehabilitation program to determine if it is
    right for your needs. If you experience faintness, dizziness, pain or shortness of breath at any time
    while using this device you should stop immediately.""",
        font=LARGE_FONT, justify='left'
                         )
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Agree",
                            command=lambda: controller.show_frame(ForceGraph))
        button1.pack()

        button2 = ttk.Button(self, text="Disagree", command=quit)
        button2.pack()

        button3 = ttk.Button(self, text="Page One", command=lambda: controller.show_frame(PageOne))
        button3.pack()



class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()




class ForceGraph(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        def pauseHelper():
            if button3["text"] == "Pause":
                pauseGraph()
                button3["text"] = "Resume"
            else:
                resumeGraph()
                button3["text"] = "Pause"

        def resetHelper():
            resumeGraph()
            button3["text"] = "Pause"
            graphReset()

        button1 = ttk.Button(self, text="Zero Force Sensor", command=calibrate)
        button1.pack()

        button2 = ttk.Button(self, text="Reset", command=resetHelper)
        button2.pack()

        button3 = ttk.Button(self, text="Pause", command=pauseHelper)
        button3.pack()

        button4 = ttk.Button(self, text="Help!", command=pauseHelper)
        button4.pack()

        # adds the plot to the window
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # adds the matplotlib toolbar to the window
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

xData = []
yData = []
startTime = time.time()
maxForce = time.time()
forceSensorOffset = 0.007
pause = False

force_text = axis1.text(0.5, 125, "0", fontsize=25)
max_text = axis1.text(0.5, 110, "0", fontsize=25)

displayDeviceInfo()
app = SeaofBTCapp()
#figure, animation function, how long between updates in ms
ani = animation.FuncAnimation(fig, animate, interval=24, init_func=init)
app.mainloop()
