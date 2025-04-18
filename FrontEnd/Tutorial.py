import sys
import os
import pygame
import pygame_gui

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class Tutorial:
    def __init__(self, screen, display, manager, stage):
        pygame.init()

        self.screen = screen
        self.display = display
        self.manager = manager

        self.manager.get_theme().load_theme("../ThemeFile/LeaderboardSelectMenu.json")

        self.stage = stage
        self.page = 1

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
        dialogRect = pygame.Rect((0, 0), (500, 300))
        dialog = pygame_gui.elements.UILabel(relative_rect=dialogRect,
                                             manager=self.manager,
                                             text="test",
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
                                                       text="hi",
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
                        print(self.stage)
                        match self.stage:
                            case "1":
                                self.screen("tutorialEngine;conversion;None")
                            case "2":
                                self.screen("tutorialEngine;basic_calculation;None")
                            case "3":
                                self.screen("tutorialEngine;mixed_calculation;None")
                            case "4":
                                self.screen("gameMenu")

    def update(self, timeDelta):
        self.manager.update(timeDelta)

    def draw(self):
        pass
