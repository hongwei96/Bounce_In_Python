from Engine.DebugLog import Debug
import pygame

class BaseState:
    def __init__(self, win, name):
        self.backgroundColor = (255,255,255)
        self.renderList = []
        self.window = win
        self.name = name

    def Load(self):
        Debug.Log(f'Loading... {self.name}')
        
    def Unload(self):
        Debug.Log(f'Unloading... {self.name}')

    def Update(self):
        pass

    def Draw(self):
        # Background
        self.window.fill(self.backgroundColor)
        # Draw all Object
        #print(f'drawing...')
        # Refresh
        pygame.display.update()
        
    def LogInfo(self):
        Debug.Log(f'Level name : {self.name}')