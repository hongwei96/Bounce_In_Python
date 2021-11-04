import os
import pygame

class Texture2D:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.tex = pygame.image.load(os.path.join(path))
        self.imagerect = self.tex.get_rect()