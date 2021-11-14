from pygame import event
from pygame.constants import K_DOWN, K_F1, K_LEFT, K_RIGHT, K_UP
from Engine.BaseState import BaseState
from Engine.LevelMap import LevelMap
from Engine.DebugLog import Debug
from Engine.Vector2 import Vector2
import Engine.Utilities
import pygame
import os

class State_Level(BaseState):
    statename = "Level 1"

    def __init__(self, resourcemanager, window):
        super().__init__(resourcemanager, window, State_Level.statename)
        self.backgroundColor = (137, 207, 240)

        self.showDebug = False
        self.cameraPos = Vector2()
        self.level = 1
        self.isOnGround = False
        self.playerPos = Vector2()
        self.playerVel = Vector2()

        self.levelMap = LevelMap(64) # GridSize = 64x64

        self.tpos = Vector2()
            
    def __drawMap(self):
        Tiles = LevelMap.Tiles
        dimension = self.levelMap.mapDim
        map = self.levelMap.map
        for x in range(dimension[0]):
            for y in range(dimension[1]):
                value = map[y * dimension[0] + x]
                if value != 0:
                    self.AddDrawCall(Tiles[value], Vector2(x * 64, y * 64))

    def __drawColliders(self):
        YELLOW_COLOR = (255,255,0)
        GREEN_COLOR = (0,255,0)
        for col in self.levelMap.colliders:
            self.AddDrawDebugRectCall(col.position, col.size, GREEN_COLOR)
        for trig in self.levelMap.triggers:
            self.AddDrawDebugRectCall(trig.position, trig.size, YELLOW_COLOR)

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

        #self.playerPos += self.playerVel * 64.0 * dt # assume 64px = 1metre

    def __handleKeyInput(self):
        # Trigger once
        # Toggle Debug
        for env in self.eventlist:
            if env.type == pygame.KEYDOWN:            
                if env.key == K_F1:
                    self.showDebug = not self.showDebug
                if env.key == K_UP and self.isOnGround:
                    self.playerVel.y = -7.5
        #elif keypress[K_DOWN]:
        #    self.playerVel.y = 5

        # Repeated call
        keypress = pygame.key.get_pressed()
        if keypress[K_LEFT]:
            if self.playerVel.x > -3:
                self.playerVel.x -= 1
        elif keypress[K_RIGHT]:
            if self.playerVel.x < 3:
                self.playerVel.x += 1

    def Load(self):
        super().Load()
        self.levelMap.LoadMap(os.path.join("Assets", "Level", f'Level{self.level}.dat'))
        self.levelMap.GenerateColliders()
        self.playerPos = self.levelMap.GetStartPoint_ScreenPos() - Vector2(0,64)

    def Update(self, dt):
        self.__handleKeyInput()
        self.__handleCollision()
        self.__handlePhysics(dt)

        self.__drawMap()
        super().AddDrawCall("Ball", self.playerPos)

        RED_COL = (255,0,0)
        RED2_COL = (255,128,128)
        keypress = pygame.key.get_pressed()
        if keypress[K_UP]:
            self.tpos.y -= 1
        elif keypress[K_DOWN]:
            self.tpos.y += 1
        if keypress[K_LEFT]:
            self.tpos.x -= 1
        elif keypress[K_RIGHT]:
            self.tpos.x += 1
        squarePoint = Vector2(300,300)
        squareDim = Vector2(200,150)
        circlePoint = self.tpos
        circleRadius = 100
        collision = Engine.Utilities.CircleAABB(circlePoint, circleRadius,squarePoint, squarePoint + squareDim)
        Debug.Warn(f"Check Collision : {collision}")
        self.AddDrawDebugRectCall(squarePoint, squareDim, RED_COL)
        self.AddDrawDebugRectCall(squarePoint - Vector2(circleRadius, circleRadius), 
                                  squareDim + (Vector2(circleRadius, circleRadius) * 2), RED2_COL)
        self.AddDrawDebugCircleCall(circlePoint, circleRadius, RED_COL)
        self.AddDrawDebugPointCall(circlePoint, RED_COL)
        self.AddDrawDebugCircleCall(squarePoint, circleRadius, RED2_COL)
        self.AddDrawDebugCircleCall(squarePoint + squareDim, circleRadius, RED2_COL)
        self.AddDrawDebugCircleCall(squarePoint + Vector2(squareDim.x, 0), circleRadius, RED2_COL)
        self.AddDrawDebugCircleCall(squarePoint + Vector2(0, squareDim.y), circleRadius, RED2_COL)
        """
        squarePoint = Vector2(300,300)
        squareDim = Vector2(200,150)
        collision = Engine.Utilities.PointAABB(self.tpos, squarePoint, squarePoint + squareDim)
        Debug.Warn(f"Check Collision : {collision.hit} | Contact Point : {collision.contactPoint[0]}")
        self.AddDrawDebugRectCall(squarePoint, squareDim, RED_COL)
        self.AddDrawDebugPointCall(self.tpos, RED_COL)
        """

        if self.showDebug:
            self.__drawColliders()

        super().Update(dt)
        super().Draw()
