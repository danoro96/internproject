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
from dronekit import connect, VehicleMode, LocationGlobalRelative, mavutil
import math
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
    if (com == '0'):
        connection_string = '127.0.0.1:14550'
    else:
        connection_string = str(com) + "," + str(baudrate)
        
    print('Connecting to vehicle on: %s' % connection_string)
    vehicle = connect(connection_string, wait_ready=True)

    #vehicle = connect(connection_string, wait_ready=False)
    #vehicle.wait_ready(True, raise_exception=False)
    def get_distance_metres(aLocation1, aLocation2):
        """
        Returns the ground distance in metres between two LocationGlobal objects.

        This method is an approximation, and will not be accurate over large distances and close to the 
        earth's poles. It comes from the ArduPilot test code: 
        https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
        """
        dlat = aLocation2.lat - aLocation1.lat
        dlong = aLocation2.lon - aLocation1.lon
        return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5

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


    def fly_waypoint(dest_point):
        print("Flying to waypoint..")
        
        vehicle.simple_goto(dest_point,groundspeed=10)
        current_loc = vehicle.location.global_relative_frame
        dist=get_distance_metres(current_loc, dest_point)
        while (dist > 1):
            time.sleep(0.25)
            current_loc = vehicle.location.global_relative_frame
            dist=get_distance_metres(current_loc, dest_point)
        print("Arrived at waypoint!") 
        
    
    
    arm_and_takeoff(5)

    print("Set default/target airspeed to 3")
    vehicle.airspeed = 3
    print("Set default RTL Altitude to same level")
    vehicle.parameters['RTL_ALT'] = 10

    print("Going towards first point for 30 seconds ...")
    point1 = LocationGlobalRelative(latitude, longitude, 5)
    fly_waypoint(point1)

    # sleep so we can see the change in map

    #print("Setting vehicle to loiter")
    #vehicle.mode = VehicleMode("LOITER")
    time.sleep(5)
    print("Dropping Payload...")
    
    msg = vehicle.message_factory.command_long_encode(
        0, 0,    # target_system, target_component
        mavutil.mavlink.MAV_CMD_DO_DIGICAM_CONTROL, #command
        1,          # confirmation
        0,          # param 1, yaw in degrees
        0,          # param 2, yaw speed deg/s
        0,          # param 3, direction -1 ccw, 1 cw
        0,          # param 4, relative offset 1, absolute angle 0
        1, 0, 0)    # param 5 ~ 7 not used
        
    vehicle.send_mavlink(msg)
    
    time.sleep(5)


    print("Returning to Launch")
    vehicle.mode = VehicleMode("RTL")
    
    while (vehicle.location.global_relative_frame.alt > 1):
        time.sleep(0.25)
    print("Landed.");

    # Close vehicle object before exiting script
    print("Close vehicle object")
    vehicle.close()