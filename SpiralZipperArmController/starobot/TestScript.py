"""
This repesents a cluster of modules that can be controlled with the WASD keys.
The modules move synchronously. [W] speeds up motion; [S] slows down motion.
[A] and [D] control motion of a UBar module.
"""

import ckbot.logical as L
from pygame import *

class DriveModule () :
  """
  A class that represents a cluster of modules that can be driven.
  """
  def __init__(self, c):
    """
    INPUTS:
      c -- Cluster -- the populated cluster of modules that is controlled.
    """
    self.speed = 500
    self.modspeed = 5
    self.direction = 0
    self.c = c

    init()

    screen = display.set_mode((150, 50))
    display.set_caption('Basic Pygame program')

    for m in self.c.itermodules():
      m.set_speed(self.modspeed)
      m.set_torque_limit(.25)
      m.set_pos(-3000)
      print(m)

  def handle(self, evt):
    """
    Responds to a pygame event. Direction controls undergo positive
    interference, where holding down both left and right keys result in
    no motion.
    INPUTS:
      evt -- pygame.event
    """
    # Uncomment this line if you want to see each event as it is called.
    # print(evt)
    # [Q], [ESC], and closing the window shuts the loop.
    if evt.type == KEYDOWN:
      if evt.key in [K_q, K_ESCAPE]:
        return False
      # [A] and [D] changes the direction of the module
      elif evt.key == K_a: # A
        self.direction -= 1
      elif evt.key == K_d:
        self.direction += 1
      # [W] and [S] control speed.
      elif evt.key == K_w:
        if self.modspeed < 20:
          self.modspeed += 1
      elif evt.key == K_s:
        if self.modspeed >= 3:
          self.modspeed -= 1
    # Releasing a key stops that motion.
    elif evt.type == KEYUP:
      if evt.key == K_a:
        self.direction += 1
      elif evt.key == K_d:
        self.direction -= 1
    return True

  def move(self, d, mod):
    """
    Moves a given module in the given direction at the class's module speed.
    """
    mod.set_speed(self.modspeed)
    pos = mod.get_pos()
    mod.set_pos(pos + d * self.speed)

  def main(self):
    """
    Controls the main action loop of the script.
    """
    loop = True
    while 1:
      for evt in event.get():
        loop = self.handle(evt)
      for m in self.c.itermodules():
        self.move(self.direction, m)
      if not loop:
        break
    
    # Take care to shut down the modules properly.
    self.shut_down()

  def shut_down(self):
    """
    Lower speed, and go_slack on each module.
    """
    for m in self.c.itermodules():
      m.set_speed(5)
      m.go_slack()

if __name__ == '__main__':
  import sys
  c = L.Cluster()
  # If an argument is given, populate that number of modules.
  if len(sys.argv) == 2:
    c.populate(int(sys.argv[1]))
  # Otherwise, use the default value. #EDIT to change default num of robots.
  else:
    c.populate(1)
  DriveModule(c).main()
