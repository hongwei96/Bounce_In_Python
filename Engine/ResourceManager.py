from Engine.DebugLog import Debug

class ResourceManager:
    def __init__(self):
        self.textureList = {}
        pass

    def AddTexture(self, tex):
        self.textureList[tex.name] = tex

    def GetTexture(self, name):
        return self.textureList.get(name)
    
    def RemoveTexture(self, name):
        self.textureList.pop(name)
    
    def PrettyPrint(self):
        string = f'Loaded Textures ({len(self.textureList)}):\n'
        for texName in self.textureList:
            string += f'- {texName}\n'
        Debug.Log(string)
