import pygame
from Engine.StateManager import StateManager
from State_Level1 import State_Level1

# Global Constants
FPS = 60
WIN_DIMENSION = (1280,720)

# Game Global
WIN = pygame.display.set_mode(WIN_DIMENSION)

# Setup window
pygame.display.set_caption("Bounce Classic")

# Global Var
sm = StateManager(WIN, WIN_DIMENSION)

def InitializeStates():
    sm.AddState(State_Level1)
    sm.ChangeState(State_Level1.statename)

# Game Loop
def main():

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