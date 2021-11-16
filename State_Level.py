from pygame import event
from pygame.constants import K_DOWN, K_F1, K_LEFT, K_RIGHT, K_UP
from Engine.BaseState import BaseState
from Engine.LevelMap import LevelMap
from Engine.DebugLog import Debug
from Engine.Vector2 import Vector2
import Engine.Utilities
import pygame
import os

class Camera:
    def __init__(self):
        self.position = Vector2(0,0)

class Player:
    def __init__(self):
        self.position = Vector2(0,0)
        self.velocity = Vector2(0,0)
        self.radius = 28

    def colliderData(self):
        return (self.position + Vector2(32,32), self.radius)

class State_Level(BaseState):
    statename = "Level 1"

    def __init__(self, resourcemanager, window):
        super().__init__(resourcemanager, window, State_Level.statename)
        self.backgroundColor = (137, 207, 240)
        self.gravity = 1.8

        self.showDebug = False
        self.camera = Camera()
        
        self.player = Player()
        self.isOnGround = False

        self.levelMap = LevelMap(64) # GridSize = 64x64
        self.level = 1
            
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

        player_collider = self.player.colliderData()
        self.AddDrawDebugCircleCall(player_collider[0], player_collider[1], GREEN_COLOR)

    def __handleCollision(self):
        BLUE_COL = (0,0,255)

        player_collider = self.player.colliderData()
        # Collision between player and world
        for colider in self.levelMap.colliders:
            collision = Engine.Utilities.CircleAABB(player_collider[0], player_collider[1], colider.position, colider.position + colider.size)
            if collision.hit:
                # Resolve
                resolve_dir = (player_collider[0] - collision.contactPoint).Normalized()
                resolve_dist = self.player.radius - (player_collider[0] - collision.contactPoint).Length()
                self.player.position += resolve_dir * resolve_dist
                self.player.velocity = Vector2.Zero()
                self.isOnGround = True
                # Debug draw contact point
                if self.showDebug:
                    self.AddDrawDebugPointCall(collision.contactPoint, BLUE_COL)

    def __handlePhysics(self, dt: float):
        # Gravity
        if not self.isOnGround:
            self.player.velocity.y += self.gravity * dt * 2
            # Terminal velocity
            if self.player.velocity.y > 33.0:
                self.player.velocity.y = 33.0
        else:
            self.player.velocity.y = 0.0

        # Friction
        if self.player.velocity.x > 0.3:
            self.player.velocity.x -= 0.2
        elif self.player.velocity.x < -0.3:
            self.player.velocity.x += 0.2
        else:
            self.player.velocity.x = 0.0

        self.player.position += self.player.velocity * 64.0 * dt # assume 64px = 1metre

    def __handleKeyInput(self):
        # Trigger once
        # Toggle Debug
        for env in self.eventlist:
            if env.type == pygame.KEYDOWN:            
                if env.key == K_F1:
                    self.showDebug = not self.showDebug
                if env.key == K_UP and self.isOnGround:
                    self.player.velocity.y = -7.5
        #elif keypress[K_DOWN]:
        #    self.playerVel.y = 5

        # Repeated call
        keypress = pygame.key.get_pressed()
        if keypress[K_LEFT]:
            if self.player.velocity.x > -3:
                self.player.velocity.x -= 1
        elif keypress[K_RIGHT]:
            if self.player.velocity.x < 3:
                self.player.velocity.x += 1

    def Load(self):
        super().Load()
        self.levelMap.LoadMap(os.path.join("Assets", "Level", f'Level{self.level}.dat'))
        self.levelMap.GenerateColliders()
        self.player.position = self.levelMap.GetStartPoint_ScreenPos() - Vector2(0,64)

    def Update(self, dt):
        self.__handleKeyInput()
        self.__handlePhysics(dt)
        self.__handleCollision()

        self.__drawMap()
        super().AddDrawCall("Ball", self.player.position)


        if self.showDebug:
            self.__drawColliders()

        super().Update(dt)
        super().Draw()
