from pygame.constants import K_RETURN
from Engine.BaseState import BaseState
from Engine.DebugLog import Debug
from Engine.LevelMap import LevelMap
from Engine.ResourceManager import ResourceManager
from Engine.StateManager import StateManager
from Engine.Vector2 import Vector2
from Engine.Utilities import MYCOLOR
import pygame
import os

class State_GameOver(BaseState):
    statename = "Game Over"

    def __init__(self, sm : StateManager, rm : ResourceManager, window : pygame.Surface):
        super().__init__(sm, rm, window, State_GameOver.statename)
        self.backgroundColor = (100, 180, 220)
        
        self.levelMap = LevelMap(64) # GridSize = 64x64
    
    def __drawMap(self):
        Tiles = LevelMap.Tiles
        dimension = self.levelMap.mapDim
        map = self.levelMap.map
        for x in range(dimension[0]):
            for y in range(dimension[1]):
                value = map[y * dimension[0] + x]
                if value != 0:
                    position = Vector2(x * 64, y * 64)
                    self.AddDrawSprite(Tiles[value], position)

    def __handleKeyInput(self):
        # Trigger once
        # Toggle Debug
        for env in self.eventlist:
            if env.type == pygame.KEYDOWN:            
                if env.key == K_RETURN:
                    self.sm.ChangeState("Main Menu")
                    self.rm.GetAudioClip("Selecting").Play()

    def __drawUIs(self):
        if self.sm.variables["Lives"] == -1: # Died
            self.AddDrawUIFont("You Died!", Vector2(32, 64), MYCOLOR.RED, 72)
            self.AddDrawUIFont(f'Levels Completed : {self.sm.variables["CurrentLevel"] - 1} / {self.sm.variables["NumOfLevels"]}', Vector2(32, 150), MYCOLOR.WHITE, 30)
        else:
            self.AddDrawUIFont("All Levels Completed!", Vector2(32, 64), MYCOLOR.GREEN, 72)
            self.AddDrawUIFont(f'Levels Completed : {self.sm.variables["NumOfLevels"]} / {self.sm.variables["NumOfLevels"]}', Vector2(32, 150), MYCOLOR.WHITE, 30)

        self.AddDrawUIFont(f'Coins Collected : {self.sm.variables["Coins"]} / 600', Vector2(32, 180), MYCOLOR.WHITE, 30)
        self.AddDrawUIFont(f'Time Elapsed : {int(self.sm.variables["TimeTaken"] / 60)}m {int(self.sm.variables["TimeTaken"] % 60)}s', Vector2(32, 210), MYCOLOR.WHITE, 30)

        self.AddDrawUIFont("[Enter] Return to main menu", Vector2(32, 250), MYCOLOR.RED, 25)
            

    def Load(self):
        super().Load()
        self.levelMap.LoadMap(os.path.join("Assets", "Level", 'GameOverScreen.dat'))
        self.rm.GetAudioClip("MainMenuBGM").source.play(loops=-1)
    
    def Unload(self):
        super().Unload()
        self.rm.GetAudioClip("MainMenuBGM").source.stop()
    
    def Update(self, dt):
        self.__handleKeyInput()
        # Draw screen
        self.__drawMap()
        self.__drawUIs()

        super().Update(dt)
        super().Draw()
