# Import modules
import sys
import os
import pygame
import pygame_gui

# Allow parent directory to system paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from BackEnd.Settings import Settings

class GameOverMenu:
    """
    Handle the game over menu, including player's score, time taken, highscore and buttons to retry or return to the main menu.
    """
    def __init__(self, screen, display, manager, music, score, timeTaken, highScore, gameMode):
        """
        Initialise the GameOverMenu class and setup the interface.

        :param screen: The pygame screen surface for rendering.
        :param display: The display manager for the game.
        :param manager: The UI manager to handle UI elements.
        :param music: The music to be played in the menu.
        :param score: The player's score from the game.
        :param timeTaken: The time taken to complete the game.
        :param highScore: The player's highest score in the game.
        :param gameMode: The current game mode.
        :return: None.
        """
        pygame.init()

        # Default
        self.screen = screen
        self.display = display
        self.manager = manager

        # Theme
        self.manager.get_theme().load_theme("../ThemeFile/GameOver.json")

        # Audio
        if music != "Determination":
            pygame.mixer.music.load("../Assets/Audio/Game-Undertale_Determination.ogg")
            pygame.mixer.music.play(-1, fade_ms=3000)

        sfxVolume = Settings().getKeyVariable("SFX")

        self.buttonClick = pygame.mixer.Sound("../Assets/Audio/ButtonClick.wav")
        self.buttonClick.set_volume(sfxVolume)

        # GameOver
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
        """
        Sets up the basic GUI for the game over menu.
        :return: None.
        """
        # Background
        self.display.fill(pygame.Color('#FFE0E3'))
        self.display.blit(pygame.image.load("../Assets/Background/BackgroundBlur.png"), (0, 0))

        # Character and ghost sprites
        death_blur = pygame.image.load("../Assets/Character/NeuroDeathBlur.png")
        ghost_blur = pygame.image.load("../Assets/Character/NeuroGhostBlur.png")
        death_rect = death_blur.get_rect()
        ghost_rect = ghost_blur.get_rect()
        death_rect.bottomright = (1020, 640)
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

        # Stats panel - fixed position
        statsRect = pygame.Rect((1080 // 2 - 275, 220), (600, 200))
        self.statsPanel = pygame_gui.elements.UIPanel(
            relative_rect=statsRect,
            manager=self.manager,
            starting_height=1,
            object_id="@statsPanel"
        )

        # Time Taken
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((50, 20), (250, 45)),
            text="Time Taken :  ",
            manager=self.manager,
            container=self.statsPanel,
            object_id="@statsLabel"
        )
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((300, 20), (250, 45)),
            text=self.timeTaken,
            manager=self.manager,
            container=self.statsPanel,
            object_id="@statsValue"
        )

        # Score
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((50, 85), (250, 45)),
            text="Score :  ",
            manager=self.manager,
            container=self.statsPanel,
            object_id="@statsLabel"
        )
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((300, 85), (250, 45)),
            text=str(self.score),
            manager=self.manager,
            container=self.statsPanel,
            object_id="@statsValue"
        )

        # High Score
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((50, 150), (250, 45)),
            text="High Score :  ",
            manager=self.manager,
            container=self.statsPanel,
            object_id="@statsLabel"
        )
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((300, 150), (250, 45)),
            text=str(self.highScore),
            manager=self.manager,
            container=self.statsPanel,
            object_id="@statsValue"
        )
    
        # Back button (left arrow)
        backButtonRect = pygame.Rect((0, 0), (56,56))
        backButtonRect.centerx = 1080//2 - 110
        backButtonRect.centery = 640 - 145
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
        retryButtonRect.centerx = 1080//2
        retryButtonRect.centery = 640 - 145
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
        homeButtonRect.centerx = 1080//2 + 110
        homeButtonRect.centery = 640 - 145
        self.homeButton = pygame_gui.elements.UIButton(
            relative_rect=homeButtonRect,
            text="",
            manager=self.manager,
            object_id=pygame_gui.core.ObjectID(
                class_id="@gameButtons",
                object_id="#homeButton")
        )

    def eventCheck(self, ev):
        """
        Check for event happened in this menu (button pressed).
        :param ev: Pygame event variable.
        :return: None.
        """
        match ev.type:
            case pygame_gui.UI_BUTTON_PRESSED:
                match ev.ui_element:
                    case self.retryButton:
                        self.buttonClick.play()
                        self.screen(f"game;{self.gameMode};none")
                    case self.homeButton:
                        self.buttonClick.play()
                        self.screen("gameMenu")
                    case self.backButton:
                        self.buttonClick.play()
                        self.screen("gameModeSelectMenu")

    def update(self, timeDelta):
        """
        Update the event in this menu.
        :param timeDelta: The time elapsed since last update.
        :return: None
        """
        self.manager.update(timeDelta)

    def draw(self):
        """
        Draw elements onto the game
        :return: None
        """
        pass
