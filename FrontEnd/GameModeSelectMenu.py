import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pygame
import pygame_gui


class GameModeSelectMenu:
    def __init__(self, screen, display, manager):
        pygame.init()
        self.screen = screen
        self.display = display
        self.manager = manager

        self.manager.get_theme().load_theme("../ThemeFile/GameMenu.json")

        self.conversionButton = None
        self.additionButton = None
        self.subtractionButton = None
        self.backButton = None

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

        # Conversion button
        conversionButtonRect = pygame.Rect((0, 0), (350, 70))
        conversionButtonRect.top = initialYElement + (stackY * 2)
        self.conversionButton = pygame_gui.elements.UIButton(relative_rect=conversionButtonRect,
                                                             text="CONVERSION",
                                                             manager=self.manager,
                                                             object_id=pygame_gui.core.ObjectID(
                                                                 class_id="@gameModeSelectButton",
                                                                 object_id="#conversionButton"),
                                                             anchors={'centerx': 'centerx',
                                                                      'top': 'top'})

        # Addition button
        additionButtonRect = pygame.Rect((0, 0), (350, 70))
        additionButtonRect.top = initialYElement + (stackY * 3)
        self.additionButton = pygame_gui.elements.UIButton(relative_rect=additionButtonRect,
                                                           text="ADDITION",
                                                           manager=self.manager,
                                                           object_id=pygame_gui.core.ObjectID(
                                                               class_id="@gameModeSelectButton",
                                                               object_id="#additionButton"),
                                                           anchors={'centerx': 'centerx',
                                                                    'top': 'top'})

        # Subtract button
        subtractionButtonRect = pygame.Rect((0, 0), (350, 76))
        subtractionButtonRect.top = initialYElement + (stackY * 4)
        self.subtractionButton = pygame_gui.elements.UIButton(relative_rect=subtractionButtonRect,
                                                              text="SUBTRACTION",
                                                              manager=self.manager,
                                                              object_id=pygame_gui.core.ObjectID(
                                                                  class_id="@gameModeSelectButton",
                                                                  object_id="#subtractionButton"),
                                                              anchors={'centerx': 'centerx',
                                                                       'top': 'top'})

        # Back button
        backButtonRect = pygame.Rect((0, 0), (50, 50))
        backButtonRect.topright = -50, 50
        self.backButton = pygame_gui.elements.UIButton(relative_rect=backButtonRect,
                                                       text="Back",
                                                       manager=self.manager,
                                                       anchors={'right': 'right',
                                                                'top': 'top'})

    def eventCheck(self, ev):
        match ev.type:
            case pygame_gui.UI_BUTTON_PRESSED:
                print(ev.ui_element)
                match ev.ui_element:
                    case self.conversionButton:
                        print("plays")
                    case self.additionButton:
                        print("leaderboards")
                    case self.subtractionButton:
                        print("exits")
                    case self.backButton:
                        self.screen("gameMenu")

    def update(self, timeDelta):
        self.manager.update(timeDelta)
