import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pygame
import pygame_gui


class GameMenu:
    def __init__(self, screen, display, manager):
        pygame.init()
        self.screen = screen
        self.display = display
        self.manager = manager
        self.isRunning = True

        self.manager.get_theme().load_theme("../ThemeFile/GameMenu.json")

        self.playButton = None
        self.leaderboardButton = None
        self.exitButton = None

        self.uiSetup()

    def uiSetup(self):
        # Background
        self.display.blit(pygame.image.load("../Assets/Background/BackgroundBlur.png"), (0, 0))

        initialYElement = 100
        stackY = 90

        # Logo Img
        logoImage = pygame.image.load("../Assets/Logo.png")
        logoRect = pygame.Rect((-5, 0), (363, 138))
        logoRect.top = initialYElement
        logo = pygame_gui.elements.UIImage(relative_rect=logoRect,
                                           image_surface=logoImage,
                                           manager=self.manager,
                                           anchors={'centerx': 'centerx',
                                                    'top': 'top'})

        # Play button
        playButtonRect = pygame.Rect((0, 0), (350, 70))
        playButtonRect.top = initialYElement + (stackY * 2)
        self.playButton = pygame_gui.elements.UIButton(relative_rect=playButtonRect,
                                                  text="PLAY",
                                                  manager=self.manager,
                                                  object_id=pygame_gui.core.ObjectID(
                                                      class_id="@gameButton",
                                                      object_id="#playButton"),
                                                  anchors={'centerx': 'centerx',
                                                           'top': 'top'})

        # Leaderboard button
        leaderboardButtonRect = pygame.Rect((0, 0), (350, 70))
        leaderboardButtonRect.top = initialYElement + (stackY * 3)
        self.leaderboardButton = pygame_gui.elements.UIButton(relative_rect=leaderboardButtonRect,
                                                         text="LEADER BOARD",
                                                         manager=self.manager,
                                                         object_id=pygame_gui.core.ObjectID(
                                                             class_id="@gameButton",
                                                             object_id="#leaderboardButton"),
                                                         anchors={'centerx': 'centerx',
                                                                  'top': 'top'})

        # Exit button
        exitButtonRect = pygame.Rect((0, 0), (350, 76))
        exitButtonRect.top = initialYElement + (stackY * 4)
        self.exitButton = pygame_gui.elements.UIButton(relative_rect=exitButtonRect,
                                                  text="EXIT",
                                                  manager=self.manager,
                                                  object_id=pygame_gui.core.ObjectID(
                                                      class_id="@gameButton",
                                                      object_id="#exitButton"),
                                                  anchors={'centerx': 'centerx',
                                                           'top': 'top'})

    def eventCheck(self, ev):
        match ev.type:
            case pygame_gui.UI_BUTTON_PRESSED:
                print(ev.ui_element)
                match ev.ui_element:
                    case self.playButton:
                        print("plays")
                    case self.leaderboardButton:
                        print("leaderboards")
                    case self.exitButton:
                        print("exits")

    def update(self, timeDelta):
        self.manager.update(timeDelta)
