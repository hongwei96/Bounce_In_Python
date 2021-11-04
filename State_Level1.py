from Engine.BaseState import BaseState

class State_Level1(BaseState):
    statename = "Level 1"

    def __init__(self, resourcemanager, window):
        super().__init__(resourcemanager, window, State_Level1.statename)
        
    def Load(self):
        super().Load()

    def Update(self):
        super().Update()

        super().AddDrawCall("Ball")

        super().Draw()
