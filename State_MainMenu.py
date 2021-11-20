from pygame.constants import K_DOWN, K_RETURN, K_UP
from Engine.BaseState import BaseState
from Engine.DebugLog import Debug
from Engine.LevelMap import LevelMap
from Engine.ResourceManager import ResourceManager
from Engine.StateManager import StateManager
from Engine.Vector2 import Vector2
from Engine.Utilities import MYCOLOR
import pygame
import os

class CycleOptions:
    def __init__(self, min : int, max : int):
        self.currentVal : int = 0
        self.minmax = (min, max)

    def Inc(self) -> int:
        if self.currentVal == self.minmax[1]:
            self.currentVal = self.minmax[0]
        else:
            self.currentVal += 1
        return self.currentVal

    def Dec(self) -> int:
        if self.currentVal == self.minmax[0]:
            self.currentVal = self.minmax[1]
        else:
            self.currentVal -= 1
        return self.currentVal
    
    def GetColor(self, val):
        return MYCOLOR.RED if self.currentVal == val else MYCOLOR.WHITE

    def GetSize(self, val):
        return 70 if self.currentVal == val else 50

class State_MainMenu(BaseState):
    statename = "Main Menu"

    def __init__(self, sm : StateManager, rm : ResourceManager, window : pygame.Surface):
        super().__init__(sm, rm, window, State_MainMenu.statename)
        self.backgroundColor = (100, 180, 220)
        
        self.options = CycleOptions(0,2)
        self.levelMap = LevelMap(64) # GridSize = 64x64
        self.showCredits = False
    
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
                if env.key == K_UP and not self.showCredits:
                    self.options.Dec()
                    self.rm.GetAudioClip("Selecting").Play()
                elif env.key == K_DOWN and not self.showCredits:
                    self.options.Inc()
                    self.rm.GetAudioClip("Selecting").Play()
                elif env.key == K_RETURN:
                    if self.options.currentVal == 0:
                        self.sm.ChangeState("Levels")
                    elif self.options.currentVal == 1:
                        self.showCredits = not self.showCredits
                    elif self.options.currentVal == 2:
                        self.sm.ChangeState("None")
                    self.rm.GetAudioClip("Selecting").Play()

    def __drawUIs(self):
        if not self.showCredits:
            self.AddDrawCall("Title", Vector2(0, 0))
            self.AddDrawUIText("Play", Vector2(32, 200), self.options.GetColor(0), self.options.GetSize(0))
            self.AddDrawUIText("Credits", Vector2(32, 250), self.options.GetColor(1), self.options.GetSize(1))
            self.AddDrawUIText("Quit", Vector2(32, 300), self.options.GetColor(2), self.options.GetSize(2))
        else:
            self.AddDrawUIText("Credits", Vector2(32, 64), MYCOLOR.RED, 72)
            self.AddDrawUIText("Game made in Python by Chua Hong Wei", Vector2(32, 130), MYCOLOR.WHITE, 30)
            self.AddDrawUIText("BGM done by Chua Hong Zhi", Vector2(32, 160), MYCOLOR.WHITE, 30)
            self.AddDrawUIText("SFX generated at https://sfxr.me/", Vector2(32, 190), MYCOLOR.WHITE, 30)
            self.AddDrawUIText("[Enter] Return to main menu", Vector2(32, 400), MYCOLOR.RED, 30)
            

    def Load(self):
        super().Load()
        self.levelMap.LoadMap(os.path.join("Assets", "Level", 'TitleScreen.dat'))
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
