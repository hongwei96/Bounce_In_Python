from Engine.DebugLog import Debug
from Engine.Vector2 import Vector2

class CollisionData:
    def __init__(self):
        self.hit = False
        self.contactPoint = [Vector2()]
# Utilities functions
# +-----> x
# |
# v
# y
def PointAABB(pt, topleft, bottomright):
    #data = CollisionData()
    if (pt.x <= topleft.x or pt.y <= topleft.y or 
        pt.x >= bottomright.x or pt.y >= bottomright.y):
        return False
        #data.hit = False
    #else:
        #data.hit = True
    #return data
    return True
    
def PointCircle(pt, center, radius):
    return (pt - center).LengthSq() <= radius * radius

def AABBAABB(topleft1, bottomright1, topleft2, bottomright2):
    if (topleft1.x > bottomright2.x or topleft2.x > bottomright1.x or 
        topleft1.y > bottomright2.y or topleft2.y > bottomright1.y):
        return False
    return True

def CircleCircle(c1, r1, c2, r2):
    return (c2 - c1).LengthSq() <= (r1 + r2) * (r1 + r2)

def CircleAABB(center, radius, topleft, bottomright):
    topright = Vector2(bottomright.x, topleft.y)
    bottomleft = Vector2(topleft.x, bottomright.y)
    # Expanded Square
    etopleft = topleft - Vector2(radius, radius)
    ebottomright = bottomright + Vector2(radius, radius)
    #etopright = topright + Vector2(radius, -radius)
    #ebottomleft = bottomleft + Vector2(-radius, radius)
    
    if not PointAABB(center, etopleft, ebottomright):
        return False
    # Left side
    if center.x <= topleft.x:
        # Left Top
        if center.y <= topleft.y:
            return PointCircle(center, topleft, radius)
        # Left Bottom
        elif center.y >= bottomright.y:
            return PointCircle(center, bottomleft, radius)
        # Left
        else:
            return True
    # Right side
    elif center.x >= bottomright.x:
        # Right Top
        if center.y <= topleft.y:
            return PointCircle(center, topright, radius)
        # Right Bottom
        elif center.y >= bottomright.y:
            return PointCircle(center, bottomright, radius)
        # Right
        else:
            return True
    else:
        return True

    return False