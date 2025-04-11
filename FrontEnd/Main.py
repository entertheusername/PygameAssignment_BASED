import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pygame
import pygame_gui
import re
from BackEnd.Authentication import Authentication
from RegisterMenu import RegisterMenu
from LoginMenu import LoginMenu
from Error import Error
from GameMenu import GameMenu
from GameModeSelectMenu import GameModeSelectMenu
from GameEngine_game import Game
from LeaderboardSelectMenu import LeaderboardSelectMenu


class Main:
    def __init__(self):
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
        try:
            auth = Authentication()
            self.currentDisplay = GameMenu(self.switchScreen, self.display, self.manager,
                                           self.endGame) if auth.silentLogin() else RegisterMenu(self.switchScreen,
                                                                                                 self.display,
                                                                                                 self.manager)
        except:
            self.currentDisplay = Error(self.switchScreen, self.display, self.manager)

    def switchScreen(self, screen):
        self.screen = screen
        self.manager = pygame_gui.UIManager((1080, 640))
        if re.match(r"^.+;.+;.+$", self.screen):
            variables = self.screen.split(";")
            match variables[0]:
                case "error":
                    errorMsg = [variables[1], variables[2]]
                    self.currentDisplay = Error(self.switchScreen, self.display, self.manager, errorMsg)
                case "game":
                    self.currentDisplay = Game(self.switchScreen, self.display, self.manager, variables[1])
                case "leaderboard":
                    # self.currentDisplay = Leaderboard(self.switchScreen, self.display, self.manager, variables[1],
                    #                                   variables[2])
                    pass
        else:
            match self.screen:
                case "registerMenu":
                    self.currentDisplay = RegisterMenu(self.switchScreen, self.display, self.manager)
                case "loginMenu":
                    self.currentDisplay = LoginMenu(self.switchScreen, self.display, self.manager)
                case "gameMenu":
                    self.currentDisplay = GameMenu(self.switchScreen, self.display, self.manager, self.endGame)
                case "gameModeSelectMenu":
                    self.currentDisplay = GameModeSelectMenu(self.switchScreen, self.display, self.manager)
                case "leaderboardSelectMenu":
                    self.currentDisplay = LeaderboardSelectMenu(self.switchScreen, self.display, self.manager)

    def endGame(self):
        self.isRunning = False

    def gameLoop(self):
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


if __name__ == "__main__":
    main = Main()
    while main.isRunning:
        main.gameLoop()
