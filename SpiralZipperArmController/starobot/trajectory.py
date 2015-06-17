#!/usr/bin/env python
'''
Set up and control a spiral zipper arm using a joystick

I recommend running this code in ipython via:
>> execfile('tethern.py')
'''
import ckbot.logical as L # CKBot interface
import math
import serial
import solution
from time import time as now, sleep
import time
def go(moveL, moveR):
    runL = moveL + iLencoder
    turnL = runL // rev
    resiL = runL % rev
    signL = math.copysign(1.0,turnL)
    tqL1 = signL*0.1
    tqL2 = -signL*0.05
    turnL = abs(turnL)
    runR = moveR + iRencoder
    turnR = runR // rev
    resiR = runR % rev
    signR = math.copysign(1.0,turnR)
    tqR1 = signR*0.1
    tqR2 = -signR*0.05
    turnR = abs(turnR)
    print "moveL: %f" % moveL
    print "moveR: %f" % moveR
    while (turnL > 0.0)or(turnR > 0.0):
	Lencoder = c.at.Left.get_pos()
        Rencoder = c.at.Right.get_pos()
	if (turnL > 0.0):
         #print "TurnL: %f" % turnL
         c.at.Left.set_torque(tqL1)
	elif (turnL <= 0.0):
	 c.at.Left.set_torque(0.0)
	 #print "TurnL: %f" % turnL
        if (Lencoder >= 0.0)and(Lencoder <= 5.0):
	 turnL = turnL - 1.0
	 time.sleep(0.1)
	if (turnR > 0.0):
         #print "TurnR: %f" % turnR
         c.at.Right.set_torque(tqR1)
	elif (turnR <= 0.0):
	 c.at.Right.set_torque(0.0)
        if (Rencoder >= 0.0)and(Rencoder <= 5.0):
	 turnR = turnR - 1.0
	 time.sleep(0.1)
    else:
	 Lencoder = c.at.Left.get_pos()
	 Rencoder = c.at.Right.get_pos()
	 while (signL*Lencoder <= signL*resiL)or(signR*Rencoder <= signR*resiR):
	  Lencoder = c.at.Left.get_pos()
	  Rencoder = c.at.Right.get_pos()
	  if (signL*Lencoder <= signL*resiL):
	   c.at.Left.set_torque(tqL1)
	  elif (signL*Lencoder > signL*resiL):
	   c.at.Left.set_torque(0.0)
	  if (signR*Rencoder <= signR*resiR):
	   c.at.Right.set_torque(tqR1)
	  elif (signR*Rencoder > signR*resiR):
	   c.at.Right.set_torque(0.0)
	 else:
	   while (signL*Lencoder > signL*resiL)or(signR*Rencoder > signR*resiR):
	    Lencoder = c.at.Left.get_pos()
	    Rencoder = c.at.Right.get_pos()
	    if (signL*Lencoder > signL*resiL):
	     c.at.Left.set_torque(tqL2)
	    elif (signL*Lencoder <= signL*resiL):
	     c.at.Left.set_torque(0.0)
	    if (signR*Rencoder > signR*resiR):
	     c.at.Right.set_torque(tqR2)
	    elif (signR*Rencoder <= signR*resiR):
	     c.at.Right.set_torque(0.0)
	   else:
	    c.at.Left.set_torque(0.0)
	    c.at.Right.set_torque(0.0)
	    print "Lposition: %f" % Lencoder
	    print "Rposition: %f" % Rencoder
	    print "Done"
    return;
if __name__=="__main__":
   ser = serial.Serial('/dev/ttyACM0')
   # Specify module ID and the name we want to give it:
   modules = { 17: 'Left', 07: 'Right'} 
   import sys
   # Create a CKBot cluster
   c = L.Cluster()
   # Now populate the cluster with our dictionary of module IDs and names 
   c.populate( len(modules), modules )
   last_report = now()
   report_interval = 1.0
   pr = 22.5
   pi = 6.283
   rev = 4096.0
   l1 = 768.0
   l2 = 768.0
   rad = 571.5
   div = 3.0
   a =0
   b =0
   c =0
   theta_list = [140, 90, 30]
   phi_list = [90, 90, 90]
   servo_list =['1','9','2']
   yes = 0
   while True:
     iLencoder = c.at.Left.get_pos()
     iRencoder = c.at.Right.get_pos()
     if a > (len(theta_list)-1):
        a = 0
        b = 0
        c = 0
        yes = int(raw_input("Once more?:\n"))
     while True:
      theta = theta_list[a]
      a = a+1
      phi = phi_list[b]
      b = b+1
      if (165>= theta >=25)and(165>= phi >=25):
        break
      else:
        print "Input angle out of range\n"
        continue
     theta = theta/180.0*3.1416
     print "theta: %f" % theta
     phi = phi/180.0*3.1416
     print "phi: %f" % phi
     #time.sleep(2)
     lengths = solution.getSolution(theta,phi,rad)
     l11 = lengths['l1']
     l21 = lengths['l2']
     l31 = lengths['l3']
     print "l1: %f" % l1
     print "l2: %f" % l2
     #time.sleep(2)
     t1 = l11 - l1
     t2 = l21 - l2
     #time.sleep(2)
     moveR = -t1/(pi*pr)*rev
     moveL = t2/(pi*pr)*rev
     l1 = l11
     l2 = l21
     go(moveL,moveR)
     print "t1: %f" % t1
     print "t2: %f" % t2
     ser.write(servo_list[c])
     c = c +1
    # Turn the modules off before we exit for safety
     for m in c.itermodules():
        m.go_slack()
