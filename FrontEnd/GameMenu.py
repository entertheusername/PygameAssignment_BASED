import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pygame
import pygame_gui
from BackEnd.Authentication import Authentication
from BackEnd.TutorialManage import TutorialManage
from Popup import Popup


class GameMenu:
    def __init__(self, screen, display, manager, endGame):
        pygame.init()
        self.screen = screen
        self.display = display
        self.manager = manager
        self.endGame = endGame
        try:
            tutorialManage = TutorialManage()
            self.tutorialStat = tutorialManage.checkTutorial()
        except:
            self.screen("error;Database Error Occurred:;Please contact Admin to resolve the matter.")

        self.manager.get_theme().load_theme("../ThemeFile/GameMenu.json")
        self.manager.get_theme().load_theme("../ThemeFile/Popup.json")

        self.playButton = None
        self.leaderboardButton = None
        self.exitButton = None
        self.popup = None

        self.uiSetup()

    def uiSetup(self):
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
        match ev.type:
            case pygame_gui.UI_BUTTON_PRESSED:
                print(ev.ui_element)
                match ev.ui_element:
                    case self.playButton:
                        self.screen("gameModeSelectMenu")
                    case self.leaderboardButton:
                        self.screen("leaderboardSelectMenu")
                    case self.exitButton:
                        # need to change this to a popup function (exit or exit with logout)
                        message = "Do you want logout and exit?"
                        self.popup = Popup(self.manager, self.display, message, "YesNo", "Logout")
                        self.disableAllElements()
                    case self.popup.yesButton:
                        if self.popup.purpose == "Tutorial":
                            self.screen("tutorial;1;None")
                        else:
                            auth = Authentication()
                            auth.logout()
                            self.endGame()
                    case self.popup.noButton:
                        if self.popup.purpose == "Tutorial":
                            self.popup.killAll()
                            self.enableAllElements()
                        else:
                            self.endGame()
                    case self.popup.closeButton:
                        self.enableAllElements()

    def update(self, timeDelta):
        self.manager.update(timeDelta)

    def disableAllElements(self):
        self.playButton.disable()
        self.leaderboardButton.disable()
        self.exitButton.disable()

    def enableAllElements(self):
        self.playButton.enable()
        self.leaderboardButton.enable()
        self.exitButton.enable()

    def draw(self):
        pass
