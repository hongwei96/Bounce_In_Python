from pygame import rect
from Engine.DebugLog import Debug
from Engine.ResourceManager import ResourceManager
from Engine.StateManager import StateManager
from Engine.Utilities import MYCOLOR
from Engine.Vector2 import Vector2
import pygame

class Entity:
    def __init__(self):
        self.type = "" # "Sprite", "Font"
        self.name = ""
        self.color = MYCOLOR.WHITE
        self.position = Vector2.Zero()
        self.rotation : int = 0
        self.scale = Vector2.One()
        self.size = 0

    @classmethod
    def SetAsSprite(cls, texName, pos : Vector2, rot : int, scale : Vector2):
        obj = cls()
        obj.type = "Sprite"
        obj.name = texName
        obj.position = pos
        obj.rotation = rot
        obj.scale = scale
        return obj

    @classmethod
    def SetAsFont(cls, text : str, pos : Vector2, col, size : int):
        obj = cls()
        obj.type = "Font"
        obj.name = text
        obj.position = pos
        obj.color = col
        obj.size = size
        return obj


class BaseState:
    def __init__(self, sm : StateManager, rm : ResourceManager, win : pygame.Surface, name : str):
        self.rm = rm # Resource Manager 
        self.sm = sm # State Manager
        self.backgroundColor = (255,255,255)
        self.renderList = []
        self.UIrenderList = []
        self.debuglines = []
        self.debugrects = []
        self.debugcircles = []
        self.window = win
        self.name = name
        self.eventlist =[]

    def Load(self):
        Debug.Log(f'Loading... {self.name}')
        
    def Unload(self):
        Debug.Log(f'Unloading... {self.name}')

    def Update(self, dt):
        pass

    def AddDrawSprite(self, texName : str, position : Vector2 = Vector2(), rotation : float = 0, scale : Vector2 = Vector2.One()):
        self.renderList.append(Entity.SetAsSprite(texName, position, rotation, scale))

    def AddDrawFont(self, text : str, pos : Vector2 = Vector2(), col : tuple = (255,255,255), size : int = 24):
        self.renderList.append(Entity.SetAsFont(text, pos, col, size))

    def AddDrawUISprite(self, texName : str, position : Vector2 = Vector2(), rotation : float = 0, scale : Vector2 = Vector2.One()):
        self.UIrenderList.append(Entity.SetAsSprite(texName, position, rotation, scale))

    def AddDrawUIFont(self, text : str, pos : Vector2 = Vector2(), col : tuple = (255,255,255), size : int = 24):
        self.UIrenderList.append(Entity.SetAsFont(text, pos, col, size))

    def AddDrawDebugLineCall(self, start, end, color):
        self.debuglines.append((start, end, color))

    def AddDrawDebugRectCall(self, topleft, dim, color):
        self.debugrects.append((topleft, dim, color))

    def AddDrawDebugCircleCall(self, point, radius, color):
        self.debugcircles.append((point, radius, color))

    def AddDrawDebugPointCall(self, point, color):
        self.debugcircles.append((point, 2, color))

    def Draw(self):
        # Background
        self.window.fill(self.backgroundColor)
        # Draw all Sprite & Font
        for entity in self.renderList:
            if entity.type == "Sprite":
                texture = self.rm.GetTexture(entity.name)
                if texture != None:
                    self.window.blit(pygame.transform.scale(texture.tex, texture.GetNewSizeAfterScale(entity.scale).toTuple()),
                                    entity.position.toTuple())
                else:
                    Debug.Error(f'{entity.name} is not loaded...')
            elif entity.type == "Font":
                img = self.rm.RenderFont(entity.name, entity.color, entity.size)
                self.window.blit(img, entity.position.toTuple())

        # Draw UI Sprite & Font
        for entity in self.UIrenderList:
            if entity.type == "Sprite":
                texture = self.rm.GetTexture(entity.name)
                if texture != None:
                    self.window.blit(pygame.transform.scale(texture.tex, texture.GetNewSizeAfterScale(entity.scale).toTuple()),
                                    entity.position.toTuple())
                else:
                    Debug.Error(f'{entity.name} is not loaded...')
            elif entity.type == "Font":
                img = self.rm.RenderFont(entity.name, entity.color, entity.size)
                self.window.blit(img, entity.position.toTuple())

        # Draw all debug
        LINE_WIDTH = 2
        for line in self.debuglines:
            pygame.draw.line(self.window, line[2], line[0].toTuple(), line[1].toTuple(), LINE_WIDTH)
        for sq in self.debugrects:
            pygame.draw.rect(self.window, sq[2], pygame.Rect(sq[0].x,sq[0].y,sq[1].x,sq[1].y), LINE_WIDTH)
        for cir in self.debugcircles:
            pygame.draw.circle(self.window, cir[2], cir[0].toTuple(), cir[1], LINE_WIDTH)
            
        # Refresh
        pygame.display.update()
        self.renderList.clear()
        self.UIrenderList.clear()
        self.debuglines.clear()
        self.debugrects.clear()
        self.debugcircles.clear()
        
    def LogInfo(self):
        Debug.Log(f'Level name : {self.name}')