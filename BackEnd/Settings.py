import json


class Settings:
    def __init__(self):
        file = open("../settings.json", "r")
        self.settings = json.load(file)
        file.close()

    def setKeyVariable(self, key, value):
        self.settings[key] = value
        file = open("../settings.json", "w")
        json.dump(self.settings, file, indent=4)
        file.close()

    def getKeyVariable(self, key):
        return self.settings[key]