import pygame
from pygame.constants import K_DOWN, K_RETURN, K_UP
from Engine.BaseState import BaseState
from Engine.DebugLog import Debug
from Engine.LevelMap import LevelMap
from Engine.ResourceManager import ResourceManager
from Engine.StateManager import StateManager
from Engine.Vector2 import Vector2
from State_Level import State_Level
from Engine.Utilities import MYCOLOR
import os

class State_MainMenu(BaseState):
    statename = "Main Menu"

    def __init__(self, sm : StateManager, rm : ResourceManager, window : pygame.Surface):
        super().__init__(sm, rm, window, State_MainMenu.statename)
        self.backgroundColor = (100, 180, 220)
        
        self.selected = 0
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
                    self.AddDrawCall(Tiles[value], position)

    def __handleKeyInput(self):
        # Trigger once
        # Toggle Debug
        for env in self.eventlist:
            if env.type == pygame.KEYDOWN:            
                if env.key == K_UP or env.key == K_DOWN:
                    self.selected = 0 if self.selected == 1 else 1
                elif env.key == K_RETURN:
                    if self.selected == 0:
                        self.sm.ChangeState(State_Level.statename)
                    else:
                        self.sm.ChangeState("None")


    def Load(self):
        super().Load()
        self.levelMap.LoadMap(os.path.join("Assets", "Level", 'TitleScreen.dat'))
        
    
    def Update(self, dt):
        self.__handleKeyInput()
        # Draw screen
        self.__drawMap()
        self.AddDrawCall("Title", Vector2(0, 0))
        self.AddDrawUIText("Play", Vector2(32, 200), MYCOLOR.RED if self.selected == 0 else MYCOLOR.WHITE, 
                                                        70 if self.selected == 0 else 50)
        self.AddDrawUIText("Quit", Vector2(32, 250), MYCOLOR.RED if self.selected == 1 else MYCOLOR.WHITE,
                                                        70 if self.selected == 1 else 50)

        super().Update(dt)
        super().Draw()
