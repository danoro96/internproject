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

import drone_goto

import os

import subprocess

import time

import numpy

import histo

# open serial port
#ser = serial.Serial("/dev/ttyUSB0", 9600)



# this changes stuff from binary to ASCII
# currently takes in a file but we can chage it so that it takes in something else

# !!! here we can try to implement  a different web socket that we can grab the data fromfrom Thuy's program !!!

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

        
        drone = await websocket.recv()
        if (len(drone) > 1):
            print('Calling script...')
            drone.split(",")
            print(drone)
            #drone_goto.drone_goto('COM13',57600,38.832804, -104.801181)
            drone_goto.drone_goto(drone[0],int(drone[1]),float(drone[2]), float(drone[3]))
            
            
        else:
            print('received')
            
        separatedData = "38.832804, -104.801181, 1,1,2020,0,0,0"
        separatedData.encode()
        await websocket.send(separatedData)
        
        #==============================Donnie's Code
        
        #separatedData = serialConn()
        '''
        await websocket.recv()

        print('received')
        #Run Gnuradio
        # s = subprocess.Popen(["python2", "music.py"], stdout = subprocess.PIPE)
        # time.sleep(10)
        # s.kill()

        #histogram
        avg = histo.doitboi()
        #print(avg)
        #separatedData = serialConn()
        separatedData = separatedData + (str(avg))
        separatedData.encode()
   
        separatedData = "38.832804, -104.801181, 1,1,2020,0,0,0"
        separatedData.encode()
        await websocket.send(separatedData)

        print(separatedData)
        print('The message has been sent..........')
        '''

print("Starting server...")
start_server = websockets.serve(hello, 'localhost', 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

#Here we would like to receive the data again and send the data to the drone to run automatically'''
# 1. receive the data
# 2. process the data
# 3. tell the drone what to do
# 4. get some type of confirmation???
