import pygame
import pygame_gui
from MainMenu import MainMenu
from TestMenu import TestMenu


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
        self.mainMenu = MainMenu(self.switchScreen, self.display, self.manager)
        self.testMenu = None

    def switchScreen(self, screen):
        self.screen = screen
        self.manager = pygame_gui.UIManager((1080, 640))
        match self.screen:
            case "mainMenu":
                self.mainMenu = MainMenu(self.switchScreen, self.display, self.manager)
            case "testMenu":
                self.testMenu = TestMenu(self.switchScreen, self.display, self.manager)

    def gameLoop(self):
        print(self.screen)
        timeDelta = self.clock.tick(60) / 1000.0
        for ev in pygame.event.get():
            self.manager.process_events(ev)

            if ev.type == pygame.QUIT:
                self.isRunning = False
                break

            match self.screen:
                case "mainMenu":
                    self.mainMenu.eventCheck(ev)
                case "testMenu":
                    self.testMenu.eventCheck(ev)

        match self.screen:
            case "mainMenu":
                self.mainMenu.update(timeDelta)
            case "testMenu":
                self.testMenu.update(timeDelta)

        # self.display.fill(self.black)
        self.window.blit(self.display, (0, 0))
        self.manager.draw_ui(self.window)
        pygame.display.update()

if __name__ == "__main__":
    main = Main()
    while main.isRunning:
        main.gameLoop()
