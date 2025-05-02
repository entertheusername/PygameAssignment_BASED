# Import modules
import sys
import os
import pygame
import pygame_gui

# Allow parent directory to system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from BackEnd.Settings import Settings


class GameModeSelectMenu:
    """
    Handle game mode selection menu, allowing user to choose different game mode.
    """
    def __init__(self, screen, display, manager, music):
        """
        Initialise the GameModeSelectMenu class and setup the interface.

        :param screen: The pygame screen surface for rendering.
        :param display: The display manager for the game.
        :param manager: The UI manager to handle UI elements.
        :param music: The music to be played in the menu.
        :return: None.
        """
        pygame.init()

        # Default
        self.screen = screen
        self.display = display
        self.manager = manager

        # Theme
        self.manager.get_theme().load_theme("../ThemeFile/GameSelectMenu.json")

        # Audio
        if music != "Littleroot_Town":
            pygame.mixer.music.load("../Assets/Audio/GameMenuSong-Littleroot_Town.ogg")
            pygame.mixer.music.play(-1, fade_ms=3000)

        sfxVolume = Settings().getKeyVariable("SFX")

        self.buttonClick = pygame.mixer.Sound("../Assets/Audio/ButtonClick.wav")
        self.buttonClick.set_volume(sfxVolume)

        # GameModeSelect
        self.conversionButton = None
        self.calculationButton = None
        self.mixedCalculationButton = None
        self.closeButton = None

        self.uiSetup()

    def uiSetup(self):
        """
        Sets up the basic GUI interface for the menu.
        :return: None
        """
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
        Check for events happened in the menu (press button).
        :param ev: Pygame event variable.
        :return:
        """
        match ev.type:
            case pygame_gui.UI_BUTTON_PRESSED:
                # print(ev.ui_element)
                match ev.ui_element:
                    case self.conversionButton:
                        self.buttonClick.play()
                        self.screen("game;conversion;none")
                    case self.calculationButton:
                        self.buttonClick.play()
                        self.screen("game;basic_calculation;none")
                    case self.mixedCalculationButton:
                        self.buttonClick.play()
                        self.screen("game;mixed_calculation;none")
                    case self.closeButton:
                        self.buttonClick.play()
                        self.screen("gameMenu")

    def update(self, timeDelta):
        """
        Update the events.
        :param timeDelta: The time elapsed since last update.
        :return: None
        """
        self.manager.update(timeDelta)

    def draw(self):
        """
        Draw elements onto the screen.
        :return: None
        """
        pass
