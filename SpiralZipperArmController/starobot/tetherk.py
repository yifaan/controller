#!/usr/bin/env python
'''
Set up and control a spiral zipper arm using a joystick

I recommend running this code in ipython via:
>> execfile('tetherf.py')
'''

import ckbot.logical as L # CKBot interface
import math
from time import time as now, sleep
import time

if __name__=="__main__":

   import sys
   # Create a CKBot cluster
   c = L.Cluster()
   c.populate(1)
   print "DiffDrive demo initialized"
   last_report = now()
   report_interval = 1.0
   pr = 20.5
   pi = 3.14159
   rev = 4096.0
   while True:
    # get initial encoder value
    iLencoder = c.at.Nx10.get_pos()
    print "iLencoder: %f" % iLencoder
    theta = int(raw_input("Input theta:\n"))
    #phi = int(raw_input("Input phi:\n"))
    move = theta
    if move>0:
     run0 = move + iLencoder
     turn = run0 // rev
     print "Turn0: %f" % turn
     resi = run0 % rev
     print "Resi: %f" % resi
     while (turn > 0.0):
         print "Turn1: %f" % turn
         c.at.Nx10.set_torque(0.1)
         Lencoder = c.at.Nx10.get_pos()
	 print "position: %f" % Lencoder
         if (Lencoder >= 0.0)and(Lencoder <= 5.0):
	     turn = turn - 1.0
	     time.sleep(0.1)
	     continue
     else:
	 Lencoder = c.at.Nx10.get_pos()
	 while (Lencoder <= resi):
	   c.at.Nx10.set_torque(0.1)
	   Lencoder = c.at.Nx10.get_pos()
	   print "position: %f" % Lencoder
	   print "Turn2: %f" % turn
	 else:
	   while Lencoder > resi:
	    c.at.Nx10.set_torque(-0.005)
	    Lencoder = c.at.Nx10.get_pos()
	   else:
	    c.at.Nx10.set_torque(0.0)
            print "resi: %f" % resi
	    print "Done"
    else:
     run0 = move + iLencoder
     turn = run0 // rev
     print "Turn0: %f" % turn
     resi = run0 % rev
     print "Resi: %f" % resi
     while (turn < 0.0):
         print "Turn1: %f" % turn
         c.at.Nx10.set_torque(-0.1)
         Lencoder = c.at.Nx10.get_pos()
	 print "position: %f" % Lencoder
         if (Lencoder >= 4092.0)and(Lencoder <= 4095.0):
	     turn = turn + 1.0
	     time.sleep(0.1)
	     continue
     else:
 	 Lencoder = c.at.Nx10.get_pos()
	 while (Lencoder >= resi):
	   c.at.Nx10.set_torque(-0.1)
	   Lencoder = c.at.Nx10.get_pos()
	   print "position: %f" % Lencoder
	   print "Turn2: %f" % turn
	 else:
	   while Lencoder < resi:
	    c.at.Nx10.set_torque(0.005)
	    Lencoder = c.at.Nx10.get_pos()
	   else:
	    c.at.Nx10.set_torque(0.0)
            print "resi: %f" % resi
	    print "Done"
    print "Demo exiting, turning off all modules"
    # Turn the modules off before we exit for safety
    for m in c.itermodules():
        m.go_slack()
