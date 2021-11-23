from Engine.Vector2 import Vector2

class Box:
    def __init__(self, name, pos = None, size = None, active = True):
        self.name = name
        self.position = Vector2() if pos == None else pos
        self.size = Vector2() if size == None else size
        self.active = active

class LevelMap:
    Tiles = ["-", "Brick", "Slope", "Ring", "Spike", "JumpPad", "Startpoint", "Endpoint",
            "Checkpoint_Active", "Checkpoint_NotActive"]
    TilesToIndexMap = {"-" : 0, "Brick" : 1, "Slope" : 2, "Ring" : 3, 
                        "Spike" : 4, "JumpPad" : 5, "Startpoint" : 6, "Endpoint" : 7,
                        "Checkpoint_Active" : 8, "Checkpoint_NotActive" : 9}
            
    def __init__(self, gridsize):
        self.gridsize = gridsize
        self.mapDim = ()
        self.colliders = []
        self.triggers = []
        self.map = []
        self.startpoint = Vector2()
        self.endpoint = Vector2()
        self.spawnpoint = Vector2()
        self.resetPoints = []

    def GetStartPoint_ScreenPos(self):
        return self.startpoint * self.gridsize
    
    def GetRespawnPoint_ScreenPos(self):
        return self.spawnpoint * self.gridsize

    def LoadMap(self, path):
        with open(path, "r") as f:
            x, y = 0, 0
            self.map.clear()
            for line in f:
                list = line.split(',')
                x = 0
                for index in list:
                    value = int(index, 10)
                    self.map.append(value)
                    if value == LevelMap.TilesToIndexMap["Startpoint"]:
                        self.startpoint = Vector2(x,y)
                        self.spawnpoint = self.startpoint
                    elif value == LevelMap.TilesToIndexMap["Endpoint"]:
                        self.endpoint = Vector2(x,y)
                    x += 1
                y += 1
            self.mapDim = (x,y)
    
    def GenerateColliders(self):
        # Reset existing colliders
        self.colliders.clear()
        self.triggers.clear()
        # Find colliders
        mymap = self.map.copy()
        dimension = self.mapDim
        for y in range(dimension[1]):
            for x in range(dimension[0]):
                value =  mymap[y * dimension[0] + x]
                if value == 0: # Nothing
                    continue
                if value == 1: # Wall
                    combinedSize = Vector2(1,1) # using normalized coord
                    # Combine horizonal colliders
                    if x < dimension[0]:
                        for i in range(x+1, dimension[0]):
                            if mymap[y * dimension[0] + (i)] == value:
                                mymap[y * dimension[0] + (i)] = 0
                                combinedSize.x += 1
                            else:
                                break
                    # If no horizontal then check vertical and combine
                    if y < dimension[1] and combinedSize.x == 1:
                        for i in range(y+1, dimension[1]):
                            if mymap[(i) * dimension[0] + x] == value:
                                mymap[(i) * dimension[0] + x] = 0
                                combinedSize.y += 1
                            else:
                                break
                    self.colliders.append(Box(LevelMap.Tiles[value], 
                                                Vector2(x,y) * self.gridsize, 
                                                combinedSize * self.gridsize))
                elif value == 3: # Ring
                    self.triggers.append(Box(LevelMap.Tiles[value], 
                                                Vector2(x,y) * self.gridsize + Vector2(self.gridsize/4,0), 
                                                Vector2(self.gridsize/2, self.gridsize)))
                    self.resetPoints.append((y * dimension[0] + x, value))
                elif value == 4: # Spike
                    horizontalCount = 1
                    # Combine horizonal colliders
                    if x < dimension[0]:
                        for i in range(x+1, dimension[0]):
                            if mymap[y * dimension[0] + (i)] == value:
                                mymap[y * dimension[0] + (i)] = 0
                                horizontalCount += 1
                            else:
                                break
                    self.triggers.append(Box(LevelMap.Tiles[value], 
                                                Vector2(x,y) * self.gridsize + Vector2(0,self.gridsize/2), 
                                                Vector2(self.gridsize * horizontalCount, self.gridsize/2)))
                elif value == 5: # JumpPad
                    self.triggers.append(Box(LevelMap.Tiles[value], 
                                                Vector2(x,y) * self.gridsize + Vector2(0,8), 
                                                Vector2(self.gridsize, self.gridsize-8)))
                elif value == 6 or value == 7: # Startpoint / Endpoint
                    self.triggers.append(Box(LevelMap.Tiles[value], 
                                                Vector2(x,y) * self.gridsize, 
                                                Vector2(self.gridsize, self.gridsize)))
                elif value == 9: # Checkpoint_NotActive, ignore 6(Checkpoint_Active)
                    self.triggers.append(Box(LevelMap.Tiles[value], 
                                                Vector2(x,y) * self.gridsize, 
                                                Vector2(self.gridsize, self.gridsize)))
                    self.resetPoints.append((y * dimension[0] + x, value))
    
    def Reset(self):
        # Reset coins
        # Reset checkpoints
        for point in self.resetPoints:
            self.map[point[0]] = point[1]
        for trig in self.triggers:
            trig.active = True
        # Reset spawnpoint
        self.spawnpoint = self.startpoint

    def RemoveRingTrigger(self, trigger : Box):
        rpos = (trigger.position - Vector2(self.gridsize / 4, 0)) / self.gridsize
        index = int(rpos.y) * self.mapDim[0] + int(rpos.x)
        self.map[index] = LevelMap.TilesToIndexMap["-"]

    def ActivateCheckpointTrigger(self, trigger : Box):
        rpos = trigger.position / self.gridsize
        index = int(rpos.y) * self.mapDim[0] + int(rpos.x)
        self.map[index] = LevelMap.TilesToIndexMap["Checkpoint_Active"]
        self.spawnpoint = rpos + Vector2(0, -1)