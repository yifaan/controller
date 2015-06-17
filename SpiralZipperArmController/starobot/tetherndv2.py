#!/usr/bin/env python
'''
Set up and control a spiral zipper arm using a joystick

I recommend running this code in ipython via:
>> execfile('tethern.py')
'''
import ckbot.logical as L # CKBot interface
import math
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
    Lencoder = c.at.Left.get_pos()
    Rencoder = c.at.Right.get_pos()
    while (turnL > 0.0) or(turnR > 0.0) or (abs(Lencoder)-abs(resiL))>=5.0 or (abs(Rencoder)-abs(resiR))>=5.0:
	Lencoder = c.at.Left.get_pos()
        Rencoder = c.at.Right.get_pos()
	if (turnL > 0.0):
         c.at.Left.set_torque(tqL1)
        if (Lencoder >= 0.0)and(Lencoder <= 5.0):
	 turnL = turnL - 1.0
	 time.sleep(0.1)
	if (turnR > 0.0):
         c.at.Right.set_torque(tqR1)
        if (Rencoder >= 0.0)and(Rencoder <= 5.0):
	 turnR = turnR - 1.0
	 time.sleep(0.1)
	if (turnL <= 0.0)and(signL*Lencoder <= signL*resiL):
	 c.at.Left.set_torque(tqL1)
	if (turnR <= 0.0)and(signR*Rencoder <= signR*resiR):
	 c.at.Right.set_torque(tqR1)
	if (turnL <= 0.0)and(signL*Lencoder > signL*resiL):
	 c.at.Left.set_torque(tqL2)
	elif (turnL <= 0.0)and(signL*Lencoder <= signL*resiL):
	 c.at.Left.set_torque(0.0)
	if (turnR <= 0.0)and(signR*Rencoder > signR*resiR):
	 c.at.Right.set_torque(tqR2)
	elif (turnR <= 0.0)and(signR*Rencoder <= signR*resiR):
	 c.at.Right.set_torque(0.0)
	Lencoder = c.at.Left.get_pos()
        Rencoder = c.at.Right.get_pos()
    else:
	c.at.Left.set_torque(0.0)
	c.at.Right.set_torque(0.0)
	print "Lposition: %f" % Lencoder
	print "Rposition: %f" % Rencoder
	print "Done"
    return;
if __name__=="__main__":
   # Specify module ID and the name we want to give it:
   modules = { 17: 'Left', 07: 'Right'} 
   import sys
   # Create a CKBot cluster
   c = L.Cluster()
   # Now populate the cluster with our dictionary of module IDs and names 
   c.populate( len(modules), modules )
   last_report = now()
   report_interval = 1.0
   pr = 23.0
   pi = 6.283
   rev = 4096.0
   l1 = 724.0
   l2 = 724.0
   rad = 546.1
   div = 3.0
   while True:
     iLencoder = c.at.Left.get_pos()
     iRencoder = c.at.Right.get_pos()
     moveR = int(raw_input("moveR:\n"))
     moveL = int(raw_input("moveL:\n"))
     go(moveL,moveR)
     print "t1: %f" % t1
     print "t2: %f" % t2
    # Turn the modules off before we exit for safety
     for m in c.itermodules():
        m.go_slack()
