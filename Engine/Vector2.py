# Vector2D class
# Stores 2 values (Point/Vector/Coordinate)
import math

class Vector2:
    def __init__(self, x = 0.0, y = 0.0):
        self.x = x
        self.y = y
    
    # inheritable alternative constructors
    @classmethod
    def fromTuple(cls, tuple):
        return cls(tuple[0],tuple[1])

    def toTuple(self):
        return (self.x, self.y)

    def Normalize(self):
        len = self.Length()
        self.x = self.x / len
        self.y = self.y / len

    def Normalized(self):
        len = self.Length()
        return Vector2(self.x / len, self.y / len)

    def LengthSq(self):
        return self.x ** 2 + self.y ** 2
        
    def Length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def SetZero(self):
        self.x = 0.0
        self.y = 0.0

    @staticmethod
    def Zero():
        return Vector2(0, 0)
    def One():
        return Vector2(1, 1)

    # Magic method / Special method
    def __str__(self):
        return "({}, {})".format(self.x, self.y)
            
    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector2(x, y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Vector2(x, y)

    def __mul__(self, other: float):
        x = self.x * other
        y = self.y * other
        return Vector2(x, y)

    def __truediv__(self, other: float):
        x = self.x / other
        y = self.y / other
        return Vector2(x, y)

    def __eq__(self, other):
        if other != None:
            return (self.x == other.x and self.y == other.y)
        else:
            return False