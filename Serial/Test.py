import serial
import time

ser = serial.Serial('com3',115200,timeout=1)


while True:
    time.sleep(0.5)
    ser.flushInput()
    time.sleep(0.001)
    try:
        fValue = float(ser.readline())
        print(fValue)
    except:
        print("error")



