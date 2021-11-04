import pygame
from Engine.DebugLog import Debug
from Engine.StateManager import StateManager
from Engine.ResourceManager import ResourceManager
from Engine.Resources import Texture2D
from State_Level1 import State_Level1

# Global Constants
FPS = 60
WIN_DIMENSION = (1280,720)

# Game Global
WIN = pygame.display.set_mode(WIN_DIMENSION)

# Setup window
pygame.display.set_caption("Bounce Classic")

# Global Var
rm = ResourceManager()
sm = StateManager(rm, WIN, WIN_DIMENSION)

def InitializeResources():
    rm.AddTexture(Texture2D("Ball", "Assets\\Ball.png"))
    rm.AddTexture(Texture2D("Brick", "Assets\\Brick.png"))
    rm.AddTexture(Texture2D("Checkpoint_Active", "Assets\\Checkpoint_Active.png"))
    rm.AddTexture(Texture2D("Checkpoint_NotActive", "Assets\\Checkpoint_NotActive.png"))
    rm.AddTexture(Texture2D("Startpoint", "Assets\\Startpoint.png"))
    rm.AddTexture(Texture2D("Endpoint", "Assets\\Endpoint.png"))
    rm.AddTexture(Texture2D("Ring", "Assets\\Ring.png"))
    rm.AddTexture(Texture2D("Slope", "Assets\\Slope.png"))
    rm.AddTexture(Texture2D("Spike", "Assets\\Spike.png"))
    rm.PrettyPrint()

def InitializeStates():
    sm.AddState(State_Level1)
    sm.ChangeState(State_Level1.statename)

def LogFPS(getTicksLastFrame = [0]):
    t = pygame.time.get_ticks()
    # deltaTime in seconds.
    deltaTime = (t - getTicksLastFrame[0]) / 1000.0
    getTicksLastFrame[0] = t
    Debug.Log(deltaTime)

# Game Loop
def main():
    InitializeResources()
    InitializeStates()
    pygame.init()
    clock = pygame.time.Clock()
    run = True
    while run:
        if sm.IsStateChanged():
            sm.LoadNewState()

        clock.tick(FPS)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # State Update
        sm.UpdateState()

        if sm.IsStateChanged():
            sm.UnloadCurrentState()
    
    sm.CleanUp()
    pygame.quit()

if __name__ == "__main__":
    main()