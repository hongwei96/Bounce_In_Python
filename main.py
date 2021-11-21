import pygame
from Engine.StateManager import StateManager
from Engine.ResourceManager import ResourceManager
from Engine.Resources import Texture2D, Audio
from State_Level import State_Level
from State_MainMenu import State_MainMenu

# Global Constants
FPS = 60
WIN_DIMENSION = (960, 640) # Grid = 15 x 10, 64px

# Game Global
WIN = pygame.display.set_mode(WIN_DIMENSION)

# Setup window
pygame.display.set_caption("Bounce Classic")

# Global Var
rm = ResourceManager()
sm = StateManager(rm, WIN)

def InitializeResources():
    rm.AddTexture(Texture2D("Ball", "Assets\\Ball.png"))
    rm.AddTexture(Texture2D("Brick", "Assets\\Brick.png"))
    rm.AddTexture(Texture2D("Black", "Assets\\Black.png"))
    rm.GetTexture("Black").tex.set_alpha(128)
    rm.AddTexture(Texture2D("Checkpoint_Active", "Assets\\Checkpoint_Active.png"))
    rm.AddTexture(Texture2D("Checkpoint_NotActive", "Assets\\Checkpoint_NotActive.png"))
    rm.AddTexture(Texture2D("Startpoint", "Assets\\Startpoint.png"))
    rm.AddTexture(Texture2D("Endpoint", "Assets\\Endpoint.png"))
    rm.AddTexture(Texture2D("Ring", "Assets\\Ring.png"))
    rm.AddTexture(Texture2D("Slope", "Assets\\Slope.png"))
    rm.AddTexture(Texture2D("Spike", "Assets\\Spike.png"))
    rm.AddTexture(Texture2D("Title", "Assets\\Title.png"))

    rm.AddAudioClip(Audio("Selecting", "Assets\\SFX\\blipSelect.wav"))
    rm.GetAudioClip("Selecting").source.set_volume(0.4)
    rm.AddAudioClip(Audio("Checkpoint", "Assets\\SFX\\checkpoint.wav"))
    rm.GetAudioClip("Checkpoint").source.set_volume(0.4)
    rm.AddAudioClip(Audio("Hit", "Assets\\SFX\\hitHurt.wav"))
    rm.GetAudioClip("Hit").source.set_volume(0.5)
    rm.AddAudioClip(Audio("Jump", "Assets\\SFX\\jump.wav"))
    rm.GetAudioClip("Jump").source.set_volume(0.2)
    rm.AddAudioClip(Audio("PickupCoin", "Assets\\SFX\\pickupCoin.wav"))
    rm.GetAudioClip("PickupCoin").source.set_volume(0.4)
    rm.AddAudioClip(Audio("MainMenuBGM", "Assets\\SFX\\mainMenuBGM.wav"))
    rm.GetAudioClip("MainMenuBGM").source.set_volume(0.3)
    rm.AddAudioClip(Audio("inGameBGM", "Assets\\SFX\\inGameBGM.wav"))
    rm.GetAudioClip("inGameBGM").source.set_volume(1.0)

    rm.InitFont()
    #rm.PrettyPrint()

def InitializeStates():
    sm.AddState(State_Level)
    sm.AddState(State_MainMenu)
    sm.ChangeState(State_MainMenu.statename)

def GetDeltaTime(getTicksLastFrame = [0]):
    t = pygame.time.get_ticks()
    # deltaTime in seconds.
    deltaTime = (t - getTicksLastFrame[0]) / 1000.0
    getTicksLastFrame[0] = t
    return deltaTime
    #Debug.Log(deltaTime)

# Game Loop
def main():
    pygame.init()
    InitializeResources()
    InitializeStates()
    clock = pygame.time.Clock()
    run = True
    while run:
        if sm.IsStateChanged():
            sm.LoadNewState()

        clock.tick(FPS)

        # Events
        eventList = pygame.event.get()
        for event in eventList:
            if event.type == pygame.QUIT:
                run = False

        # State Update
        sm.UpdateState(eventList, GetDeltaTime())

        if sm.IsStateChanged():
            if sm.isQuit():
                run = False
            else:
                sm.UnloadCurrentState()

    sm.CleanUp()
    pygame.quit()

if __name__ == "__main__":
    main()