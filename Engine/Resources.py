import os
import pygame
from Engine.Vector2 import Vector2

class Texture2D:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.tex = pygame.image.load(os.path.join(path)).convert_alpha()
        self.rect = Vector2(self.tex.get_rect()[2], self.tex.get_rect()[3])
    
    def GetNewSizeAfterScale(self, scale : Vector2):
        return Vector2(self.rect.x * scale.x, self.rect.y * scale.y)

class Audio:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.source : pygame.mixer.Sound = pygame.mixer.Sound(path)
    
    def Play(self):
        self.source.play()