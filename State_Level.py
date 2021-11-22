from pygame.constants import K_DOWN, K_F1, K_LEFT, K_RIGHT, K_UP
from Engine.BaseState import BaseState
from Engine.LevelMap import LevelMap
from Engine.DebugLog import Debug
from Engine.ResourceManager import ResourceManager
from Engine.StateManager import StateManager
from Engine.Vector2 import Vector2
from Engine.Utilities import MYCOLOR
import Engine.Utilities
import pygame
import os

from State_MainMenu import State_MainMenu

class Camera:
    def __init__(self, size : Vector2):
        self.position = Vector2()
        self.size = size
        self.bufferSize = 64
        self.boundary = (Vector2(), Vector2())
    
    def isWithinView(self, pos):
        buffer = Vector2(self.bufferSize, self.bufferSize)
        return Engine.Utilities.PointAABB(pos, self.position - buffer, self.position + self.size + buffer)

    def clampToBoundary(self):
        if self.position.x < self.boundary[0].x: self.position.x = self.boundary[0].x
        elif self.position.x > self.boundary[1].x: self.position.x = self.boundary[1].x
        if self.position.y < self.boundary[0].y: self.position.y = self.boundary[0].y
        if self.position.y > self.boundary[1].y: self.position.y = self.boundary[1].y

class Player:
    def __init__(self):
        self.position = Vector2(0,0)
        self.velocity = Vector2(0,0)
        self.radius = 28
        self.lives = 3
        self.coins = 0
    
    def Died(self, respawnpt : Vector2):
        self.position = respawnpt
        self.velocity.SetZero()
        self.lives -= 1

    def isDead(self):
        return self.lives <= 0

    def colliderData(self):
        return (self.position + Vector2(32,32), self.radius)

class State_Level(BaseState):
    statename = "Levels"

    def __init__(self, sm : StateManager, rm : ResourceManager, window : pygame.Surface):
        super().__init__(sm, rm, window, State_Level.statename)
        self.backgroundColor = (100, 180, 220)
        self.gravity = 9.8

        self.showDebug = False
        self.camera = Camera(Vector2.fromTuple(window.get_size()))
        
        self.player = Player()
        self.isOnGround = False

        self.levelMap = LevelMap(64) # GridSize = 64x64
        self.numOfLevels = 2
        self.currentLevel = 1
            
    def __drawMap(self):
        Tiles = LevelMap.Tiles
        dimension = self.levelMap.mapDim
        map = self.levelMap.map
        for x in range(dimension[0]):
            for y in range(dimension[1]):
                value = map[y * dimension[0] + x]
                if value != 0:
                    position = Vector2(x * 64, y * 64)
                    if self.camera.isWithinView(position):
                        self.AddDrawCall(Tiles[value], position - self.camera.position)

    def __drawColliders(self):
        for col in self.levelMap.colliders:
            self.AddDrawDebugRectCall(col.position - self.camera.position, col.size, MYCOLOR.GREEN)
        for trig in self.levelMap.triggers:
            self.AddDrawDebugRectCall(trig.position - self.camera.position, trig.size, MYCOLOR.YELLOW)

        player_collider = self.player.colliderData()
        self.AddDrawDebugCircleCall(player_collider[0] - self.camera.position, player_collider[1], MYCOLOR.GREEN)

    def __drawUI(self):
        self.AddDrawUITex("Black", Vector2(), 0, Vector2(2, 1.3))
        self.AddDrawUITex("Ball", Vector2(10,3), 0, Vector2(0.6, 0.6))
        self.AddDrawUIText(f'x{self.player.lives}', Vector2(55, 10), MYCOLOR.WHITE, 30)
        self.AddDrawUITex("Ring", Vector2(10,43), 0, Vector2(0.6, 0.6))
        self.AddDrawUIText(f'x{self.player.coins}', Vector2(55, 50), MYCOLOR.WHITE, 30)


    def __handleCollision(self):
        player_collider = self.player.colliderData()
        # Collision between player and world
        for collider in self.levelMap.colliders:
            collision = Engine.Utilities.CircleAABB(player_collider[0], player_collider[1], collider.position, collider.position + collider.size)
            if collision.hit:
                # Resolve
                resolve_dir = (player_collider[0] - collision.contactPoint).Normalized()
                resolve_dist = self.player.radius - (player_collider[0] - collision.contactPoint).Length()
                self.player.position += resolve_dir * resolve_dist

                if resolve_dir.y <= -0.7:
                    self.player.velocity.y = 0
                    self.isOnGround = True
                if resolve_dir.y >= 0.7:
                    self.player.velocity.y = 0

                # Debug draw contact point
                if self.showDebug:
                    self.AddDrawDebugPointCall(collision.contactPoint - self.camera.position, MYCOLOR.BLUE)

    def __handleTriggers(self):
        player_collider = self.player.colliderData()
        for trigger in self.levelMap.triggers:
            if trigger.active:
                triggered = Engine.Utilities.CircleAABB(player_collider[0], player_collider[1],
                                                        trigger.position, trigger.position + trigger.size)
                if triggered.hit:
                    if trigger.name == "Ring":
                        self.player.coins += 1
                        self.levelMap.RemoveRingTrigger(trigger)
                        self.rm.GetAudioClip("PickupCoin").Play()
                        trigger.active = False
                    elif trigger.name == "Checkpoint_NotActive":
                        self.levelMap.ActivateCheckpointTrigger(trigger)
                        self.rm.GetAudioClip("Checkpoint").Play()
                        trigger.active = False
                    elif trigger.name == "Spike":
                        self.player.Died(self.levelMap.GetRespawnPoint_ScreenPos())
                        self.rm.GetAudioClip("Hit").Play()
                        break
                    elif trigger.name == "JumpPad":
                        self.player.velocity.y = -20
                        break
                    elif trigger.name == "Endpoint":
                        trigger.active = False
                        if self.currentLevel != self.numOfLevels:
                            self.__LoadLevel(self.currentLevel + 1)
                        else:
                            self.sm.ChangeState("Main Menu")
                            self.currentLevel = 1
                        break

    def __handlePhysics(self, dt: float):
        # Gravity
        self.player.velocity.y += self.gravity * dt * 2
        # Terminal velocity
        if self.player.velocity.y > 33.0:
            self.player.velocity.y = 33.0

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
                    self.isOnGround = False
                    self.player.velocity.y = -7.5
                    self.rm.GetAudioClip("Jump").Play()
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

    def __updateCamera(self):
        self.camera.position = self.player.position - Vector2(400, 400)
        self.camera.clampToBoundary()

    def __LoadLevel(self, level):
        self.currentLevel = level
        self.levelMap.LoadMap(os.path.join("Assets", "Level", f'Level{self.currentLevel}.dat'))
        self.levelMap.GenerateColliders()
        # Init camera settings
        self.camera.boundary = (Vector2(), Vector2(self.levelMap.mapDim[0] * 64 - self.camera.size.x,
                                                   self.levelMap.mapDim[1] * 64 - self.camera.size.y))
        # Init player starting position
        self.player.position = self.levelMap.GetStartPoint_ScreenPos() - Vector2(0,64)

    def __ResetStats(self):
        self.player.coins = 0
        self.player.lives = 3
        self.player.velocity.SetZero()

    def Load(self):
        super().Load()
        self.rm.GetAudioClip("inGameBGM").source.play(loops=-1)
        self.__LoadLevel(self.currentLevel)
        self.__ResetStats()

    def Unload(self):
        super().Unload()
        self.rm.GetAudioClip("inGameBGM").source.stop()

    def Update(self, dt):
        self.__handleKeyInput()
        self.__handlePhysics(dt)
        self.__handleCollision()
        self.__handleTriggers()

        self.__drawMap()
        self.__updateCamera()
        self.AddDrawCall("Ball", self.player.position - self.camera.position)
        self.__drawUI()

        if self.showDebug:
            self.__drawColliders()

        super().Update(dt)
        super().Draw()
