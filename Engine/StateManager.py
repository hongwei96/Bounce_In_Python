from Engine.DebugLog import Debug

class StateManager:
    def __init__(self, resourcemanager, window):
        self.window = window
        self.resourcemanager = resourcemanager
        self.newState = "None"
        self.currentState = "None"
        self.states = {}
        self.variables = {}

    def isQuit(self):
        return self.newState == "None"

    # state: type
    def AddState(self, state):
        if state.statename in self.states:
            Debug.Warn(f'State \"{state.statename}\" already exist')
        else:
            self.states[state.statename] = state(self, self.resourcemanager, self.window)

    def RemoveState(self, state):
        if state.statename in self.states:
            self.states.pop(state.statename, None)
        else:
            Debug.Warn(f'State \"{state.statename}\" does not exist')

    def IsStateChanged(self):
        return self.currentState != self.newState
    
    def LoadNewState(self):
        if self.newState == "None":
            Debug.Warn("State not specified before InitializeState()")
        else:
            self.states[self.newState].Load()
            self.currentState = self.newState

    def UpdateState(self, eventlist, dt):
        state = self.states.get(self.currentState)
        if state:
            state.eventlist = eventlist
            state.Update(dt)
        else:
            Debug.Warn(f'{self.currentState} does not exist')

    def UnloadCurrentState(self):
        if self.currentState == "None":
            Debug.Warn("State not specified before InitializeState()")
        else:
            self.states[self.currentState].Unload()
            if not self.IsStateChanged():
                self.currentState = "None"
                self.newState = "None"
    
    def ChangeState(self, newstate):
        if newstate == "None" or newstate in self.states:
            if newstate != self.currentState:
                self.newState = newstate
                Debug.Log(f'Changing State... {self.currentState} -> {self.newState}')
            else:
                Debug.Warn(f'ChangeState() is the same')
        else:
            Debug.Warn(f'State \"{newstate}\" does not exist')

    def CleanUp(self):
        self.UnloadCurrentState()