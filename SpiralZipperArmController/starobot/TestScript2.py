#!/usr/bin/env python
'''
Set up and control a diff drive robot using a joystick

I recommend running this code in ipython via:
>> execfile('diffdrive.py')
'''

import ckbot.logical as L # CKBot interface
# Import pygame, which handles joysticks and other inputs
import pygame
from pygame import joystick
from pygame import event
from pygame.locals import *
from time import time as now, sleep

# Specify module ID and the name we want to give each of them:
modules = { 42: 'Left', 16: 'Right' } 

if __name__=="__main__":

    import sys

    print "Initializing DiffDrive Demo"  
    # Initialize pygame and a joystick
    pygame.init()
    joystick.init()
    joystick.Joystick(0).init()

    # Optionally specify left and right modules through the command line.
    if len(sys.argv) == 3:
        modules = { int(sys.argv[1]) : 'Left', int(sys.argv[2]) : 'Right' }

    # Create a CKBot cluster
    c = L.Cluster()
    c.populate( len(modules), modules )

    # Limit module speed and torque for safety
    for m in c.itermodules():
        m.set_torque_limit( 0.95 )
        # If module is a servo, then also limit speed
        if not m.get_mode():
            m.set_speed( 20 )

    print "DiffDrive demo initialized"
    drivable = False
    drive = 0.0
    turn = 0.0
    driveGain = 0.5
    turnGain = 0.4
    last_report = now()
    report_interval = 10
    while True:
        try:
            # A 5 cell lipo shouldn't be used below 16 V.
            # Check to make sure the voltage is still good.
            if now()-last_report > report_interval:
                batt_v = c.at.Left.get_voltage()
                last_report = now()
                if batt_v < 10: # EDIT: set below 16 if using wired power
                    print 'Battery voltage less than 16V, please charge battery. Shutting off robot.'
                    break
                else:
                    print 'Battery voltage: %2.2f V' % batt_v
            # Get and handle events
            for evt in event.get():
                if evt.type == JOYAXISMOTION:   
                    # Look at joystick events and control values
                    if evt.axis == 3:
                        turn = evt.value
                        print "Turn: %f" % turn
                    elif evt.axis == 1:
                        drive = evt.value
                        print "Drive: %f" % drive
                elif evt.type == JOYBUTTONDOWN:
	                  # Pressing controller's main buttons toggles drivability
                    if evt.button in range(6):
                        drivable = not drivable
                        print 'Drivability status: %s' % str(drivable)
                    # Pressing the trigger buttons ends demo.
                    else:
                        raise KeyboardInterrupt
            if drivable:
                # Set the torque values on the CR modules based on the 
                # inputs that we got from the joystick 
                c.at.Left.set_torque( -(drive*driveGain - turn*turnGain) )
                c.at.Right.set_torque(  drive*driveGain + turn*turnGain )
		Lencoder = c.at.Left.get_pos()
       	        Rencoder = c.at.Right.get_pos()
	        print "Lposition: %f" % Lencoder
	        #print "Rposition: %f" % Rencoder
        except KeyboardInterrupt:
            # Break out of the loop
            break

    print "Demo exiting, turning off all modules"
    # Turn the modules off before we exit for safety
    for m in c.itermodules():
        m.go_slack()
