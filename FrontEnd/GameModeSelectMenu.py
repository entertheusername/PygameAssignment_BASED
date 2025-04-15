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

        self.manager.get_theme().load_theme("../ThemeFile/GameSelectMenu.json")

        self.conversionButton = None
        self.calculationButton = None
        self.mixedCalculationButton = None
        self.backButton = None

        self.uiSetup()

    def uiSetup(self):
        # Background
        self.display.fill(pygame.Color('#FFE0E3'))  # Flooding the bg with pink make the pic brighter
        self.display.blit(pygame.image.load("../Assets/Background/BackgroundBlur.png"), (0, 0))

        initialXElement = 45
        stackX = 291

        # Background Img
        backgroundRect = pygame.Rect((0, 0), (948, 451))
        background = pygame_gui.elements.UIPanel(relative_rect=backgroundRect,
                                                 manager=self.manager,
                                                 starting_height= 0,
                                                 anchors={'centerx': 'centerx',
                                                          'centery': 'centery'})

        backgroundImage = pygame.image.load("../Assets/WindowElements/BackWindow.png")
        pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect((0, 0), backgroundImage.get_size()),
            image_surface=backgroundImage,
            starting_height=0,
            manager=self.manager,
            container=background
        )

        # Title Img
        titleImage = pygame.image.load("../Assets/WindowElements/GameSelectTitle.png")
        titleRect = pygame.Rect((-5, 0), (422, 89))
        titleRect.top = 50
        title = pygame_gui.elements.UIImage(relative_rect=titleRect,
                                            image_surface=titleImage,
                                            manager=self.manager,
                                            anchors={'centerx': 'centerx',
                                                     'top': 'top'})

        # Conversion button
        conversionButtonRect = pygame.Rect((0, 0), (268, 293))
        conversionButtonRect.left = initialXElement
        self.conversionButton = pygame_gui.elements.UIButton(relative_rect=conversionButtonRect,
                                                             text="",
                                                             manager=self.manager,
                                                             object_id=pygame_gui.core.ObjectID(
                                                                 class_id="@gameModeSelectButton",
                                                                 object_id="#conversionButton"),
                                                             container=background,
                                                             anchors={'left': 'left',
                                                                      'centery': 'centery'})

        # Calculation button
        calculationButtonRect = pygame.Rect((0, 0), (268, 293))
        calculationButtonRect.left = initialXElement + stackX
        self.calculationButton = pygame_gui.elements.UIButton(relative_rect=calculationButtonRect,
                                                              text="",
                                                              manager=self.manager,
                                                              object_id=pygame_gui.core.ObjectID(
                                                                  class_id="@gameModeSelectButton",
                                                                  object_id="#calculationButton"),
                                                              container=background,
                                                              anchors={'left': 'left',
                                                                      'centery': 'centery'})

        # Mixed Calculation button
        mixedCalculationButtonRect = pygame.Rect((0, 0), (268, 293))
        mixedCalculationButtonRect.left = initialXElement + (stackX * 2)
        self.mixedCalculationButton = pygame_gui.elements.UIButton(relative_rect=mixedCalculationButtonRect,
                                                                   text="",
                                                                   manager=self.manager,
                                                                   object_id=pygame_gui.core.ObjectID(
                                                                       class_id="@gameModeSelectButton",
                                                                       object_id="#mixedCalculationButton"),
                                                                   container=background,
                                                                   anchors={'left': 'left',
                                                                      'centery': 'centery'})

        # Back button
        backButtonRect = pygame.Rect((0, 0), (56, 56))
        backButtonRect.topright = -50, 75
        self.backButton = pygame_gui.elements.UIButton(relative_rect=backButtonRect,
                                                       text="",
                                                       object_id=pygame_gui.core.ObjectID(
                                                           class_id="@gameModeSelectButton",
                                                           object_id="#backButton"),
                                                       manager=self.manager,
                                                       anchors={'right': 'right',
                                                                'top': 'top'})

    def eventCheck(self, ev):
        match ev.type:
            case pygame_gui.UI_BUTTON_PRESSED:
                print(ev.ui_element)
                match ev.ui_element:
                    case self.conversionButton:
                        self.screen("game;conversion;none")
                    case self.calculationButton:
                        self.screen("game;basic_calculation;none")
                    case self.mixedCalculationButton:
                        self.screen("game;mixed_calculation;none")
                    case self.backButton:
                        self.screen("gameMenu")

    def update(self, timeDelta):
        self.manager.update(timeDelta)

    def draw(self):
        pass
