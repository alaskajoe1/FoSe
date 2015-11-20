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


print("Opening phidget object....")

# Creates bridge object
bridge = Bridge()

# Opens phidget
bridge.openPhidget()

# waits 10000 ms (10s) for bridge to connect
bridge.waitForAttach(10000)

displayDeviceInfo()


# defines initial parameters
def init():
    ax.set_ylim(0, 125)
    ax.set_xlim(0, 10)
    del xdata[:]
    del ydata[:]
    line.set_data(xdata, ydata)

    time_text.set_text('')
    return line, time_text


# sets up plot
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
ax.grid()
xdata, ydata = [], []
startTime = time.time()

time_template = 'time = %.1fs'
time_text = plt.text(2, 120, "0",)


# update the data
def run(data):
    # calculates seconds since program started running
    t = time.time() - startTime
    # converts bridge voltage output to lbs
    y = (bridge.getBridgeValue(1) + 0.007) * 74.3  # lbs/mV

    # adds this data onto the xdata and y data
    xdata.append(t)
    ydata.append(y)

    # updates plot title with current force* in lbs
    plt.title("%.1f" % np.mean(ydata[(len(ydata) - 10):]))
    # "%.1f" %" -- formats following number as a float with 1 value after the decimal
    # np.mean() -- takes the mean
    # len(ydata) -- computes the length of ydata
    # ydata[(len(ydata)-10):] -- takes the last ten values of ydata (similar to MATLAB colon notation)
    # So really avergaing the last 10 values (0.24s) worth of data

    time_text.set_text("%.1f" % np.mean(ydata[(len(ydata) - 10):]))

    a, b = time_text.get_position()


    # calculates current bounds on the x-axis
    xmin, xmax = ax.get_xlim()

    # if the data is within 2 second of the end of the graph
    if t >= xmax - 2:
        ax.set_xlim(xmin + 0.05, xmax + 0.05)  # increment the x-axis
        time_text.set_position((a+0.05,b))
        ax.figure.canvas.draw()  # redraw the graph
    line.set_data(xdata, ydata)  # update x and y values

    return line


# animates the graph
ani = animation.FuncAnimation(fig, run, blit=False, interval=10,
                              repeat=False, init_func=init)
plt.show()
