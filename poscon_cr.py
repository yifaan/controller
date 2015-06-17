#!/usr/bin/env python
import ckbot.logical as L
from time import sleep

c = L.Cluster()
c.populate(1)

if __name__ == "__main__":

    try:
        init_pos = c.at.NxDE.get_pos()
        print "initial position =", init_pos
        waypoint_1 = init_pos + 1500
        waypoint_2 = init_pos + 3000
        if waypoint_1 > 65535:
            waypoint_1 = waypoint_1 - 65535
        if waypoint_2 > 65535:
            waypoint_2 = waypoint_2 - 65535
        print "waypoint #1 =", waypoint_1
        print "waypoint #2 =", waypoint_2

        c.at.NxDE.set_torque(0.05)

        while True:
            cur_pos = c.at.NxDE.get_pos()
            # print "current position =", cur_pos
            if cur_pos > waypoint_1:
                c.at.NxDE.set_torque(0.1)
                print "waypoint 1 reached =", c.at.NxDE.get_pos()
                break

        print "current position =", c.at.NxDE.get_pos()

        while True:
            cur_pos = c.at.NxDE.get_pos()
            # print "current position =", cur_pos
            if cur_pos > waypoint_2:
                c.at.NxDE.set_torque(0.0)
                print "waypoint 2 reached =", c.at.NxDE.get_pos()
                break

        print "current position =", c.at.NxDE.get_pos()
        c.at.NxDE.go_slack()

    except KeyboardInterrupt:
        for m in c.itermodules():
            m.go_slack()
