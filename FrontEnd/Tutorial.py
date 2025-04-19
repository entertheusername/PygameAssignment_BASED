import json
import sys
import os
import pygame
import pygame_gui
from BackEnd.TutorialManage import TutorialManage

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class Tutorial:
    def __init__(self, screen, display, manager, stage):
        pygame.init()

        self.screen = screen
        self.display = display
        self.manager = manager
        self.stage = stage

        self.manager.get_theme().load_theme("../ThemeFile/Tutorial.json")

        file = open("../tutorial.json", "r")
        self.dialogs = json.load(file)
        file.close()

        self.page = 1
        self.dialog = self.dialogs[self.stage][str(self.page)]
        self.wordCount = 1
        self.currentDialog = ""

        self.dialogBox = None
        self.nextButton = None

        self.uiSetup()

    def uiSetup(self):
        # Background
        self.display.fill(pygame.Color('#FFE0E3'))  # Flooding the bg with pink make the pic brighter
        self.display.blit(pygame.image.load("../Assets/Background/BackgroundBlur.png"), (0, 0))

        # Background Img
        backgroundRect = pygame.Rect((0, 0), (948, 451))
        background = pygame_gui.elements.UIPanel(relative_rect=backgroundRect,
                                                 manager=self.manager,
                                                 starting_height=0,
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

        # Diplay words
        dialogRect = pygame.Rect((0, 0), (900, 440))
        self.dialogBox = pygame_gui.elements.UITextBox(relative_rect=dialogRect,
                                             manager=self.manager,
                                                       starting_height=0,
                                             html_text=self.dialog[self.wordCount],
                                             object_id=pygame_gui.core.ObjectID(
                                                 class_id="@tutorialDialog",
                                                 object_id="#dialog"),
                                             container=background,
                                             anchors={'centerx': 'centerx',
                                                      'centery': 'centery'})

        # Back button
        nextButtonRect = pygame.Rect((0, 0), (56, 56))
        nextButtonRect.bottomright = -50, -75
        self.nextButton = pygame_gui.elements.UIButton(relative_rect=nextButtonRect,
                                                       text=">",
                                                       object_id=pygame_gui.core.ObjectID(
                                                           class_id="@tutorialButton",
                                                           object_id="#nextButton"),
                                                       container=background,
                                                       manager=self.manager,
                                                       anchors={'right': 'right',
                                                                'bottom': 'bottom'})

    def eventCheck(self, ev):
        match ev.type:
            case pygame_gui.UI_BUTTON_PRESSED:
                # print(ev.ui_element)
                match ev.ui_element:
                    case self.nextButton:
                        match self.stage:
                            case "1":
                                if self.page > 9:
                                    self.screen("tutorialEngine;conversion;None")
                                else:
                                    self.updateDialog()
                            case "2":
                                if self.page > 2:
                                    self.screen("tutorialEngine;basic_calculation;None")
                                else:
                                    self.updateDialog()
                            case "3":
                                if self.page > 2:
                                    self.screen("tutorialEngine;mixed_calculation;None")
                                else:
                                    self.updateDialog()
                            case "4":
                                if self.page > 3:
                                    try:
                                        tutorialManage = TutorialManage()
                                        tutorialManage.updateTutorial()
                                        self.screen("gameMenu")
                                    except:
                                        self.screen("error;Database Error Occurred:;Please contact Admin to resolve the matter.")
                                else:
                                    self.updateDialog()

    def updateDialog(self):
        self.page += 1
        self.dialog = self.dialogs[self.stage][str(self.page)]
        self.wordCount = 1
        self.currentDialog = ""

    def update(self, timeDelta):
        self.manager.update(timeDelta)

        if "</p>" in self.currentDialog:
            self.currentDialog = self.dialog[:len(self.dialog)]
            self.dialogBox.set_text(self.currentDialog)
        elif self.wordCount <= len(self.dialog) :
            self.wordCount += 1
            self.currentDialog = self.dialog[:self.wordCount]
            self.dialogBox.set_text(self.currentDialog)



    def draw(self):
        pass
