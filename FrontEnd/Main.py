# Import modules
import sys
import os
import pygame
import pygame_gui
import re

# Allow parent directory to system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from BackEnd.Authentication import Authentication
from RegisterMenu import RegisterMenu
from LoginMenu import LoginMenu
from Error import Error
from GameMenu import GameMenu
from GameModeSelectMenu import GameModeSelectMenu
from BackEnd.Game import Game
from Tutorial import Tutorial
from BackEnd.TutorialEngine import TutorialEngine
from LeaderboardSelectMenu import LeaderboardSelectMenu
from Leaderboard import Leaderboard
from GameOverMenu import GameOverMenu
from BackEnd.Settings import Settings
from SettingsMenu import SettingMenu

class Main:
    """
    Main class to handle the game loop and manage different screens in the application.
    """
    def __init__(self):
        """
        Initialise the main application, setting up the display, music, and initial screen.
        """
        pygame.init()
        pygame.display.set_caption("BASED")
        self.isRunning = True
        self.screen = "mainMenu"
        self.displayWidth, self.displayHeight = 1080, 640
        self.display = pygame.Surface((self.displayWidth, self.displayHeight))
        self.window = pygame.display.set_mode((self.displayWidth, self.displayHeight))
        self.black = (0, 0, 0)
        self.clock = pygame.time.Clock()
        self.manager = pygame_gui.UIManager((1080, 640))

        self.currentMusic = ""

        # Audio volume
        musicVolume = Settings().getKeyVariable("Music")
        pygame.mixer.music.set_volume(musicVolume)

        # Silent login
        try:
            auth = Authentication()
            if auth.silentLogin():
                self.currentDisplay = GameMenu(self.switchScreen, self.display, self.manager,
                                                self.currentMusic,
                                                self.endGame)
                self.currentMusic = "Littleroot_Town"
            else:
                self.currentDisplay = RegisterMenu(self.switchScreen, self.display, self.manager, self.currentMusic)
                self.currentMusic = ""
        except:
            errorMsg = ["Database Error Occurred:", "Please contact Admin to resolve the matter."]
            self.currentDisplay = Error(self.switchScreen, self.display, self.manager, self.currentMusic, errorMsg)

    def switchScreen(self, screen):
        """
        Switch the screens based on the screen identifier.
        :param screen: The identifier for the screen to switch to.
        :return: None
        """
        self.screen = screen
        self.manager = pygame_gui.UIManager((1080, 640))
        if re.match(r"^.+;.+;.+$", self.screen):
            variables = self.screen.split(";")
            match variables[0]:
                case "error":
                    errorMsg = [variables[1], variables[2]]
                    self.currentDisplay = Error(self.switchScreen, self.display, self.manager, self.currentMusic, errorMsg)
                    self.currentMusic = ""
                case "game":
                    self.currentDisplay = Game(self.switchScreen, self.display, self.manager, self.currentMusic, variables[1])
                    self.switchMusic("Snowy")
                case "tutorial":
                    self.currentDisplay = Tutorial(self.switchScreen, self.display, self.manager, self.currentMusic,
                                                   variables[1])
                    self.switchMusic("Sans")
                case "tutorialEngine":
                    self.currentDisplay = TutorialEngine(self.switchScreen, self.display, self.manager,
                                                         self.currentMusic, variables[1])
                    self.switchMusic("Sans")
                case "leaderboard":
                    self.currentDisplay = Leaderboard(self.switchScreen, self.display, self.manager, self.currentMusic,
                                                      variables[1],
                                                      variables[2])
                    self.switchMusic("Fallen_Down")
                case "gameOver":
                    self.currentDisplay = GameOverMenu(self.switchScreen, self.display, self.manager, self.currentMusic,
                                                       score=int(variables[1]), timeTaken=variables[2],
                                                       highScore=int(variables[3]), gameMode=variables[4])
                    self.switchMusic("musicHere")

        else:
            match self.screen:
                case "registerMenu":
                    self.currentDisplay = RegisterMenu(self.switchScreen, self.display, self.manager, self.currentMusic)
                    self.currentMusic = ""
                case "loginMenu":
                    self.currentDisplay = LoginMenu(self.switchScreen, self.display, self.manager, self.currentMusic)
                    self.currentMusic = ""
                case "gameMenu":
                    self.currentDisplay = GameMenu(self.switchScreen, self.display, self.manager, self.currentMusic,
                                                   self.endGame)
                    self.switchMusic("Littleroot_Town")
                case "gameModeSelectMenu":
                    self.currentDisplay = GameModeSelectMenu(self.switchScreen, self.display, self.manager, self.currentMusic)
                    self.switchMusic("Littleroot_Town")
                case "leaderboardSelectMenu":
                    self.currentDisplay = LeaderboardSelectMenu(self.switchScreen, self.display, self.manager,
                                                                self.currentMusic)
                    self.switchMusic("Littleroot_Town")
                case "settingMenu":
                    self.currentDisplay = SettingMenu(self.switchScreen, self.display, self.manager, self.currentMusic)
                    self.currentMusic = ""


    def switchMusic(self, music):
        """
        Switch the music theme based on screen.
        :param music: The music to be played.
        :return: None
        """
        self.currentMusic = music

    def endGame(self):
        """
        End the game loop and sets the game state to false.
        :return: None
        """
        self.isRunning = False

    def gameLoop(self):
        """
        Main game loop to processes events, update displays, and render UI.
        :return: None
        """
        clock = self.clock.tick(60)
        timeDelta = clock / 1000

        for ev in pygame.event.get():
            self.manager.process_events(ev)

            if ev.type == pygame.QUIT:
                self.isRunning = False
                break
            self.currentDisplay.eventCheck(ev)

        self.currentDisplay.update(timeDelta)
        self.window.blit(self.display, (0, 0))
        self.manager.draw_ui(self.window)
        self.currentDisplay.draw()
        pygame.display.update()

# Start
if __name__ == "__main__":
    main = Main()
    while main.isRunning:
        main.gameLoop()
