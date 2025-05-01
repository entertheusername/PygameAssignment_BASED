# Import modules
import sys
import os
import pygame
import pygame_gui

# Allow parent directory to system paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from BackEnd.Settings import Settings
from FrontEnd.Hints import HintMenu

class PauseMenu:
    def __init__(self, gameInstance, display, manager, gameMode):
        pygame.init()
        self.game = gameInstance
        self.display = display
        self.manager = manager
        self.gameMode = gameMode

        # Theme
        self.manager.get_theme().load_theme("../ThemeFile/PauseMenu.json")

        # Audio
        sfxVolume = Settings().getKeyVariable("SFX")

        self.buttonClick = pygame.mixer.Sound("../Assets/Audio/ButtonClick.wav")
        self.buttonClick.set_volume(sfxVolume)

        # PauseMenu
        self.hintMenu = None

        self.resumeButton = None
        self.hintButton = None
        self.quitButton = None

        self.elements = []

        self.uiSetup()

    def uiSetup(self):
        """

        :return:
        """
        initialYElement = 100
        stackY = 90

        # Pause Icon
        pauseIcon = pygame.image.load("../Assets/WindowElements/PauseIcon.png")
        iconRect = pygame.Rect((-5, 0), (99, 109))
        iconRect.top = initialYElement
        icon = pygame_gui.elements.UIImage(relative_rect=iconRect,
                                           image_surface=pauseIcon,
                                           manager=self.manager,
                                           anchors={'centerx': 'centerx',
                                                    'top': 'top'})
        self.elements.append(icon)

        # Resume button
        resumeButtonRect = pygame.Rect((0, 0), (360, 63))
        resumeButtonRect.top = initialYElement + (stackY * 2)
        self.resumeButton = pygame_gui.elements.UIButton(relative_rect=resumeButtonRect,
                                                       text="",
                                                       manager=self.manager,
                                                       object_id=pygame_gui.core.ObjectID(
                                                           class_id="@gameButton",
                                                           object_id="#resumeButton"),
                                                       anchors={'centerx': 'centerx',
                                                                'top': 'top'})
        self.elements.append(self.resumeButton)

        # Hint button
        hintButtonRect = pygame.Rect((0, 0), (360, 63))
        hintButtonRect.top = initialYElement + (stackY * 3)
        self.hintButton = pygame_gui.elements.UIButton(relative_rect=hintButtonRect,
                                                              text="",
                                                              manager=self.manager,
                                                              object_id=pygame_gui.core.ObjectID(
                                                                  class_id="@gameButton",
                                                                  object_id="#hintButton"),
                                                              anchors={'centerx': 'centerx',
                                                                       'top': 'top'})
        self.elements.append(self.hintButton)

        # Quit button
        quitButtonRect = pygame.Rect((0, 0), (360, 63))
        quitButtonRect.top = initialYElement + (stackY * 4)
        self.quitButton = pygame_gui.elements.UIButton(relative_rect=quitButtonRect,
                                                       text="",
                                                       manager=self.manager,
                                                       object_id=pygame_gui.core.ObjectID(
                                                           class_id="@gameButton",
                                                           object_id="#quitButton"),
                                                       anchors={'centerx': 'centerx',
                                                                'top': 'top'})
        self.elements.append(self.quitButton)

    def killAll(self):
        """

        :return:
        """
        for i in self.elements:
            i.kill()

    def hideAll(self):
        """

        :return:
        """
        for i in self.elements:
            i.hide()

    def showAll(self):
        """

        :return:
        """
        for i in self.elements:
            i.show()

    def eventCheck(self, ev):
        """

        :param ev:
        :return:
        """

        if self.game.paused and self.hintMenu:
            self.hintMenu.eventCheck(ev)
            return

        match ev.type:
            case pygame_gui.UI_BUTTON_PRESSED:
                match ev.ui_element:
                    case self.resumeButton:
                        self.buttonClick.play()
                        self.killAll()
                        self.game.pause_button.show()
                        self.game.paused = False 
                    case self.hintButton:
                        self.buttonClick.play()
                        self.hintMenu = HintMenu(self, self.manager, self.display, self.gameMode)
                        self.hideAll()
                    case self.quitButton:
                        self.buttonClick.play()
                        self.game.screen("gameModeSelectMenu")
            case pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    self.killAll()
                    self.game.pause_button.show()
                    self.game.paused = False

    def update(self, timeDelta):
        """

        :param timeDelta:
        :return:
        """
        self.manager.update(timeDelta)

    def draw(self):
        """

        :return:
        """
        if self.game.paused and self.hintMenu:
            self.hintMenu.draw()
        else:
            self.display.fill(pygame.Color('#FFE0E3'))
            self.display.blit(pygame.image.load("../Assets/Background/BackgroundBlur.png"), (0, 0))
            alive_blur = pygame.image.load("../Assets/Character/NeuroAliveBlur.png")
            alive_rect = alive_blur.get_rect()
            alive_rect.bottomright = (1020, 640)
            self.display.blit(alive_blur, alive_rect)
