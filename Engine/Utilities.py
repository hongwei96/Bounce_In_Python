from Engine.Vector2 import Vector2

# Utilities functions
# +-----> x
# |
# v
# y
def PointAABB(pt, topleft, bottomright):
    if (pt.x < topleft.x or pt.y < topleft.y or 
        pt.x > bottomright.x or pt.y > bottomright.y):
        return False
    return True

def AABBAABB(topleft1, bottomright1, topleft2, bottomright2):
    if (topleft1.x > bottomright2.x or topleft2.x > bottomright1.x or 
        topleft1.y > bottomright2.y or topleft2.y > bottomright1.y):
        return False
    return True

def CircleCircle(c1, r1, c2, r2):
    return (c2 - c1).LengthSq() < (r1 + r2) * (r1 + r2)

def CircleAABB(center, radius, topleft, bottomright):
    topright = Vector2(bottomright.x, topleft.y)
    bottomleft = Vector2(topleft.x, bottomright.y)
    return False