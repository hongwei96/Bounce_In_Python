class Line2:
    def __init__(self, list):
        self.points = list
    
    @classmethod
    def from2Points(cls, start, end):
        return cls([start, end])

    @property
    def start(self):
        return self.points[0]
    
    @property
    def end(self):
        return self.points[-1]