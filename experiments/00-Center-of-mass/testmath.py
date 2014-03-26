import sys
sys.path.append("../../modules")
from mymath import *
b = vector2(2,3)
c = vector2(1,0)
a = b.dot(c)

vec3 = vector3(1,2,3)
vec3b = vector3(1,1,1)

print vec3

vec3C = vec3.cross(vec3b)
print vec3C
print a
print 'a: ', a
print 'b: ', b.x, ', ', b.y
print b
print c

print 'mod(c): ', c.mod()
print 'mod(b): ', b.mod()

print  'unit(b): ', b.get_unit()

print  'projection(b em c): ', b.projection(c)
print  'projection vector(b em c): ', b.projection_vector(c)