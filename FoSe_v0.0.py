#Basic imports
import sys
import time
#Phidget specific imports
from Phidgets.PhidgetException import PhidgetException
from Phidgets.Devices.Bridge import Bridge, BridgeGain
from Phidgets.Phidget import PhidgetLogLevel
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


#Create a bridge object
try:
    bridge = Bridge()
except RuntimeError as e:	#error handling
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)


#Information Display Function
def displayDeviceInfo():
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (bridge.isAttached(), bridge.getDeviceName(), bridge.getSerialNum(), bridge.getDeviceVersion()))
    print("|------------|----------------------------------|--------------|------------|")
    print("Number of bridge inputs: %i" % (bridge.getInputCount()))
    print("Data Rate Max: %d" % (bridge.getDataRateMax()))
    print("Data Rate Min: %d" % (bridge.getDataRateMin()))
    print("Input Value Max: %d" % (bridge.getBridgeMax(0)))
    print("Input Value Min: %d" % (bridge.getBridgeMin(0)))

	#Event Handler Callback Functions
def BridgeAttached(e):
    attached = e.device
    print("Bridge %i Attached!" % (attached.getSerialNum()))

def BridgeDetached(e):
    detached = e.device
    print("Bridge %i Detached!" % (detached.getSerialNum()))

def BridgeError(e):
    try:
        source = e.device
        print("Bridge %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

def BridgeData(e):
    source = e.device
    print("Bridge %i: Input %i: %f" % (source.getSerialNum(), e.index, e.value))
	
try:
	#logging example, uncomment to generate a log file
    #bridge.enableLogging(PhidgetLogLevel.PHIDGET_LOG_VERBOSE, "phidgetlog.log")
	
    bridge.setOnAttachHandler(BridgeAttached)
    bridge.setOnDetachHandler(BridgeDetached)
    bridge.setOnErrorhandler(BridgeError)
    #bridge.setOnBridgeDataHandler(BridgeData)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)
	
print("Opening phidget object....")


bridge.openPhidget()
bridge.waitForAttach(10000)

displayDeviceInfo()


print("Set data rate to 8ms ...")
bridge.setDataRate(16)
time.sleep(.2)

print("Set Gain to 8...")
bridge.setGain(1, BridgeGain.PHIDGET_BRIDGE_GAIN_8)
time.sleep(.2)

print("Enable the Bridge input for reading data...")
bridge.setEnabled(1, True)
time.sleep(.2)




def init():
    ax.set_ylim(-0.1, 0.1)
    ax.set_xlim(0, 10)
    del xdata[:]
    del ydata[:]
    line.set_data(xdata, ydata)
    return line,

fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
ax.grid()
xdata, ydata = [], []

global startTime
startTime = time.time()
print(time.time() - startTime)
#time.sleep(0.1)

def run(data):
    # update the data
    t = time.time() - startTime
    y = bridge.getBridgeValue(1)
    xdata.append(t)
    ydata.append(y)	
	
    xmin, xmax = ax.get_xlim()

    if t >= xmax-2:
        ax.set_xlim(xmin+0.03, xmax+0.03)
        ax.figure.canvas.draw()
    line.set_data(xdata, ydata)

    return line,

ani = animation.FuncAnimation(fig, run, blit=False, interval=10,
                              repeat=False, init_func=init)
plt.show()


