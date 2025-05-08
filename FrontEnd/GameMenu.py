# Import modules
import sys
import os
import pygame
import pygame_gui

# Allow parent directory to system paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from BackEnd.Settings import Settings
from BackEnd.Authentication import Authentication
from BackEnd.TutorialManage import TutorialManage
from Popup import Popup


class GameMenu:
    """
    Handle game menu interface, including play button, leaderboard button, setting button and exit button.
    """
    def __init__(self, screen, display, manager, music, endGame):
        """
        Initialise the GameMenu class and setup the interface.

        :param screen: The pygame screen surface for rendering.
        :param display: The display manager for the game.
        :param manager: The UI manager to handle UI elements.
        :param music: The music to be played in the game menu.
        :param endGame: A function to call when exiting the game.
        :return: None
        """
        pygame.init()

        # Default
        self.screen = screen
        self.display = display
        self.manager = manager
        self.endGame = endGame
        try:
            tutorialManage = TutorialManage()
            self.tutorialStat = tutorialManage.checkTutorial()
        except:
            self.screen("error;Database Error Occurred:;Please contact Admin to resolve the matter.")

        # Theme
        self.manager.get_theme().load_theme("../ThemeFile/GameMenu.json")
        self.manager.get_theme().load_theme("../ThemeFile/Popup.json")

        # Audio
        if music != "Littleroot_Town":
            pygame.mixer.music.load("../Assets/Audio/GameMenuSong-Littleroot_Town.ogg")
            pygame.mixer.music.play(-1, fade_ms=3000)

        sfxVolume = Settings().getKeyVariable("SFX")

        self.buttonClick = pygame.mixer.Sound("../Assets/Audio/ButtonClick.wav")
        self.buttonClick.set_volume(sfxVolume)

        # GameMenu
        self.playButton = None
        self.leaderboardButton = None
        self.exitButton = None
        self.popup = None

        self.uiSetup()

    def uiSetup(self):
        """
        Setup basic GUI interface using pygame_gui.
        :return: None
        """
        # Background
        self.display.fill(pygame.Color('#FFE0E3'))  # Flooding the bg with pink make the pic brighter
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

        # Settings button
        settingsButtonRect = pygame.Rect((0, 0), (56, 56))
        settingsButtonRect.bottomleft = 30, -30
        self.settingsButton = pygame_gui.elements.UIButton(relative_rect=settingsButtonRect,
                                                       text="",
                                                       manager=self.manager,
                                                       object_id=pygame_gui.core.ObjectID(
                                                           class_id="@gameButton",
                                                           object_id="#settingsButton"),
                                                       anchors={'left': 'left',
                                                                'bottom': 'bottom'})
        
        # Play button
        playButtonRect = pygame.Rect((0, 0), (360, 70))
        playButtonRect.top = initialYElement + (stackY * 2)
        self.playButton = pygame_gui.elements.UIButton(relative_rect=playButtonRect,
                                                       text="",
                                                       manager=self.manager,
                                                       object_id=pygame_gui.core.ObjectID(
                                                           class_id="@gameButton",
                                                           object_id="#playButton"),
                                                       anchors={'centerx': 'centerx',
                                                                'top': 'top'})

        # Leaderboard button
        leaderboardButtonRect = pygame.Rect((0, 0), (360, 70))
        leaderboardButtonRect.top = initialYElement + (stackY * 3)
        self.leaderboardButton = pygame_gui.elements.UIButton(relative_rect=leaderboardButtonRect,
                                                              text="",
                                                              manager=self.manager,
                                                              object_id=pygame_gui.core.ObjectID(
                                                                  class_id="@gameButton",
                                                                  object_id="#leaderboardButton"),
                                                              anchors={'centerx': 'centerx',
                                                                       'top': 'top'})

        # Exit button
        exitButtonRect = pygame.Rect((0, 0), (360, 70))
        exitButtonRect.top = initialYElement + (stackY * 4)
        self.exitButton = pygame_gui.elements.UIButton(relative_rect=exitButtonRect,
                                                       text="",
                                                       manager=self.manager,
                                                       object_id=pygame_gui.core.ObjectID(
                                                           class_id="@gameButton",
                                                           object_id="#exitButton"),
                                                       anchors={'centerx': 'centerx',
                                                                'top': 'top'})

        if not self.tutorialStat:
            message = "Do you want to start the tutorial?"
            self.popup = Popup(self.manager, self.display, message, "YesNo", "Tutorial")
            self.disableAllElements()


    def eventCheck(self, ev):
        """
        Check any specific game events happened.
        :param ev: pygame event variable.
        :return: None
        """
        match ev.type:
            case pygame_gui.UI_BUTTON_PRESSED:
                print(ev.ui_element)
                match ev.ui_element:
                    case self.settingsButton:
                        self.buttonClick.play()
                        self.screen("settingMenu")
                    case self.playButton:
                        self.buttonClick.play()
                        self.screen("gameModeSelectMenu")
                    case self.leaderboardButton:
                        self.buttonClick.play()
                        self.screen("leaderboardSelectMenu")
                    case self.exitButton:
                        # need to change this to a popup function (exit or exit with logout)
                        self.buttonClick.play()
                        message = "Do you want logout and exit?"
                        self.popup = Popup(self.manager, self.display, message, "YesNo", "Logout")
                        self.disableAllElements()
                    case self.popup.yesButton:
                        self.buttonClick.play()
                        if self.popup.purpose == "Tutorial":
                            self.screen("tutorial;1;None")
                        else:
                            auth = Authentication()
                            auth.logout()
                            self.endGame()
                    case self.popup.noButton:
                        self.buttonClick.play()
                        if self.popup.purpose == "Tutorial":
                            self.popup.killAll()
                            self.enableAllElements()
                        else:
                            self.endGame()
                    case self.popup.closeButton:
                        self.buttonClick.play()
                        self.enableAllElements()

    def update(self, timeDelta):
        """
        Update game events.
        :param timeDelta: The time elapsed since last update.
        :return: None
        """
        self.manager.update(timeDelta)

    def disableAllElements(self):
        """
        Disable all the buttons on the page.
        :return: None
        """
        self.playButton.disable()
        self.leaderboardButton.disable()
        self.exitButton.disable()
        self.settingsButton.disable()

    def enableAllElements(self):
        """
        Enable all the buttons on the page.
        :return: None
        """
        self.playButton.enable()
        self.leaderboardButton.enable()
        self.exitButton.enable()
        self.settingsButton.enable()

    def draw(self):
        """
        Draw elements onto the game.
        :return: None
        """
        pass
