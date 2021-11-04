from Engine.BaseState import BaseState
from Engine.Vector2 import Vector2

class State_Level1(BaseState):
    statename = "Level 1"

    def __init__(self, resourcemanager, window):
        super().__init__(resourcemanager, window, State_Level1.statename)
        self.position = Vector2()
        
    def Load(self):
        super().Load()

    def Update(self):
        super().Update()
        self.position.x += 1
        self.position.y += 1
        super().AddDrawCall("Ball", Vector2(0,0))
        super().AddDrawCall("Ball", Vector2(100,100))
        super().AddDrawCall("Ball", Vector2(200,200))
        super().AddDrawCall("Ball", Vector2(300,300))
        super().AddDrawCall("Ball", self.position)

        super().Draw()
