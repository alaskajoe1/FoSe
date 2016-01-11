# Basic imports
import sys
import time
import math
from tkinter import *
# Phidget specific imports
from Phidgets.PhidgetException import PhidgetException
from Phidgets.Devices.Bridge import Bridge, BridgeGain
from Phidgets.Phidget import PhidgetLogLevel
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# ToDO
# GUI
# Calibrate?

class ForceGraph:

    def __init__(self):

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

        # defines initial parameters
        def init():
            ax.set_ylim(0, 150)
            ax.set_xlim(0, 10)
            del xdata[:]
            del ydata[:]
            line.set_data(xdata, ydata)

            force_text.set_text('')
            return line, force_text

        # update the data
        def run(maxForce):
            # calculates seconds since program started running
            t = time.time() - startTime
            # converts bridge voltage output to lbs
            y = (bridge.getBridgeValue(1) + 0.007) * 74.3  # lbs/mV

            # adds this data onto the xdata and y data
            xdata.append(t)
            ydata.append(y)

            if len(ydata) > 30:
                ydata[len(ydata)-1] = (np.mean(ydata[(len(ydata) - 5):]))

            # updates plot title with current force* in lbs
            plt.title("%.1f" % np.mean(ydata[(len(ydata) - 10):]))
            # "%.1f" %" -- formats following number as a float with 1 value after the decimal
            # np.mean() -- takes the mean
            # len(ydata) -- computes the length of ydata
            # ydata[(len(ydata)-10):] -- takes the last ten values of ydata (similar to MATLAB colon notation)
            # So really avergaing the last 10 values (0.24s) worth of data


            currentForce = np.mean(ydata[(len(ydata) - 10):])
            force_text.set_text("Current Force: %.1f" % currentForce + " lbs")
            force_text.set_size(30)

            if currentForce > maxForce:
                maxForce = currentForce

            max_text.set_text("Max Force: %.1f" % np.max(ydata) + " lbs")
            max_text.set_size(30)

            a, b = force_text.get_position()
            c, d = max_text.get_position()

            # calculates current bounds on the x-axis
            xmin, xmax = ax.get_xlim()

            # if the data is within 2 second of the end of the graph
            if t >= xmax - 2:
                ax.set_xlim(t-8, t+2)  # increment the x-axis
                force_text.set_position((t-7.5, b))
                max_text.set_position((t-7.5, d))
                ax.figure.canvas.draw()  # redraw the graph
            line.set_data(xdata, ydata)  # update x and y values

            return line

        print("Opening phidget object....")

        # Creates bridge object
        bridge = Bridge()

        # Opens phidget
        bridge.openPhidget()

        # waits 10000 ms (10s) for bridge to connect
        bridge.waitForAttach(10000)

        displayDeviceInfo()

        # sets up plot
        fig, ax = plt.subplots()
        line, = ax.plot([], [], lw=2)
        ax.grid()
        xdata, ydata = [], []
        startTime = time.time()

        time_template = 'time = %.1fs'
        force_text = plt.text(0.5, 125, "0")
        max_text = plt.text(0.5, 110, "0")

        # animates the graph
        ani = animation.FuncAnimation(fig, run, blit=False, interval=10, repeat=False, init_func=init)
        plt.show()


# runs the force trial
def starttest():
    print("Running Trial")
    Fgraph = ForceGraph()


# calibrates the device
def calibrate():
    print("Now Calibrating...")


# displays help information
def helpme():
    print("Help!")
    help_root = Toplevel()
    help_root.wm_title("Help!")

    help_image = PhotoImage(file="file.png")
    helplabel = Label(help_root, image=help_image)
    helplabel.pack()

    quitbutton = Button(help_root, text="Done", command=help_root.destroy)
    quitbutton.pack()

    help_root.mainloop()


root = Tk()

root.wm_title("FoSe Jeenaa")


# loads intro image
introImage = PhotoImage(file="FoSeJeenaa_med.png")
introLabel = Label(root, image=introImage)
introLabel.pack()

# adds next buttton
nextButton = Button(root, text="Continue", command=root.destroy)
nextButton.pack()

# mainloop
root.mainloop()

root2 = Tk()
root2.wm_title("FoSe Jeenaa")

runButton = Button(root2, text="Start Test", font=("Times New Roman", 36), bg="blue", fg="yellow", command=starttest)
runButton.pack()

calibButton = Button(root2, text="Calibrate", font=("Times New Roman", 36), bg="blue", fg="yellow", command=calibrate)
calibButton.pack()

helpButton = Button(root2, text="Help!", font=("Times New Roman", 36), bg="blue", fg="yellow", command=helpme)
helpButton.pack()


root2.mainloop()
