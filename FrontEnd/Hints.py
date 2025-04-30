import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pygame
import pygame_gui
from BackEnd.Settings import Settings

class HintMenu:
    def __init__(self, pauseInstance, manager, display, gameMode):
        pygame.init()

        # Default
        self.pauseMenu = pauseInstance
        self.manager = manager
        self.display = display
        self.gameMode = gameMode

        # Theme
        self.manager.get_theme().load_theme("../ThemeFile/HintMenu.json")

        # Audio
        sfxVolume = Settings().getKeyVariable("SFX")

        self.buttonClick = pygame.mixer.Sound("../Assets/Audio/ButtonClick.wav")
        self.buttonClick.set_volume(sfxVolume)

        # Hint
        self.pageCount = 1

        annyTFHappy = pygame.image.load("../Assets/Character/AnnyTFHappy.png")
        annyTFSad = pygame.image.load("../Assets/Character/AnnyTFSad.png")
        annyTFTease = pygame.image.load("../Assets/Character/AnnyTFTease.png")
        self.annyTFList = [annyTFHappy, annyTFSad, annyTFTease]

        self.hintList = []
        match gameMode:
            case "conversion":
                for i in range(1, 6):
                    hint = pygame.image.load(f"../Assets/Hint/{gameMode}Hint_{i}.png")
                    self.hintList.append(hint)
                    self.annyTFExpressionList = [0, 2, 2, 1, 0]
            case "basic_calculation":
                for i in range(1, 7):
                    hint = pygame.image.load(f"../Assets/Hint/{gameMode}Hint_{i}.png")
                    self.hintList.append(hint)
                    self.annyTFExpressionList = [0, 0, 2, 1, 1, 2]
            case "mixed_calculation":
                hint = pygame.image.load(f"../Assets/Hint/{gameMode}Hint_{1}.png")
                self.hintList.append(hint)
                self.annyTFExpressionList = [0]

        self.cheatSheet = None
        self.leftPageButton = None
        self.rightPageButton = None
        self.closeButton = None

        self.elements = []

        self.uiSetup()

    def uiSetup(self):
        """

        :return:
        """
        # Background Img
        backgroundRect = pygame.Rect((0, 0), (948, 451))
        background = pygame_gui.elements.UIPanel(relative_rect=backgroundRect,
                                                      manager=self.manager,
                                                      starting_height=0,
                                                      object_id=pygame_gui.core.ObjectID(
                                                          class_id="@mainPanel",
                                                          object_id="#mainPanel"),
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

        self.elements.append(background)

        # title Img
        titleImage = pygame.image.load(f"../Assets/WindowElements/AnnysHintTitle.png")
        titleRect = pygame.Rect((-5, 0), (422, 89))
        titleRect.top = 30
        title = pygame_gui.elements.UIImage(relative_rect=titleRect,
                                            image_surface=titleImage,
                                            manager=self.manager,
                                            anchors={'centerx': 'centerx',
                                                     'top': 'top'})

        self.elements.append(title)

        # Cheat Sheet
        cheatSheetRect = pygame.Rect((0, 0), (800, 400))
        self.cheatSheet = pygame_gui.elements.UIImage(relative_rect=cheatSheetRect,
                                                      image_surface=self.hintList[self.pageCount - 1],
                                                      manager=self.manager,
                                                      container=background,
                                                      anchors={'centerx': 'centerx',
                                                               'centery': 'centery'})

        self.elements.append(self.cheatSheet)

        # Anny
        annyTFRect = pygame.Rect((0, 0), (192, 192))
        annyTFRect.bottomright = 0, 0
        self.annyTF = pygame_gui.elements.UIImage(relative_rect=annyTFRect,
                                                      image_surface=self.annyTFList[0],
                                                      manager=self.manager,
                                                      container=background,
                                                      anchors={'right': 'right',
                                                               'bottom': 'bottom'})

        self.elements.append(self.annyTF)

        # Right Page button
        rightPageButtonRect = pygame.Rect((0, 0), (44, 78))
        rightPageButtonRect.right = -20
        self.rightPageButton = pygame_gui.elements.UIButton(relative_rect=rightPageButtonRect,
                                                            text="",
                                                            object_id=pygame_gui.core.ObjectID(
                                                                class_id="@hintButton",
                                                                object_id="#rightPageButton"),
                                                            manager=self.manager,
                                                            container=background,
                                                            anchors={'right': 'right',
                                                                     'centery': 'centery'})

        self.elements.append(self.rightPageButton)

        # Left Page button
        leftPageButtonRect = pygame.Rect((0, 0), (44, 78))
        leftPageButtonRect.left = 20
        self.leftPageButton = pygame_gui.elements.UIButton(relative_rect=leftPageButtonRect,
                                                           text="",
                                                           object_id=pygame_gui.core.ObjectID(
                                                               class_id="@hintButton",
                                                               object_id="#leftPageButton"),
                                                           manager=self.manager,
                                                           container=background,
                                                           anchors={'left': 'left',
                                                                    'centery': 'centery'})

        self.elements.append(self.leftPageButton)

        # Close button
        closeButtonRect = pygame.Rect((0, 0), (56, 56))
        closeButtonRect.topright = -50, 75
        self.closeButton = pygame_gui.elements.UIButton(relative_rect=closeButtonRect,
                                                        text="",
                                                        object_id=pygame_gui.core.ObjectID(
                                                            class_id="@hintButton",
                                                            object_id="#closeButton"),
                                                        manager=self.manager,
                                                        anchors={'right': 'right',
                                                                 'top': 'top'})

        self.elements.append(self.closeButton)

    def killAll(self):
        """

        :return:
        """
        for i in self.elements:
            i.kill()

    def eventCheck(self, ev):
        """

        :param ev:
        :return:
        """
        match ev.type:
            case pygame_gui.UI_BUTTON_PRESSED:
                # print(ev.ui_element)
                match ev.ui_element:
                    case self.leftPageButton:
                        self.buttonClick.play()
                        if self.pageCount > 1:
                            self.pageCount -= 1
                            self.updateHintContent()
                    case self.rightPageButton:
                        self.buttonClick.play()
                        if self.pageCount < len(self.hintList):
                            self.pageCount += 1
                            self.updateHintContent()
                    case self.closeButton:
                        self.buttonClick.play()
                        self.killAll()
                        self.pauseMenu.showAll()
                        self.pauseMenu.hintMenu = None

    def updateHintContent(self):
        """

        :return:
        """
        self.cheatSheet.set_image(self.hintList[self.pageCount - 1])
        self.annyTF.set_image(self.annyTFList[self.annyTFExpressionList[self.pageCount - 1]])

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
        self.display.fill(pygame.Color('#FFE0E3'))
        self.display.blit(pygame.image.load("../Assets/Background/BackgroundBlur.png"), (0, 0))