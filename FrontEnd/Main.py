import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pygame
import pygame_gui
from RegisterMenu import RegisterMenu
from LoginMenu import LoginMenu
from GameMenu import GameMenu


class Main:
    def __init__(self):
        pygame.init()
        self.isRunning = True
        self.screen = "mainMenu"
        self.displayWidth, self.displayHeight = 1080, 640
        self.display = pygame.Surface((self.displayWidth, self.displayHeight))
        self.window = pygame.display.set_mode((self.displayWidth, self.displayHeight))
        self.black = (0, 0, 0)
        self.clock = pygame.time.Clock()
        self.manager = pygame_gui.UIManager((1080, 640))
        self.currentDisplay = RegisterMenu(self.switchScreen, self.display, self.manager)

    def switchScreen(self, screen):
        self.screen = screen
        self.manager = pygame_gui.UIManager((1080, 640))
        match self.screen:
            case "registerMenu":
                self.currentDisplay = RegisterMenu(self.switchScreen, self.display, self.manager)
            case "loginMenu":
                self.currentDisplay = LoginMenu(self.switchScreen, self.display, self.manager)
            case "gameMenu":
                self.currentDisplay = GameMenu(self.switchScreen, self.display, self.manager)

    def gameLoop(self):
        # print(self.screen)
        timeDelta = self.clock.tick(60) / 1000.0
        for ev in pygame.event.get():
            self.manager.process_events(ev)

            if ev.type == pygame.QUIT:
                self.isRunning = False
                break

            self.currentDisplay.eventCheck(ev)

            self.currentDisplay.update(timeDelta)

        self.window.blit(self.display, (0, 0))
        self.manager.draw_ui(self.window)
        pygame.display.update()


if __name__ == "__main__":
    main = Main()
    while main.isRunning:
        main.gameLoop()
