import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pygame
import pygame_gui


class LeaderboardSelectMenu:
    def __init__(self, screen, display, manager):
        pygame.init()
        self.screen = screen
        self.display = display
        self.manager = manager

        self.manager.get_theme().load_theme("../ThemeFile/LeaderboardSelectMenu.json")

        self.conversionMonthButton = None
        self.calculationMonthButton = None
        self.mixedCalculationMonthButton = None
        self.conversionAllButton = None
        self.calculationAllButton = None
        self.mixedCalculationAllButton = None
        self.backButton = None

        self.uiSetup()

    def uiSetup(self):
        # Background
        self.display.fill(pygame.Color('#FFE0E3'))  # Flooding the bg with pink make the pic brighter
        self.display.blit(pygame.image.load("../Assets/Background/BackgroundBlur.png"), (0, 0))

        initialXElement = 87
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
        titleImage = pygame.image.load("../Assets/WindowElements/LeaderboardSelectTitle.png")
        titleRect = pygame.Rect((-5, 0), (422, 89))
        titleRect.top = 50
        title = pygame_gui.elements.UIImage(relative_rect=titleRect,
                                            image_surface=titleImage,
                                            manager=self.manager,
                                            anchors={'centerx': 'centerx',
                                                     'top': 'top'})

        # Game Mode Board Img
        gamemodeImage = pygame.image.load("../Assets/WindowElements/GameModeBoard.png")
        gamemodeRect = pygame.Rect((0, 0), (855, 294))
        gamemode = pygame_gui.elements.UIImage(relative_rect=gamemodeRect,
                                            image_surface=gamemodeImage,
                                            manager=self.manager,
                                            container= background,
                                            anchors={'centerx': 'centerx',
                                                     'centery': 'centery'})

        # Conversion button
        conversionMonthButtonRect = pygame.Rect((0, 0), (197, 57))
        conversionMonthButtonRect.left = initialXElement
        self.conversionMonthButton = pygame_gui.elements.UIButton(relative_rect=conversionMonthButtonRect,
                                                             text="",
                                                             manager=self.manager,
                                                             object_id=pygame_gui.core.ObjectID(
                                                                 class_id="@monthSelectButton",
                                                                 object_id="#conversionButton"),
                                                             container=background,
                                                             anchors={'left': 'left',
                                                                      'centery': 'centery'})

        conversionAllButtonRect = pygame.Rect((0, 70), (197, 57))
        conversionAllButtonRect.left = initialXElement
        self.conversionAllButton = pygame_gui.elements.UIButton(relative_rect=conversionAllButtonRect,
                                                             text="",
                                                             manager=self.manager,
                                                             object_id=pygame_gui.core.ObjectID(
                                                                 class_id="@alltimeSelectButton",
                                                                 object_id="#conversionButton"),
                                                             container=background,
                                                             anchors={'left': 'left',
                                                                      'centery': 'centery'})

        # Calculation button
        calculationMonthButtonRect = pygame.Rect((0, 0), (197, 57))
        calculationMonthButtonRect.left = initialXElement + stackX
        self.calculationMonthButton = pygame_gui.elements.UIButton(relative_rect=calculationMonthButtonRect,
                                                              text="",
                                                              manager=self.manager,
                                                              object_id=pygame_gui.core.ObjectID(
                                                                  class_id="@monthSelectButton",
                                                                  object_id="#calculationButton"),
                                                              container=background,
                                                              anchors={'left': 'left',
                                                                      'centery': 'centery'})

        calculationAllButtonRect = pygame.Rect((0, 70), (197, 57))
        calculationAllButtonRect.left = initialXElement + stackX
        self.calculationAllButton = pygame_gui.elements.UIButton(relative_rect=calculationAllButtonRect,
                                                              text="",
                                                              manager=self.manager,
                                                              object_id=pygame_gui.core.ObjectID(
                                                                  class_id="@alltimeSelectButton",
                                                                  object_id="#calculationButton"),
                                                              container=background,
                                                              anchors={'left': 'left',
                                                                       'centery': 'centery'})

        # Mixed Calculation button
        mixedCalculationMonthButtonRect = pygame.Rect((0, 0), (197, 57))
        mixedCalculationMonthButtonRect.left = initialXElement + (stackX * 2)
        self.mixedCalculationMonthButton = pygame_gui.elements.UIButton(relative_rect=mixedCalculationMonthButtonRect,
                                                                   text="",
                                                                   manager=self.manager,
                                                                   object_id=pygame_gui.core.ObjectID(
                                                                       class_id="@monthSelectButton",
                                                                       object_id="#mixedCalculationButton"),
                                                                   container=background,
                                                                   anchors={'left': 'left',
                                                                      'centery': 'centery'})

        mixedCalculationAllButtonRect = pygame.Rect((0, 70), (197, 57))
        mixedCalculationAllButtonRect.left = initialXElement + (stackX * 2)
        self.mixedCalculationAllButton = pygame_gui.elements.UIButton(relative_rect=mixedCalculationAllButtonRect,
                                                                   text="",
                                                                   manager=self.manager,
                                                                   object_id=pygame_gui.core.ObjectID(
                                                                       class_id="@alltimeSelectButton",
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
                    case self.conversionMonthButton:
                        self.screen("leaderboard:conversion:month")
                    case self.calculationMonthButton:
                        self.screen("leaderboard:calculation:month")
                    case self.mixedCalculationMonthButton:
                        self.screen("leaderboard:mixedcalculation:month")
                    case self.conversionAllButton:
                        self.screen("leaderboard:conversion:all")
                    case self.calculationAllButton:
                        self.screen("leaderboard:calculation:all")
                    case self.mixedCalculationAllButton:
                        self.screen("leaderboard:mixedcalculation:all")
                    case self.backButton:
                        self.screen("gameMenu")

    def update(self, timeDelta):
        self.manager.update(timeDelta)

    def draw(self):
        pass
