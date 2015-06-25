import ckbot.logical as L
from time import sleep, time
import sys
import thread


class controller():

    # this is used to control the sprial zipper arm in quasistatic manner

    def __init__(self):
        # change the number of modules according to the application
        # modules = {0xED: 'MOD1', 0xDE: 'MOD2'}
        modules = {0xDE: 'MOD1', 0xE7: 'MOD2', 0xAB: 'MOD3'}
        self.c = L.Cluster()
        self.c.populate(len(modules), modules)
        self.pos_1 = self.c.at.MOD1.get_pos()
        self.pos_2 = self.c.at.MOD2.get_pos()
	    self.pos_3 = self.c.at.MOD3.get_pos()
        # position of the three motor
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
        self.x3 = 0
        self.y3 = 0
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
        while ((abs(x - self.pos_1) > self.range) or (abs(y - self.pos_2) > self.range)):
            sys.stdout.write("%4d\t" % self.pos_1)
            sys.stdout.write("%4d\r" % self.pos_2)
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

                self.get_pos()
            except KeyboardInterrupt:
                self.shut_down()
                break

    # the inverse kinematics of the arm
    def pos2len(self, x, y, z):
        #(x1=,y1=,z1=), (x2=,y2=,z2=)(x3=,y3=,z3=) asda
        len1 = ((x - x1) ** 2 + (y - y1) ** 2 + (z - z1) ** 2) ** 0.5
        len2 = ((x - x2) ** 2 + (y - y2) ** 2 + (z - z2) ** 2) ** 0.5
        len1 = ((x - x1) ** 2 + (y - y1) ** 2 + (z - z1) ** 2) ** 0.5
        return (len1, len2, len3)

    # forward kinematics of the 
    def len2pos(self, l1, l2, l3):
        # mat1 * [x,y]' = mat2
        mat1 = [[2*(self.x3 - self.x1),2*(self.y3 - self.y1)],[2*(self.x2 - self.x1),2*(self.x3 - self.y1)]]
        det1 = mat1[0][0] * mat1[1][1] - mat1[0][1] * mat1[1][0]
        mat2 = [l1**2 - l3**2 - (self.x1**2 - self.x3**2) - (self.y1**2 - self.y3**2), l1**2 - l2**2 - (self.x1**2 - self.x2**2) - (self.y1**2 - self.y2**2)]
        inv_mat1 = [[mat1[1][1],-mat1[0][1]],[-mat1[1][0],mat1[0][0]]]
        x = (mat2[0] * inv_mat1[0][0] + mat2[1] * inv_mat1[0][1]) / det1
        y = (mat2[0] * inv_mat1[1][0] + mat2[1] * inv_mat1[1][1]) / det1
        z = (l1**2 - (x - self.x1)**2  - (y - self.y1)**2) ** 0.5
        return (x, y, z)

    # change endeffector speed to motor speed
    def end2motor():
        pass

    # generate a valid trajectory from current position to
    # the desired position
    # rpm = 80 * set_torque(value) - 1
    # deg/sec = 480 * set_torque(value) - 6
    # 120 mm per rotation, 120/360 = 1/3 mm/deg
    # mm/sec = 160 * set_torque(value) - 2
    def trajGenerator(self, t):
        x = 7000 + 300 * t + 1.0 / 2 * 80 * t * t
        speed = 300 + 80.0 * t
        torqueValue = (speed * 0.06 + 6) / 480

        # if torqueValue < 0.03:
        #     torqueValue = 0.03
        if x > 9000:
            return (9000, torqueValue, False)
        else:
            return (x, torqueValue, True)

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

    c1.move_to(7000, 7000, 0, 0.08)

    c1.stop()

    sleep(3)

    t0 = time()

    while 1:
        try:
            traj = c1.trajGenerator(time() - t0)

            sys.stdout.write("%.2f\t" % (time() - t0))
            sys.stdout.write("%5d\t" % traj[0])
            sys.stdout.write("%5d\n" % c1.pos_1)

            sys.stdout.flush()

            if (traj[2]):
                c1.moveMOD1(traj[1])
                c1.moveMOD2(traj[1])
                # sys.stdout.write("\t\t%5d\r" % traj[0])
            else:
                break

        except KeyboardInterrupt:
	    break

    c1.shut_down()
