import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json


class Settings:
    def __init__(self):
        file = open("../settings.json", "r")
        self.settings = json.load(file)
        file.close()

    def setKeyVariable(self, key, value):
        """
        Set value in the settings.json.
        :param key: Which key is selected.
        :param value: What value to change it to.
        :return: None
        """
        self.settings[key] = value
        file = open("../settings.json", "w")
        json.dump(self.settings, file, indent=4)
        file.close()

    def getKeyVariable(self, key):
        """
        Get value in the settings.json.
        :param key: Which key is selected.
        :return: Value of selected key.
        """
        return self.settings[key]