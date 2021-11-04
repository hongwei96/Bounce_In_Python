from pygame.constants import K_DOWN, K_LEFT, K_RIGHT, K_UP
from Engine.BaseState import BaseState
from Engine.DebugLog import Debug
from Engine.Vector2 import Vector2
import pygame

class State_Level(BaseState):
    statename = "Level 1"

    def __init__(self, resourcemanager, window):
        super().__init__(resourcemanager, window, State_Level.statename)
        self.backgroundColor = (137, 207, 240)

        self.cameraPos = Vector2()
        Debug.Log(self.cameraPos)
        self.isOnGround = False
        self.playerPos = Vector2()
        self.playerFallingSpeed = 0.0
        self.map = []
    
    def __drawMap(self):
        for i in range (15):
            super().AddDrawCall("Brick", Vector2(i * 64, 0))
        for i in range (10):
            super().AddDrawCall("Brick", Vector2(0, i * 64))
        for i in range (15):
            super().AddDrawCall("Brick", Vector2(i * 64, 640-64))
        for i in range (10):
            super().AddDrawCall("Brick", Vector2(960-64, i * 64))

    def __handleCollision(self):
        pass

    def __handleGravity(self, dt: float):
        if not self.isOnGround:
            self.playerFallingSpeed += 9.8 * dt
            # Terminal velocity
            if self.playerFallingSpeed > 33.0:
                self.playerFallingSpeed = 33.0
            self.playerPos.y += self.playerFallingSpeed * 100.0 * dt # assume 100px = 1metre
        else:
            self.playerFallingSpeed = 0.0

    def __handleKeyInput(self):
        keypress = pygame.key.get_pressed()
        if keypress[K_UP]:
            self.playerPos.y -= 1
        elif keypress[K_DOWN]:
            self.playerPos.y += 1
        if keypress[K_LEFT]:
            self.playerPos.x -= 1
        elif keypress[K_RIGHT]:
            self.playerPos.x += 1

    def Load(self):
        super().Load()

    def Update(self, dt):
        self.__handleKeyInput()
        self.__handleCollision()
        self.__handleGravity(dt)

        self.__drawMap()
        super().AddDrawCall("Ball", self.playerPos)

        super().Update(dt)
        super().Draw()
