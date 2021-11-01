from Engine.BaseState import BaseState

class State_Level1(BaseState):
    statename = "Level 1"

    def __init__(self, window):
        super().__init__(window, State_Level1.statename)
        pass
    def Load(self):
        super().Load()

    def Update(self):
        super().Update()
        super().Draw()
