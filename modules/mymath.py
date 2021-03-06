import math

class vector2():
  def __init__(self, x,y):
    self.x = x
    self.y = y

  def __add__(self, vec):
    r = vector2(self.x, self.y)
    if isinstance(vec, self.__class__):
      r.x += vec.x
      r.y += vec.y
    else:
      r.x += vec
      r.y += vec
    return r

  def __sub__(self, vec):
    r = vector2(self.x, self.y)
    if isinstance(vec, self.__class__):
      r.x -= vec.x
      r.y -= vec.y
    else:
      r.x -= vec
      r.y -= vec
    return r

  def __mul__(self, vec):
    if isinstance(vec, self.__class__):
      return vector2(self.x*vec.x, self.y*vec.y)
    else:
      return vector2(self.x*vec, self.y*vec)

  def __div__(self, vec):
    if isinstance(vec, self.__class__):
      return vector2(self.x/vec.x, self.y/vec.y)
    else:
      return vector2(self.x/vec, self.y/vec)

  def __iadd__(self, vec):
    if isinstance(vec, self.__class__):
      self.x += vec.x
      self.y += vec.y
    else:
      self.x += vec
      self.y += vec
    return self

  def __idiv__(self, number):
    self.x /= number
    self.y /= number
    return self

  def __str__(self):
    return "vector2(x: {0}, y: {1})".format(self.x, self.y)

  # In 2d cross is not well defined, returns scalar
  def cross(self, vec):
    if isinstance(vec, self.__class__):
      return self.x*vec.y - self.y*vec.y
    else:
      raise("Object is not a vector2")
  
  def dot(self, vec):
    if isinstance(vec, self.__class__):
      return vec.x * self.x + vec.y * self.y
    else:
      raise("Object is not a vector2")

  def mod(self):
    return math.sqrt( self.x**2 + self.y**2 )

  def get_unit(self):
    return self / self.mod()

  def projection(self, vec):
    return (self.dot(vec) / vec.mod())

  def projection_vector(self, vec):
    return vec.get_unit() * self.projection(vec)



# vector3 - 3d Vector 

class vector3():
  def __init__(self, x,y,z):
    self.x = x
    self.y = y
    self.z = z

  def __add__(self, vec):
    r = vector2(self.x, self.y)
    if isinstance(vec, self.__class__):
      r.x += vec.x
      r.y += vec.y
      r.z += vec.z
    else:
      r.x += vec
      r.y += vec
      r.z += vec
    return r

  def __sub__(self, vec):
    r = vector3(self.x, self.y, self.z)
    if isinstance(vec, self.__class__):
      r.x -= vec.x
      r.y -= vec.y
      r.z -= vec.z
    else:
      r.x -= vec
      r.y -= vec
      r.z -= vec
    return r

  def __mul__(self, vec):
    if isinstance(vec, self.__class__):
      return vector3(self.x*vec.x, self.y*vec.y, self.y*vec.z)
    else:
      return vector3(self.x*vec, self.y*vec, self.y*vec)

  def __div__(self, vec):
    if isinstance(vec, self.__class__):
      return vector3(self.x/vec.x, self.y/vec.y, self.z/vec.y)
    else:
      return vector3(self.x/vec, self.y/vec, self.z/vec)

  def __idiv__(self, number):
    self.x /= number
    self.y /= number
    self.z /= number
    return self

  def __str__(self):
    return "vector3(x: {0}, y: {1}, z: {2})".format(self.x, self.y, self.z)

  # x is self.x and X is vec.x
  # | i j k | = (self.y*vec.z - self.z*vec.y) i
  # | x y z | + (self.x*vec.z - self.z*vec.x) j
  # | X Y Z | + (self.x*vec.y - self.y*vec.x) k
  def cross(self, vec):
    if isinstance(vec, self.__class__):

      return vector3(
        self.y*vec.z - self.z*vec.y, 
        self.x*vec.z - self.z*vec.x, 
        self.x*vec.y - self.y*vec.x)
    else:
      raise("Object is not a vector2")
  def dot(self, vec):
    if isinstance(vec, self.__class__):
      return vec.x * self.x + vec.y * self.y
    else:
      raise("Object is not a vector2")

  def mod(self):
    return math.sqrt( self.x**2 + self.y**2 + self.z**2 )

  def get_unit(self):
    return self / self.mod()

#--------------- Classe Matrix
class Matrix():
  def __init__(self, valores):
    self.M = valores;

  def __add__(self, value):
    N = self.M
    for i in range(3):
      for j in range(3):
        N[i][j] += value

    return N

  def __iadd__(self, value):
    for i in range(3):
      for j in range(3):
        self.M[i][j] += value

    return self

  def __sub__(self, value):
    N = self.M
    for i in range(3):
      for j in range(3):
        N[i][j] -= value

    return N

  def __isub__(self, value):
    for i in range(3):
      for j in range(3):
        self.M[i][j] += value

    return self


