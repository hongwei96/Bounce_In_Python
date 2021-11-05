from pygame.constants import K_DOWN, K_LEFT, K_RIGHT, K_UP
from Engine.BaseState import BaseState
from Engine.DebugLog import Debug
from Engine.Vector2 import Vector2
import pygame
import os

class State_Level(BaseState):
    statename = "Level 1"

    def __init__(self, resourcemanager, window):
        super().__init__(resourcemanager, window, State_Level.statename)
        self.backgroundColor = (137, 207, 240)

        self.cameraPos = Vector2()
        self.level = 1
        self.isOnGround = False
        self.playerPos = Vector2()
        self.playerVel = Vector2()
        self.map = []
    
    def __drawMap(self):
        Tiles = ["-", "Brick", "Slope", "Ring", "Spike", "Startpoint", "Endpoint",
                 "Checkpoint_Active", "Checkpoint_NotActive"]
        with open(os.path.join("Assets", "Level", f'Level{self.level}.dat'), "r") as f:
            y = 0
            for line in f:
                list = line.split(',')
                x = 0
                for index in list:
                    value = int(index, 10)
                    if value != 0:
                        super().AddDrawCall(Tiles[value], Vector2(x * 64, y * 64))
                    x += 1
                y += 1

    def __handleCollision(self):
        pass

    def __handlePhysics(self, dt: float):
        # Gravity
        if not self.isOnGround:
            self.playerVel.y += 9.8 * dt * 2
            # Terminal velocity
            if self.playerVel.y > 33.0:
                self.playerVel.y = 33.0
        else:
            self.playerVel.y = 0.0

        # Friction
        if self.playerVel.x > 0.3:
            self.playerVel.x -= 0.2
        elif self.playerVel.x < -0.3:
            self.playerVel.x += 0.2
        else:
            self.playerVel.x = 0.0

        self.playerPos += self.playerVel * 64.0 * dt # assume 64px = 1metre

    def __handleKeyInput(self):
        keypress = pygame.key.get_pressed()
        if keypress[K_UP] and self.isOnGround:
            self.playerVel.y = -7.5
        #elif keypress[K_DOWN]:
        #    self.playerVel.y = 5
        if keypress[K_LEFT]:
            if self.playerVel.x > -3:
                self.playerVel.x -= 1
        elif keypress[K_RIGHT]:
            if self.playerVel.x < 3:
                self.playerVel.x += 1

    def Load(self):
        super().Load()

    def Update(self, dt):
        self.__handleKeyInput()
        self.__handleCollision()
        self.__handlePhysics(dt)

        self.__drawMap()
        super().AddDrawCall("Ball", self.playerPos)

        super().Update(dt)
        super().Draw()
