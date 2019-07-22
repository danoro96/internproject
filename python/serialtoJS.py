'''
Serial to Javascipt ~ by Daniel Castillo

This function takes data from the serial port and sends it to JS
thorugh a web socket set up inside the machine.
It could be modified to send to a different machine as well.
'''
# set up and import allnecessary module
import serial

import asyncio

import websockets

import time, threading

import numpy as np

import scipy

#import drone_goto

import os

import subprocess

import time

import numpy

import histo

class obj:
    def __init__(self):
        self.points = []
        self.angles = []


#open serial port
ser = serial.Serial()
ser.baudrate = 9600
ser.port = "/dev/ttyACM1"

# this changes stuff from binary to ASCII
# currently takes in a file but we can chage it so that it takes in something else

# !!! here we can try to implement  a different web socket that we can grab the data fromfrom Thuy's program !!!

# data = scipy.fromfile(open(file), dtype=scipy.complex64)



# define function that will be used later inside of the websocket function
def serialConn(): 
    if  not ser.is_open:
        ser.open()
    # read data from serial bus
    print("serialConn() called")
    rawData = ser.readline()
    print('Getting GPS Lock....') 
    # strip formatting characters
    cleanData = rawData.decode().strip('\r\n')
    cleanData = cleanData.lstrip("0")
    separatedData = cleanData.split(",")
    
    while(len(separatedData) < 11):
        # read data from serial bus
        print("Separated data < 11: ", separatedData)
        rawData = ser.readline()
        print('Getting GPS Lock....')
        # strip formatting characters
        cleanData = rawData.decode().strip('\n')
        cleanData = cleanData.lstrip("0")
        separatedData = cleanData.split(",")

    print("Separated Data: ", separatedData)
    print('GPS Locked')
    return separatedData


# initialize web socket and send data

async def hello(websocket, path):
    tojs = None
    tojs = obj()
    print('I am connected..........')

    while True:
        print("Running ...")

        ans = await websocket.recv()

        print('received ', ans)
        
        if ans == '0':
            # if we receive a 0 from the web socket we take data

            #Run Gnuradio
            s = subprocess.Popen(["python2", "music.py"])
            time.sleep(10)
            s.kill()

            #histogram
            avg = histo.doitboi()

            print("calling serialConn()")

            separatedData = None

            separatedData = serialConn()

            print(separatedData)
            
            tojs.points.append(float(separatedData[0]))
            tojs.points.append(float(separatedData[1]))
            print('first index=',separatedData[0], 'second index=',separatedData[1])

            # add the compensation with respect to north
            print(separatedData)
            northangle = float(separatedData[9])

            realangle = northangle + avg

            if realangle > 360.0:
                realangle  = realangle - 360.0

            tojs.angles.append(realangle)
            print('calc angle=', realangle)
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            ser.close()



        elif ans == '1':
            # If we receive a 2 then we send data and plot 
            #Here we find the intersecting point
            print('locations=',tojs.points)
            print('angles=', tojs.angles)
            finalPt = histo.intersect(tojs.points, tojs.angles)
            print('intersect=',finalPt)

            # putting the found point at the end so we know where it is
            tojs.points.append(finalPt[0])
            tojs.points.append(finalPt[1])

            finalPts = str(tojs.points)
            print(finalPts)

            await websocket.send(finalPts)

        elif ans == '2':
            # if we receive a 3 then we send the drone
            
            print('Calling script...')
            drone.split(",")
            print(drone)
            #drone_goto.drone_goto('COM13',57600,38.832804, -104.801181)
            drone_goto.drone_goto('COM13',57600,tojs.points[-2],tojs.points[-1], float(drone[3]))


start_server = websockets.serve(hello, 'localhost', 8050)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()