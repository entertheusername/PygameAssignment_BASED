import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pygame
import pygame_gui
from BackEnd import Constants

class GameOverMenu:
    def __init__(self, screen, display, manager, score, timeTaken, highScore, gameMode):
        pygame.init()
        self.screen = screen
        self.display = display
        self.manager = manager

        self.manager.get_theme().load_theme("../ThemeFile/GameOver.json")

        self.score = score
        self.timeTaken = timeTaken
        self.highScore = highScore
        self.gameMode = gameMode

        self.background = None
        self.title = None
        self.statsPanel = None
        self.retryButton = None
        self.homeButton = None
        self.backButton = None

        self.uiSetup()

    def uiSetup(self):
        # Background
        self.display.fill(pygame.Color('#FFE0E3'))
        self.display.blit(pygame.image.load("../Assets/Background/BackgroundBlur.png"), (0, 0))

        # Character and ghost sprites
        death_blur = pygame.image.load("../Assets/Character/NeuroDeathBlur.png")
        ghost_blur = pygame.image.load("../Assets/Character/NeuroGhostBlur.png")
        death_rect = death_blur.get_rect()
        ghost_rect = ghost_blur.get_rect()
        death_rect.bottomright = (Constants.SCREEN_WIDTH - 60, Constants.SCREEN_HEIGHT)
        ghost_rect.centerx = death_rect.centerx - 60
        ghost_rect.bottom = death_rect.top + 100
        self.display.blit(death_blur, death_rect)
        self.display.blit(ghost_blur, ghost_rect)

        # Game Over title
        titleRect = pygame.Rect((0, 0), (450, 63))
        titleRect.top = 130
        self.title = pygame_gui.elements.UIImage(
            relative_rect=titleRect,
            image_surface=pygame.image.load("../Assets/WindowElements/GameOver.png"),
            manager=self.manager,
            object_id=pygame_gui.core.ObjectID(
                class_id="@gameOverTitle",
                object_id="#titleImage"),
            anchors={'centerx': 'centerx',
                     'top': 'top'}
        )

        # Stats panel - transparent panel for text
        statsRect = pygame.Rect((0, 0), (600, 200))
        statsRect.top = 230
        self.statsPanel = pygame_gui.elements.UIPanel(
            relative_rect=statsRect,
            manager=self.manager,
            starting_height=1,
            object_id=pygame_gui.core.ObjectID(
                class_id="@statsPanel",
                object_id="#statsPanel"),
            anchors={'centerx': 'centerx',
                     'top': 'top'}
        )

        # Time label
        timeLabelRect = pygame.Rect((0, 20), (600, 40))
        timeLabel = pygame_gui.elements.UILabel(
            relative_rect=timeLabelRect,
            text=f"Time Taken: {self.timeTaken}",
            manager=self.manager,
            container=self.statsPanel,
            object_id=pygame_gui.core.ObjectID(
                class_id="@statsFont",
                object_id="#timeLabel")
        )

        # Score label
        scoreLabelRect = pygame.Rect((0, 80), (600, 40))
        scoreLabel = pygame_gui.elements.UILabel(
            relative_rect=scoreLabelRect,
            text=f"Score: {self.score}",
            manager=self.manager,
            container=self.statsPanel,
            object_id=pygame_gui.core.ObjectID(
                class_id="@statsFont",
                object_id="#scoreLabel")
        )

        # High score label
        highScoreLabelRect = pygame.Rect((0, 140), (600, 40))
        highScoreLabel = pygame_gui.elements.UILabel(
            relative_rect=highScoreLabelRect,
            text=f"High Score: {self.highScore}",
            manager=self.manager,
            container=self.statsPanel,
            object_id=pygame_gui.core.ObjectID(
                class_id="@statsFont",
                object_id="#highScoreLabel")
        )
        
        # Back button (left arrow)
        backButtonRect = pygame.Rect((0, 0), (56,56))
        backButtonRect.centerx = Constants.SCREEN_WIDTH//2 - 110
        backButtonRect.centery = Constants.SCREEN_HEIGHT - 145
        self.backButton = pygame_gui.elements.UIButton(
            relative_rect=backButtonRect,
            text="",
            manager=self.manager,
            object_id=pygame_gui.core.ObjectID(
                class_id="@gameButtons",
                object_id="#backButton")
        )

        # Retry button (center circular arrow)
        retryButtonRect = pygame.Rect((0, 0), (90,90))
        retryButtonRect.centerx = Constants.SCREEN_WIDTH//2
        retryButtonRect.centery = Constants.SCREEN_HEIGHT - 145
        self.retryButton = pygame_gui.elements.UIButton(
            relative_rect=retryButtonRect,
            text="",
            manager=self.manager,
            object_id=pygame_gui.core.ObjectID(
                class_id="@gameButtons",
                object_id="#retryButton")
        )

        # Home button (right house icon)
        homeButtonRect = pygame.Rect((0, 0), (56,56))
        homeButtonRect.centerx = Constants.SCREEN_WIDTH//2 + 110
        homeButtonRect.centery = Constants.SCREEN_HEIGHT - 145
        self.homeButton = pygame_gui.elements.UIButton(
            relative_rect=homeButtonRect,
            text="",
            manager=self.manager,
            object_id=pygame_gui.core.ObjectID(
                class_id="@gameButtons",
                object_id="#homeButton")
        )

    def eventCheck(self, ev):
        match ev.type:
            case pygame_gui.UI_BUTTON_PRESSED:
                match ev.ui_element:
                    case self.retryButton:
                        self.screen(f"game;{self.gameMode};none")
                    case self.homeButton:
                        self.screen("gameMenu")
                    case self.backButton:
                        self.screen("gameModeSelectMenu")

    def update(self, timeDelta):
        self.manager.update(timeDelta)

    def draw(self):
        pass
