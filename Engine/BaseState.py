from Engine.DebugLog import Debug
from Engine.Vector2 import Vector2
import pygame

class Entity:
    def __init__(self, texName, position, rotation, scale):
        self.name = texName
        self.position = position
        self.rotation = rotation
        self.scale = scale


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

    def AddDrawCall(self, texName, position = Vector2(), rotation = 0, scale = Vector2()):
        self.renderList.append(Entity(texName, position, rotation, scale))

    def Draw(self):
        # Background
        self.window.fill(self.backgroundColor)
        # Draw all Object
        for entity in self.renderList:
            texture = self.rm.GetTexture(entity.name)
            if texture != None:
                self.window.blit(texture.tex, (entity.position.x, entity.position.y))
            else:
                Debug.Error(f'{entity.name} is not loaded...')
        # Refresh
        pygame.display.update()
        self.renderList.clear()
        
    def LogInfo(self):
        Debug.Log(f'Level name : {self.name}')