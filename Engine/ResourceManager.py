import pygame
from Engine.DebugLog import Debug
from Engine.Resources import Audio, Texture2D

class ResourceFont:
    def __init__(self):
        self.fontName = None
        self.font : pygame.font.Font = None

class ResourceManager:
    def __init__(self):
        self.textureList = {}
        self.audioClipList = {}
        self.myFont = ResourceFont()
        pass
    
    def AddAudioClip(self, audio):
        self.audioClipList[audio.name] = audio

    def GetAudioClip(self, name) -> Audio:
        return self.audioClipList.get(name)

    def AddTexture(self, tex):
        self.textureList[tex.name] = tex

    def GetTexture(self, name) -> Texture2D:
        return self.textureList.get(name)
    
    def RemoveTexture(self, name):
        self.textureList.pop(name)
    
    def InitFont(self, font = None, size = 24):
        self.myFont.fontName = font
        self.myFont.font = pygame.font.SysFont(font, size)
    
    def RenderFont(self, text, color = (255,255,255), size = 24) -> pygame.Surface:
        if self.myFont.font == None:
            Debug.Error("Forget to call InitFont()")
        if size != self.myFont.font.size:
            self.InitFont(self.myFont.fontName, size)
        return self.myFont.font.render(text, True, color)

    def PrettyPrint(self):
        string = f'Loaded Textures ({len(self.textureList)}):\n'
        for texName in self.textureList:
            string += f'- {texName}\n'
        string += f'\n Loaded Font ({self.myFont.fontName})\n'
        Debug.Log(string)
