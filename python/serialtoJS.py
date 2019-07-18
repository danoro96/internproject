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

import os

import subprocess

import time

import numpy

import histo

class obj:

    points = []
    angles   = []

tojs = obj()


# open serial port
ser = serial.Serial("/dev/ttyACM0", 9600)



# this changes stuff from binary to ASCII
# currently takes in a file but we can chage it so that it takes in something else

# !!! here we can try to implement  a different web socket that we can grab the data from Thuy's program !!!

# data = scipy.fromfile(open(file), dtype=scipy.complex64)



# define function that will be used later inside of the websocket function
def serialConn(): 
    
    # read data from serial bus
    rawData = ser.readline()

    # strip formatting characters
    cleanData = rawData.decode().strip('\r\n')
    cleanData = cleanData.lstrip("0")

    return cleanData


# initialize web socket and send data
async def hello(websocket, path):

    print('I am connected..........')

    while True:

        ans = await websocket.recv()

        print('received')
        
        if ans == 0:
            # if we receive a 0 from the web socket we take data

            #Run Gnuradio
            # s = subprocess.Popen(["python2", "music.py"], stdout = subprocess.PIPE)
            # time.sleep(10)
            # s.kill()

            #histogram
            avg = histo.doitboi()

            separatedData = serialConn()

            separatedData = separatedData.split(",")

            tojs.points.push([separatedData[0], separatedData[1]])

            # add the compensation with respect to north
            northangle = separatedData[9]

            realangle = northangle + avg

            if realangle > 360:
                realangle  = realangle - 360

            tojs.angles.push(realangle)


        elif ans == 1:
            # If we receive a 2 then we send data and plot 
            #Here we find the intersecting point
            finalPt = histo.intersect(tojs.points, tojs.angles)

            # putting the found point at the end so we know where it is
            finalPts = tojs.points.append(finalPt)
        

            finalPts.encode()
            await websocket.send(finalPts)

        elif ans == 2:
            # if we receive a 3 then we send the drone

            a = 5

            return a


start_server = websockets.serve(hello, 'localhost', 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

