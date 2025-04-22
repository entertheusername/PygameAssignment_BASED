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
        self.arrowImage = pygame.image.load("../Assets/WindowElements/ArrowTutorial.png")

        self.cheatSheetConversion = pygame.image.load("../Assets/Background/BackgroundTutorial.png")
        self.cheatSheetBasicCalculation = pygame.image.load("../Assets/Background/BackgroundClear.png")
        self.cheatSheetMixedCalculation = pygame.image.load("../Assets/Background/BackgroundBlur.png")

        self.annyTFHappy = pygame.image.load("../Assets/Character/AnnyTFHappy.png")
        self.annyTFSad = pygame.image.load("../Assets/Character/AnnyTFSad.png")
        self.annyTFTease = pygame.image.load("../Assets/Character/AnnyTFTease.png")

        self.buttonClick = pygame.mixer.Sound("../Assets/Audio/ButtonClick.wav")

        file = open("../tutorial.json", "r")
        self.dialogs = json.load(file)
        file.close()

        self.page = 1
        self.dialog = self.dialogs[self.stage][str(self.page)]
        self.wordCount = 1
        self.currentDialog = ""

        self.dialogBox = None
        self.cheatSheet = None
        self.annyTF = None
        self.nextButton = None

        self.uiSetup()

    def uiSetup(self):
        # Background
        self.display.fill(pygame.Color('#FFE0E3'))  # Flooding the bg with pink make the pic brighter
        self.display.blit(pygame.image.load("../Assets/Background/BackgroundTutorial.png"), (0, 0))

        # Background Img
        backgroundRect = pygame.Rect((0, 150), (1080, 100))
        background = pygame_gui.elements.UIPanel(relative_rect=backgroundRect,
                                                 manager=self.manager,
                                                 starting_height=0,
                                                 anchors={'centerx': 'centerx',
                                                          'centery': 'centery'})

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

        # Game Assets
        # Add the pause button img ltr

        # Cheat sheets
        # Conversion Img
        cheatSheetRect = pygame.Rect((-50, 0), (800, 400))
        cheatSheetRect.top = 10
        self.cheatSheet = pygame_gui.elements.UIImage(relative_rect=cheatSheetRect,
                                                 image_surface=self.cheatSheetConversion,
                                                 manager=self.manager,
                                                 visible=False,
                                                 anchors={'centerx': 'centerx',
                                                          'top': 'top'})

        # Anny
        annyTFRect = pygame.Rect((0, 0), (192, 192))
        annyTFRect.bottomright = -10, -110
        self.annyTF = pygame_gui.elements.UIImage(relative_rect=annyTFRect,
                                                      image_surface=self.annyTFHappy,
                                                      manager=self.manager,
                                                      anchors={'right': 'right',
                                                               'bottom': 'bottom'})

        annyTag = pygame.image.load("../Assets/Character/AnnyTFTag.png")
        annyTagRect = pygame.Rect((0, 0), (155, 78))
        annyTagRect.bottomright = -28, -60
        self.annyTag = pygame_gui.elements.UIImage(relative_rect=annyTagRect,
                                                  image_surface=annyTag,
                                                  manager=self.manager,
                                                  anchors={'right': 'right',
                                                           'bottom': 'bottom'})

        # Next button
        nextButtonRect = pygame.Rect((0, 0), (150, 56))
        nextButtonRect.bottomright = -30, -30
        self.nextButton = pygame_gui.elements.UIButton(relative_rect=nextButtonRect,
                                                       text="NEXT >",
                                                       object_id=pygame_gui.core.ObjectID(
                                                           class_id="@tutorialButton",
                                                           object_id="#nextButton"),
                                                       manager=self.manager,
                                                       anchors={'right': 'right',
                                                                'bottom': 'bottom'})

    def eventCheck(self, ev):
        match ev.type:
            case pygame.MOUSEBUTTONDOWN:
                match ev.button:
                    case 1:
                        match self.stage:
                            case "1":
                                match self.page:
                                    case 1:
                                        self.updateArrow(True, 600, 580, 180)
                                    case 3:
                                        self.updateArrow(True, 540, 150, 270)
                                    case 4:
                                        self.updateArrow(True, 550, 150, 180)
                                    case 5:
                                        self.updateArrow(True, 850, 100, 215)
                                    case 6:
                                        self.updateArrow(False)
                                    case 7:
                                        self.annyTF.set_image(self.annyTFSad)
                                        self.annyTF.rebuild()
                                    case 8:
                                        self.cheatSheet.visible = True
                                        self.cheatSheet.rebuild()

                                        self.annyTF.set_image(self.annyTFHappy)
                                        self.annyTF.rebuild()
                                    case 9:
                                        self.cheatSheet.visible = False
                                        self.cheatSheet.rebuild()

                                        self.annyTF.set_image(self.annyTFTease)
                                        self.annyTF.rebuild()
                                if self.page > 9:
                                    self.screen("tutorialEngine;conversion;None")
                                else:
                                    self.updateDialog()
                            case "2":
                                match self.page:
                                    case 1:
                                        self.cheatSheet.set_image(self.cheatSheetBasicCalculation)
                                        self.cheatSheet.visible = True
                                        self.cheatSheet.rebuild()
                                    case 2:
                                        self.cheatSheet.visible = False
                                        self.cheatSheet.rebuild()

                                        self.annyTF.set_image(self.annyTFTease)
                                        self.annyTF.rebuild()
                                if self.page > 2:
                                    self.screen("tutorialEngine;basic_calculation;None")
                                else:
                                    self.updateDialog()
                            case "3":
                                match self.page:
                                    case 1:
                                        self.cheatSheet.set_image(self.cheatSheetMixedCalculation)
                                        self.cheatSheet.visible = True
                                        self.cheatSheet.rebuild()
                                    case 2:
                                        self.cheatSheet.visible = False
                                        self.cheatSheet.rebuild()

                                        self.annyTF.set_image(self.annyTFTease)
                                        self.annyTF.rebuild()
                                if self.page > 2:
                                    self.screen("tutorialEngine;mixed_calculation;None")
                                else:
                                    self.updateDialog()
                            case "4":
                                match self.page:
                                    case 1:
                                        self.updateArrow(True, 150, 100, 315)

                                        self.annyTF.set_image(self.annyTFTease)
                                        self.annyTF.rebuild()
                                    case 2:
                                        self.updateArrow(False)

                                        self.annyTF.set_image(self.annyTFHappy)
                                        self.annyTF.rebuild()
                                    case 3:
                                        self.annyTF.set_image(self.annyTFSad)
                                        self.annyTF.rebuild()
                                if self.page > 3:
                                    try:
                                        tutorialManage = TutorialManage()
                                        tutorialManage.updateTutorial()
                                        self.screen("gameMenu")
                                    except:
                                        self.screen(
                                            "error;Database Error Occurred:;Please contact Admin to resolve the matter.")
                                else:
                                    self.updateDialog()
            #Fake button is intentional design
            case pygame_gui.UI_BUTTON_PRESSED:
                self.buttonClick.play()

    def updateDialog(self):
        self.page += 1
        self.dialog = self.dialogs[self.stage][str(self.page)]
        self.wordCount = 1
        self.currentDialog = ""

    def updateArrow(self, blit=True, x=0, y=0, degree=0):
        self.display.fill(pygame.Color('#FFE0E3'))  # Flooding the bg with pink make the pic brighter
        self.display.blit(pygame.image.load("../Assets/Background/BackgroundTutorial.png"), (0, 0))
        if blit:
            arrowRotateImage = pygame.transform.rotate(self.arrowImage, degree)
            arrowRect = arrowRotateImage.get_rect(center=(x, y))
            self.display.blit(arrowRotateImage, arrowRect)

    def update(self, timeDelta):
        self.manager.update(timeDelta)

        if self.wordCount <= len(self.dialog):
            self.wordCount += 1
            self.currentDialog = self.dialog[:self.wordCount]
            self.dialogBox.set_text(self.currentDialog)

    def draw(self):
        pass
