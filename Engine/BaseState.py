from Engine.DebugLog import Debug
import pygame

class BaseState:
    def __init__(self, rm, win, name):
        self.rm = rm # Resource Manager 
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

    def AddDrawCall(self, texName, position = 0, rotation = 0, scale = 0):
        self.renderList.append(texName)

    def Draw(self):
        # Background
        self.window.fill(self.backgroundColor)
        # Draw all Object
        for texName in self.renderList:
            texture = self.rm.GetTexture(texName)
            if texture != None:
                self.window.blit(texture.tex, texture.imagerect)
            else:
                Debug.Error(f'{texName} is not loaded...')
        # Refresh
        pygame.display.update()
        
    def LogInfo(self):
        Debug.Log(f'Level name : {self.name}')