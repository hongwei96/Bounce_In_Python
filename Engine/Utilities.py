from Engine.Vector2 import Vector2

# Utilities functions
# Colors
class MYCOLOR:
    BLACK  = (0, 0, 0)
    WHITE  = (255, 255, 255)
    RED    = (255, 0, 0)
    BLUE   = (0, 0, 255)
    GREEN  = (0, 255, 0)
    YELLOW = (255, 255, 0)
    CYAN   = (0, 255, 255)

# Collision
# +-----> x
# |
# v
# y

class CollisionData:
    def __init__(self):
        self.hit = False
        self.contactPoint = Vector2()

def PointAABB(pt, topleft, bottomright):
    #data = CollisionData()
    if (pt.x <= topleft.x or pt.y <= topleft.y or 
        pt.x >= bottomright.x or pt.y >= bottomright.y):
        return False
    return True
    
def __PointCircle(pt, center, radius):
    return (pt - center).LengthSq() <= radius * radius

def __AABBAABB(topleft1, bottomright1, topleft2, bottomright2):
    if (topleft1.x > bottomright2.x or topleft2.x > bottomright1.x or 
        topleft1.y > bottomright2.y or topleft2.y > bottomright1.y):
        return False
    return True

def __CircleCircle(c1, r1, c2, r2):
    return (c2 - c1).LengthSq() <= (r1 + r2) * (r1 + r2)

def CircleAABB(center, radius, topleft, bottomright):
    cData = CollisionData()
    topright = Vector2(bottomright.x, topleft.y)
    bottomleft = Vector2(topleft.x, bottomright.y)
    # Expanded Square
    etopleft = topleft - Vector2(radius, radius)
    ebottomright = bottomright + Vector2(radius, radius)
    #etopright = topright + Vector2(radius, -radius)
    #ebottomleft = bottomleft + Vector2(-radius, radius)
    
    if not PointAABB(center, etopleft, ebottomright):
        cData.hit = False
    else:
        # Left side
        if center.x <= topleft.x:
            # Left Top
            if center.y <= topleft.y:
                cData.hit = __PointCircle(center, topleft, radius)
                cData.contactPoint = topleft
            # Left Bottom
            elif center.y >= bottomright.y:
                cData.hit = __PointCircle(center, bottomleft, radius)
                cData.contactPoint = bottomleft
            # Left
            else:
                cData.hit = True
                cData.contactPoint = Vector2(topleft.x, center.y)
        # Right side
        elif center.x >= bottomright.x:
            # Right Top
            if center.y <= topleft.y:
                cData.hit = __PointCircle(center, topright, radius)
                cData.contactPoint = topright
            # Right Bottom
            elif center.y >= bottomright.y:
                cData.hit = __PointCircle(center, bottomright, radius)
                cData.contactPoint = bottomright
            # Right
            else:
                cData.hit = True
                cData.contactPoint = Vector2(bottomright.x, center.y)
        # Top side
        elif center.y <= topleft.y:
            cData.hit = True
            cData.contactPoint = Vector2(center.x, topleft.y)
        # Bottom side
        elif center.y >= bottomright.y:
            cData.hit = True
            cData.contactPoint = Vector2(center.x, bottomright.y)
        # Inside
        else:
            cData.hit = True
            # Find closest point to aabb boundary
            points = [topleft, topright, bottomright, bottomleft]
            distance = [(topleft-center).LengthSq(), (topright-center).LengthSq(),
                        (bottomright-center).LengthSq(), (bottomleft-center).LengthSq()]
            index_min = min(range(len(distance)), key=distance.__getitem__)
            direction_vector = points[index_min] - center
            # Check if it's closer to horizontal or vertical
            if abs(direction_vector.x) < abs(direction_vector.y):
                cData.contactPoint.x = points[index_min].x
                cData.contactPoint.y = center.y
            else:
                cData.contactPoint.x = center.x
                cData.contactPoint.y = points[index_min].y

    return cData