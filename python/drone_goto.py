#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
© Copyright 2015-2016, 3D Robotics.
simple_goto.py: GUIDED mode "simple goto" example (Copter Only)
Demonstrates how to arm and takeoff in Copter and how to navigate to points using Vehicle.simple_goto.
Full documentation is provided at http://python.dronekit.io/examples/simple_goto.html
"""

# Park Home (middle of Field): 38.832804, -104.801181
# Park Waypoint 1 ( Left side): 38.832796, -104.802259
# Park Waypoint 2 (Right side): 38.832584, -104.798622
from __future__ import print_function
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative

'''
# Set up option parsing to get connection string
import argparse


parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
parser.add_argument('--connect',
                    help="Vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect
sitl = None


# Start SITL if no connection string specified
if not connection_string:
    print('No Connection Specified, Exiting...')
    exit()
   
    
print('Awaiting Target Coordinates...')
'''
def drone_goto(com,baudrate, latitude, longitude):

    # Connect to the Vehicle
    connection_string = str(com) + "," + str(baudrate)
    print('Connecting to vehicle on: %s' % connection_string)
    vehicle = connect(connection_string, wait_ready=True)

    #vehicle = connect(connection_string, wait_ready=False)
    #vehicle.wait_ready(True, raise_exception=False)


    def arm_and_takeoff(aTargetAltitude):
        """
        Arms vehicle and fly to aTargetAltitude.
        """

        print("Basic pre-arm checks")
        # Don't try to arm until autopilot is ready
        while not vehicle.is_armable:
            print(" Waiting for vehicle to initialise...")
            time.sleep(1)

        print("Arming motors")
        # Copter should arm in GUIDED mode
        vehicle.mode = VehicleMode("GUIDED")
        vehicle.armed = True

        # Confirm vehicle armed before attempting to take off
        while not vehicle.armed:
            print(" Waiting for arming...")
            time.sleep(1)

        print("Taking off!")
        vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

        # Wait until the vehicle reaches a safe height before processing the goto
        #  (otherwise the command after Vehicle.simple_takeoff will execute
        #   immediately).
        while True:
            print(" Altitude: ", vehicle.location.global_relative_frame.alt)
            # Break and return from function just below target altitude.
            if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
                print("Reached target altitude")
                break
            time.sleep(1)


    arm_and_takeoff(10)

    print("Set default/target airspeed to 3")
    vehicle.airspeed = 3

    print("Going towards first point for 30 seconds ...")
    point1 = LocationGlobalRelative(latitude, longitude, 20)
    vehicle.simple_goto(point1)

    # sleep so we can see the change in map
    time.sleep(30)
    
    '''
    print("Going towards second point for 30 seconds (groundspeed set to 10 m/s) ...")
    point2 = LocationGlobalRelative(38.832584, -104.7986221, 20)
    vehicle.simple_goto(point2, groundspeed=10)
    '''
    
    # sleep so we can see the change in map
    #time.sleep(30)

    print("Returning to Launch")
    vehicle.mode = VehicleMode("RTL")

    # Close vehicle object before exiting script
    print("Close vehicle object")
    vehicle.close()