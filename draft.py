import ckbot.logical as L
from time import sleep, time
import sys
import thread


class controller():

    # this is used to control the sprial zipper arm in quasistatic manner

    def __init__(self):
        # change the number of modules according to the application
        # modules = {0xED: 'MOD1', 0xDE: 'MOD2'}
        modules = {0xDE: 'MOD1', 0xE7: 'MOD2'}
        self.c = L.Cluster()
        self.c.populate(len(modules), modules)
        self.pos_1 = self.c.at.MOD1.get_pos()
        self.pos_2 = self.c.at.MOD2.get_pos()
        self.range = 5  # about 0.6 degree
        print "initialize done"

    # set the postion of the module according to the encoder
    def get_pos(self):
        self.pos_1 = self.c.at.MOD1.get_pos()
        self.pos_2 = self.c.at.MOD2.get_pos()
        # sys.stdout.write("Cheleb:%5d\r" % self.pos_1)
        # sys.stdout.write("Canopus:%5d\r" % self.pos_2)
        # sys.stdout.flush()

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
                print "JAJAJA"
                break

    # generate a valid trajectory from current position to
    # the desired position
    # rpm = 80 * set_torque(value) - 1
    # deg/sec = 480 * set_torque(value) - 6
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

    c1.shut_down()
