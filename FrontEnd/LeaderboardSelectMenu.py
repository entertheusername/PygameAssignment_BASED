# Import modules
import sys
import os
import pygame
import pygame_gui

# Allow parent directory to system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from BackEnd.Settings import Settings

class LeaderboardSelectMenu:
    """
    Handle the leaderboard selection menu and allow user to view different leaderboard lists.
    """
    def __init__(self, screen, display, manager, music):
        """
        Initialise the LeaderboardSelectMenu class and setup the interface.

        :param screen: The pygame screen surface for rendering.
        :param display: The display manager for the game.
        :param manager: The UI manager to handle UI elements.
        :param music: The music to be played in the menu.
        :return: None
        """
        pygame.init()

        # Default
        self.screen = screen
        self.display = display
        self.manager = manager

        # Theme
        self.manager.get_theme().load_theme("../ThemeFile/LeaderboardSelectMenu.json")

        # Audio
        if music != "Littleroot_Town":
            pygame.mixer.music.load("../Assets/Audio/GameMenuSong-Littleroot_Town.ogg")
            pygame.mixer.music.play(-1, fade_ms=3000)

        sfxVolume = Settings().getKeyVariable("SFX")

        self.buttonClick = pygame.mixer.Sound("../Assets/Audio/ButtonClick.wav")
        self.buttonClick.set_volume(sfxVolume)

        # LeaderboardSelect
        self.conversionMonthButton = None
        self.calculationMonthButton = None
        self.mixedCalculationMonthButton = None
        self.conversionAllButton = None
        self.calculationAllButton = None
        self.mixedCalculationAllButton = None
        self.closeButton = None

        self.uiSetup()

    def uiSetup(self):
        """
        Sets up the basic GUI for leaderboard selection menu.
        :return: None
        """
        # Background
        self.display.fill(pygame.Color('#FFE0E3'))  # Flooding the bg with pink make the pic brighter
        self.display.blit(pygame.image.load("../Assets/Background/BackgroundBlur.png"), (0, 0))

        initialXElement = 87
        stackX = 291

        # Background image
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

        # Title image
        titleImage = pygame.image.load("../Assets/WindowElements/LeaderboardSelectTitle.png")
        titleRect = pygame.Rect((-5, 0), (331, 89))
        titleRect.top = 50
        title = pygame_gui.elements.UIImage(relative_rect=titleRect,
                                            image_surface=titleImage,
                                            manager=self.manager,
                                            anchors={'centerx': 'centerx',
                                                     'top': 'top'})

        # Game Mode Board image
        gamemodeImage = pygame.image.load("../Assets/WindowElements/GameModeBoard.png")
        gamemodeRect = pygame.Rect((0, 0), (855, 294))
        gamemode = pygame_gui.elements.UIImage(relative_rect=gamemodeRect,
                                            image_surface=gamemodeImage,
                                            manager=self.manager,
                                            container= background,
                                            anchors={'centerx': 'centerx',
                                                     'centery': 'centery'})

        # Conversion monthly button
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

        # Conversion all time button
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

        # Basic Calculation monthly button
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

        # Basic Calculation all time button
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

        # Mixed Calculation monthly button
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

        # Mixed Calculation all time button
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

        # Close button
        closeButtonRect = pygame.Rect((0, 0), (56, 56))
        closeButtonRect.topright = -50, 75
        self.closeButton = pygame_gui.elements.UIButton(relative_rect=closeButtonRect,
                                                       text="",
                                                       object_id=pygame_gui.core.ObjectID(
                                                           class_id="@gameModeSelectButton",
                                                           object_id="#closeButton"),
                                                       manager=self.manager,
                                                       anchors={'right': 'right',
                                                                'top': 'top'})

    def eventCheck(self, ev):
        """
        Check for events happening in this menu.
        :param ev: Pygame event variable.
        :return: None
        """
        match ev.type:
            case pygame_gui.UI_BUTTON_PRESSED:
                # print(ev.ui_element)
                match ev.ui_element:
                    case self.conversionMonthButton:
                        self.buttonClick.play()
                        self.screen("leaderboard;conversion;month")
                    case self.calculationMonthButton:
                        self.buttonClick.play()
                        self.screen("leaderboard;basic_calculation;month")
                    case self.mixedCalculationMonthButton:
                        self.buttonClick.play()
                        self.screen("leaderboard;mixed_calculation;month")
                    case self.conversionAllButton:
                        self.buttonClick.play()
                        self.screen("leaderboard;conversion;all")
                    case self.calculationAllButton:
                        self.buttonClick.play()
                        self.screen("leaderboard;basic_calculation;all")
                    case self.mixedCalculationAllButton:
                        self.buttonClick.play()
                        self.screen("leaderboard;mixed_calculation;all")
                    case self.closeButton:
                        self.buttonClick.play()
                        self.screen("gameMenu")

    def update(self, timeDelta):
        """
        Update the events.
        :param timeDelta: Time elapsed since last update.
        :return: None
        """
        self.manager.update(timeDelta)

    def draw(self):
        """
        Draw elements onto the game.
        :return: None
        """
        pass
