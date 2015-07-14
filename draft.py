import ckbot.logical as L
from time import sleep, time
import sys
import thread
from math import cos, sin

class controller():

    # this is used to control the sprial zipper arm in quasistatic manner

    def __init__(self):
        # change the number of modules according to the application
        # modules = {0xED: 'MOD1', 0xDE: 'MOD2'}
        modules = {0xE3: 'MOD1', 0xE6: 'MOD2', 0xDF: 'MOD3'}
        self.c = L.Cluster()
        self.c.populate(len(modules), modules)
        self.pos_1 = self.c.at.MOD1.get_pos()
        self.pos_2 = self.c.at.MOD2.get_pos()
        self.pos_3 = self.c.at.MOD3.get_pos()
        # position of the three motor
        self.x1 = 0
        self.y1 = 260
        self.z1 = 55
        self.x2 = -230
        self.y2 = -260
        self.z2 = 0
        self.x3 = 230
        self.y3 = -260
        self.z3 = 0
        self.range = 5  # about 0.6 degree
        print "initialize done"

    # set the postion of the module according to the encoder
    def get_pos(self):
        self.pos_1 = self.c.at.MOD1.get_pos()
        self.pos_2 = self.c.at.MOD2.get_pos()
        self.pos_3 = self.c.at.MOD3.get_pos()

    # move the motor according to the speed
    def moveMOD1(self, speed):
        self.get_pos()
        self.c.at.MOD1.set_torque(speed)

    # move the motor according to the speed
    def moveMOD2(self, speed):
        self.get_pos()
        self.c.at.MOD2.set_torque(speed)

    # move the motor according to the speed
    def moveMOD3(self, speed):
        self.get_pos()
        self.c.at.MOD3.set_torque(speed)

    # move motor to a certain position
    def move_to(self, x, y, z, speed):
        while ((abs(x - self.pos_1) > self.range) or (abs(y - self.pos_2) > self.range) or (abs(z - self.pos_3) > self.range)):
            sys.stdout.write("%4d\t" % self.pos_1)
            sys.stdout.write("%4d\t" % self.pos_2)
            sys.stdout.write("%4d\r" % self.pos_3)
            try:
                # module 1
                if ((x - self.pos_1) > self.range):
                    self.c.at.MOD1.set_torque(speed)
                elif ((self.pos_1 - x) > self.range):
                    self.c.at.MOD1.set_torque(-speed)
                else:
                    self.c.at.MOD1.set_torque(0)

                # module 2
                if ((y - self.pos_2) > self.range):
                    self.c.at.MOD2.set_torque(speed)
                elif ((self.pos_2 - y) > self.range):
                    self.c.at.MOD2.set_torque(-speed)
                else:
                    self.c.at.MOD2.set_torque(0)

                # module 3
                if ((z - self.pos_3) > self.range):
                    self.c.at.MOD3.set_torque(speed)
                elif ((self.pos_3 - z) > self.range):
                    self.c.at.MOD3.set_torque(-speed)
                else:
                    self.c.at.MOD3.set_torque(0)

                self.get_pos()
            except KeyboardInterrupt:
                self.shut_down()
                break

    # the inverse kinematics of the arm
    def pos2len(self, x, y, z):
        # (x1=,y1=,z1=), (x2=,y2=,z2=)(x3=,y3=,z3=)
        len1 = ((x - self.x1) ** 2 + (y - self.y1) ** 2 + (z - self.z1) ** 2) ** 0.5
        len2 = ((x - self.x2) ** 2 + (y - self.y2) ** 2 + (z - self.z2) ** 2) ** 0.5
        len3 = ((x - self.x3) ** 2 + (y - self.y3) ** 2 + (z - self.z3) ** 2) ** 0.5
        return (len1, len2, len3)

    # forward kinematics of the
    def len2pos(self, l1, l2, l3):
        # mat1 * [x,y]' = mat2
        mat1 = [[2*(self.x3 - self.x1),2*(self.y3 - self.y1)],[2*(self.x2 - self.x1),2*(self.x2 - self.y1)]]
        det1 = mat1[0][0] * mat1[1][1] - mat1[0][1] * mat1[1][0]
        mat2 = [l1**2 - l3**2 - (self.x1**2 - self.x3**2) - (self.y1**2 - self.y3**2), l1**2 - l2**2 - (self.x1**2 - self.x2**2) - (self.y1**2 - self.y2**2)]
        inv_mat1 = [[mat1[1][1],-mat1[0][1]],[-mat1[1][0],mat1[0][0]]]
        x = (mat2[0] * inv_mat1[0][0] + mat2[1] * inv_mat1[0][1]) / det1
        y = (mat2[0] * inv_mat1[1][0] + mat2[1] * inv_mat1[1][1]) / det1
        z = (l1**2 - (x - self.x1)**2 - (y - self.y1)**2) ** 0.5
        return (x, y, z)

    # change endeffector speed to motor command value
    def end2servo(self, x, y, z, Vx, Vy, Vz):
        # get the norm of the vector of each cable
        l1_norm = ((x - self.x1)**2 + (y - self.y1)**2 + (z - self.z1)**2)**0.5
        l2_norm = ((x - self.x2)**2 + (y - self.y2)**2 + (z - self.z2)**2)**0.5
        l3_norm = ((x - self.x3)**2 + (y - self.y3)**2 + (z - self.z3)**2)**0.5

        # get the unit vector on each cable's direction
        u1 = [(x - self.x1) / l1_norm, (y - self.y1) / l1_norm, (z - self.z1) / l1_norm]
        u2 = [(x - self.x2) / l2_norm, (y - self.y2) / l2_norm, (z - self.z2) / l2_norm]
        u3 = [(x - self.x3) / l3_norm, (y - self.y3) / l3_norm, (z - self.z3) / l3_norm]
        # calculate the speed of each cable, mm/s
        V1 = Vx * u1[0] + Vy * u1[1] + Vz * u1[2]
        V2 = Vx * u2[0] + Vy * u2[1] + Vz * u2[2]
        V3 = Vx * u3[0] + Vy * u3[1] + Vz * u3[2]
	
        # calculate the commanded torque value according to the cable speed
        # rpm = 80 * set_torque(value) - 1
        # deg/sec = 480 * set_torque(value) - 6
        # 120 mm per rotation, 120/360 = 1/3 mm/deg
        # mm/sec = 160 * set_torque(value) - 2
        if (V1 > 0):
            tval1 = (V1 + 2.0) / 160
        else:
            tval1 = (V1 - 2.0) / 160
        if (V2 > 0):
            tval2 = (V2 + 2.0) / 160
        else:
            tval2 = (V2 - 2.0) / 160
        if (V3 > 0):
            tval3 = (V3 + 2.0) / 160
        else:
            tval3 = (V3 - 2.0) / 160
        return (tval1, tval2, tval3)

    # move in xyz-direction
    def traj4(self, t):
        if (t < 5):
            x = 10 * t
            y = 10 * t
            z = 20 * t
            Vx = 10
            Vy = 10
            Vz = 20
        elif ((t < 10) and (t >= 5)):
            x = 50-10 * (t-5)
            y = 50-10 * (t-5)
            z = 100+20 * (t-5)
            Vx = -10
            Vy = -10
            Vz = 20
        elif ((t < 15) and (t >= 10)):
            x = -10 * (t-10)
            y = -10 * (t-10)
            z = 200-20 * (t-10)
            Vx = -10
            Vy = -10
            Vz = -20
        elif ((t < 20) and (t >= 15)):
            x = -50+10 * (t-15)
            y = -50+10 * (t-15)
            z = 100-20 * (t-15)
            Vx = 10
            Vy = 10
            Vz = -20
        else:
            x = 0
            Vx = 0
            y = 0
            Vy = 0
            z = 0
            Vz = 0
        return (x, y, z, Vx, Vy, Vz)
    
    def traj5(self,t):
        
        w = 4.0/180 * 3.14
        if (t < 10):
            x = 0
            y = 260 * sin(w * t)
            z = 260 * cos(w * t)
            Vx = 0
            Vy = 260 * w * cos(w * t)
            Vz = -260 * w * sin(w * t)
	elif (t<20):
 	    x = 0
	    y = 260 * sin(w * (20 - t))
            z = 260 * cos(w * (20 - t))
            Vx = 0
	    Vy = -260 * w * cos(w * (20-t))
            Vz = 260 * w * sin(w * (20-t))

        else:
            x = 0
            Vx = 0
            y = 0
            Vy = 0
            z = 280
            Vz = 0
        return (x,y,z,Vx,Vy,Vz)

    
    def traj6(self,t):
        
        w = 4.0/180 * 3.14
        if (t < 10):
            y = 0
            x = 260 * sin(w * t)
            z = 260 * cos(w * t)
            Vy = 0
            Vx = 260 * w * cos(w * t)
            Vz = -260 * w * sin(w * t)
	elif (t<20):
	    y = 0
	    x = 260 * sin(w * (20 - t))
            z = 260 * cos(w * (20 - t))
            Vy = 0
	    Vx = -260 * w * cos(w * (20-t))
            Vz = 260 * w * sin(w * (20-t))
        else:
            y = 0
            Vy = 0
            x = 0
            Vx = 0
            z = 280
            Vz = 0
        return (x,y,z,Vx,Vy,Vz)

    # stop motor and go_slack on each module
    def shut_down(self):
        print "shut down"
        for m in self.c.itermodules():
            m.set_torque(0)
            m.go_slack()

    def stop(self):
        for m in self.c.itermodules():
            m.set_torque(0)

if __name__ == "__main__":
    c1 = controller()
    length = c1.pos2len(0, 0, 280)
    print length[0], length[1], length[2]
    #c1.move_to(2500, 2500, 2500, 0.08)
    # c1.move_to(10000, 10000, 10000, 0.08)
    # c1.move_to(3000, 3000, 3000, 0.08)

    # c1.stop()

    # sleep(3)

    t0 = time()

    while 1:
        try:
            traj = c1.traj6(time() - t0)
            
            servo_speed = c1.end2servo(traj[0], traj[1], traj[2], traj[3], traj[4], traj[5])
            sys.stdout.write("%.3f\t" % servo_speed[0])
	    sys.stdout.write("%.3f\t" % servo_speed[1])
	    sys.stdout.write("%.3f\r" % servo_speed[2])
            # sys.stdout.write("%.3f\r" % servo_speed[0])
            # sys.stdout.write("%5d\n" % c1.pos_1)
            sys.stdout.flush()
	    # print servo_speed[2]
            c1.moveMOD1(servo_speed[0])
            c1.moveMOD2(servo_speed[1])
            c1.moveMOD3(servo_speed[2])

        except KeyboardInterrupt:
            break

    t0 = time()
    while 1:
	
        try:
            traj = c1.traj5(time() - t0)
            
            servo_speed = c1.end2servo(traj[0], traj[1], traj[2], traj[3], traj[4], traj[5])
            sys.stdout.write("%.3f\t" % servo_speed[0])
	    sys.stdout.write("%.3f\t" % servo_speed[1])
	    sys.stdout.write("%.3f\r" % servo_speed[2])
            # sys.stdout.write("%.3f\r" % servo_speed[0])
            # sys.stdout.write("%5d\n" % c1.pos_1)
            sys.stdout.flush()
	    # print servo_speed[2]
            c1.moveMOD1(servo_speed[0])
            c1.moveMOD2(servo_speed[1])
            c1.moveMOD3(servo_speed[2])

        except KeyboardInterrupt:
            break

    #c1.move_to(2500, 2500, 2500, 0.08)
    c1.shut_down()
