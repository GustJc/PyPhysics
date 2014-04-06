from mymath import vector2

class body2d():
  def __init__(self, px, py):
    self.mass = 1.0
    self.torque = 0.0
    self.force = vector2(0.0,0.0)
    self.speed = vector2(0.0,0.0)
    self.aceleration = vector2(0.0,0.0)
    self.position = vector2(float(px),float(py))
    #Rotational
    self.angular_speed = 0.0
    self.angular_aceleration = 0.0
    self.rotation_angle = 0.0
    self.moment_inertia = 1.0