# Import modules
import json
import sys
import os
import pygame
import pygame_gui

# Allow parent directory to system paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from BackEnd.Settings import Settings
from BackEnd.LeaderboardManage import LeaderboardManage


class Leaderboard:
    """
    Handle leaderboard lists and setup the interface, including pagination function.
    """
    def __init__(self, screen, display, manager, music, gameMode, timeFrame):
        """
        Initialise the Leaderboard class and setup the interface.

        :param screen: The pygame screen surface for rendering.
        :param display: The display manager for the game.
        :param manager: The UI manager to handle UI elements.
        :param music: The music to be played in the leaderboard.
        :param gameMode: The current leaderboard's game mode displayed.
        :param timeFrame: The time frame for the leaderboard (monthly, all-time).
        """
        pygame.init()
        # Default
        self.screen = screen
        self.display = display
        self.manager = manager

        # Theme
        self.manager.get_theme().load_theme("../ThemeFile/Leaderboard.json")

        # Audio
        if music != "Fallen_Down":
            pygame.mixer.music.load("../Assets/Audio/Leaderboard-Undertale_Fallen_Down.ogg")
            pygame.mixer.music.play(-1, fade_ms=3000)

        sfxVolume = Settings().getKeyVariable("SFX")

        self.buttonClick = pygame.mixer.Sound("../Assets/Audio/ButtonClick.wav")
        self.buttonClick.set_volume(sfxVolume)

        # Leaderboard
        self.gameMode = gameMode
        self.timeFrame = timeFrame
        self.page = 1

        self.background = None

        self.rowData = None
        self.leaderboardRows = []

        self.homeButton = None
        self.backButton = None
        self.rightPageButton = None
        self.leftPageButton = None

        self.uiSetup()

    def uiSetup(self):
        """
        Setup the basic GUI for leaderboard pages.
        :return: None.
        """
        # Background
        self.display.fill(pygame.Color('#FFE0E3'))  # Flooding the bg with pink make the pic brighter
        self.display.blit(pygame.image.load("../Assets/Background/BackgroundBlur.png"), (0, 0))

        # Background image
        backgroundRect = pygame.Rect((0, 0), (948, 451))
        self.background = pygame_gui.elements.UIPanel(relative_rect=backgroundRect,
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
            container=self.background
        )

        # Title image
        titlename = self.gameMode + self.timeFrame
        titleImage = pygame.image.load(f"../Assets/WindowElements/{titlename}.png")
        titleRect = pygame.Rect((-5, 0), (331, 89))
        titleRect.top = 30
        title = pygame_gui.elements.UIImage(relative_rect=titleRect,
                                            image_surface=titleImage,
                                            manager=self.manager,
                                            anchors={'centerx': 'centerx',
                                                     'top': 'top'})

        # Rows
        Headings = ["Rank", "Player Name", "Time Taken", "Score"]
        LeaderboardRow(self.manager, self.background, Headings, 30, True)
        self.updateLeaderboard(self.background)

        # Home button
        homeButtonRect = pygame.Rect((0, 0), (56, 56))
        homeButtonRect.bottomleft = 150, -30
        self.homeButton = pygame_gui.elements.UIButton(relative_rect=homeButtonRect,
                                                       text="",
                                                       object_id=pygame_gui.core.ObjectID(
                                                           class_id="@gameModeSelectButton",
                                                           object_id="#homeButton"),
                                                       manager=self.manager,
                                                       anchors={'left': 'left',
                                                                'bottom': 'bottom'})

        # Back button
        backButtonRect = pygame.Rect((0, 0), (56, 56))
        backButtonRect.bottomleft = 70, -30
        self.backButton = pygame_gui.elements.UIButton(relative_rect=backButtonRect,
                                                       text="",
                                                       object_id=pygame_gui.core.ObjectID(
                                                           class_id="@gameModeSelectButton",
                                                           object_id="#backButton"),
                                                       manager=self.manager,
                                                       anchors={'left': 'left',
                                                                'bottom': 'bottom'})

        # Right Page button
        rightPageButtonRect = pygame.Rect((0, 0), (44, 78))
        rightPageButtonRect.right = -20
        self.rightPageButton = pygame_gui.elements.UIButton(relative_rect=rightPageButtonRect,
                                                       text="",
                                                       object_id=pygame_gui.core.ObjectID(
                                                           class_id="@gameModeSelectButton",
                                                           object_id="#rightPageButton"),
                                                       manager=self.manager,
                                                       anchors={'right': 'right',
                                                                'centery': 'centery'})

        # Left Page button
        leftPageButtonRect = pygame.Rect((0, 0), (44, 78))
        leftPageButtonRect.left = 20
        self.leftPageButton = pygame_gui.elements.UIButton(relative_rect=leftPageButtonRect,
                                                       text="",
                                                       object_id=pygame_gui.core.ObjectID(
                                                           class_id="@gameModeSelectButton",
                                                           object_id="#leftPageButton"),
                                                       manager=self.manager,
                                                       anchors={'left': 'left',
                                                                'centery': 'centery'})

    def updateLeaderboard(self, background):
        """
        Update leaderboard display with the current data.

        :param background: The background panel where leaderboard rows will be displayed.
        :return: None
        """
        # Clear existing leaderboard rows
        if self.leaderboardRows:
            for i in self.leaderboardRows:
                i.killAll()
            self.leaderboardRows.clear()

        # Create a horizontal line for separation
        lineRect = pygame.Rect((0, 0), (930, 3))
        lineRect.top = 80
        line = pygame_gui.elements.UIPanel(relative_rect=lineRect,
                                           manager=self.manager,
                                           starting_height=0,
                                           object_id=pygame_gui.core.ObjectID(
                                               class_id="@line",
                                               object_id="#line"),
                                           container=background,
                                           anchors={'centerx': 'centerx',
                                                    'top': 'top'})

        # Retrieve leaderboard data
        try:
            leaderboard = LeaderboardManage()
            if self.timeFrame == "month":
                self.rowData = leaderboard.retrieveLeaderboard(self.gameMode, self.page, True)
            else:
                self.rowData = leaderboard.retrieveLeaderboard(self.gameMode, self.page)
        except:
            self.screen("error;Database Error Occurred:;Please contact Admin to resolve the matter.")

        # Fill leaderbord rows with data
        initialY = 80
        stackY = 60
        times = -1
        for i in self.rowData:
            times += 1
            row = LeaderboardRow(self.manager, background, i, initialY + (stackY * times))
            self.leaderboardRows.append(row)

    def eventCheck(self, ev):
        """
        Check for event happening in leaderboar list.
        :param ev: Pygame event variable.
        :return: None
        """
        match ev.type:
            case pygame_gui.UI_BUTTON_PRESSED:
                # print(ev.ui_element)
                match ev.ui_element:
                    case self.homeButton:
                        self.buttonClick.play()
                        self.screen("gameMenu")
                    case self.backButton:
                        self.buttonClick.play()
                        self.screen("leaderboardSelectMenu")
                    case self.leftPageButton:
                        self.buttonClick.play()
                        if self.page > 1:
                            self.page -= 1
                        self.updateLeaderboard(self.background)
                    case self.rightPageButton:
                        self.buttonClick.play()
                        if 5 < len(self.rowData):
                            self.page += 1
                        self.updateLeaderboard(self.background)
                        

    def update(self, timeDelta):
        """
        Update the events.
        :param timeDelta: Time elapsed since last update.
        :return: None
        """
        self.manager.update(timeDelta)

    def draw(self):
        """
        Draw elements onto the game.
        :return: None
        """
        pass


class LeaderboardRow:
    """
    Handle leaderboard row displays with different data.
    """
    def __init__(self, manager, container, data, y, title=False):
        """
        Initialise a row in the leaderboard with player data.

        :param manager: The UI manager to handle UI elements.
        :param container: The container of the leaderboard row.
        :param data: The data for the leaderboard row (rank, player name, time taken, score).
        :param y: The y position of the row.
        :param title: A boolean indicating if this row is a title.
        :return: None.
        """
        self.manager = manager
        self.container = container
        self.data = data
        self.y = y
        self.title = title

        self.elements = []

        self.uiSetup()

    def uiSetup(self):
        """
        Setup the basic GUI for the leaderboard rows.
        :return: None
        """
        # Load user data
        file = open("../loggedInUser.json", "r")
        data = json.load(file)
        file.close()

        y = 62 # Height for each row

        # Set the panel and font class based on if it is a title row or the current user
        if self.title:
            panelClass = "@regularPanel"
            fontClass = "@titleFont"
            shiftRightRank = 0
            shiftRightNeuro = 0
        elif data["username"] == self.data[1]:
            panelClass = "@youPanel"
            fontClass = "@youFont"
            shiftRightRank = 10
            shiftRightNeuro = 60
        else:
            panelClass = "@regularPanel"
            fontClass = "@regularFont"
            shiftRightRank = 10
            shiftRightNeuro = 0

        # Create background panel
        backgroundRect = pygame.Rect((0, 0), (930, y))
        backgroundRect.top = self.y
        background = pygame_gui.elements.UIPanel(relative_rect=backgroundRect,
                                                 manager=self.manager,
                                                 starting_height=1,
                                                 object_id=pygame_gui.core.ObjectID(
                                                     class_id=panelClass,
                                                     object_id="#panel"),
                                                 container=self.container,
                                                 anchors={'centerx': 'centerx',
                                                          'top': 'top'})
        self.elements.append(background)

        # Set rank ID based on the rank value (for different color display)
        match self.data[0]:
            case "1":
                rankID = "#1"
            case "2":
                rankID = "#2"
            case "3":
                rankID = "#3"
            case _:
                rankID = "#default"

        # Rank label
        rankRect = pygame.Rect((0, 0), (60, y))
        rankRect.left = 10 + shiftRightRank
        rank = pygame_gui.elements.UILabel(relative_rect=rankRect,
                                           text=self.data[0],
                                           manager=self.manager,
                                           object_id=pygame_gui.core.ObjectID(
                                               class_id=fontClass,
                                               object_id=rankID),
                                           container=background,
                                           anchors={
                                               'left': 'left',
                                               'centery': 'centery'})
        self.elements.append(rank)

        # Display character image if the current user is on the leaderboard
        if data["username"] == self.data[1]:
            neuroImage = pygame.image.load("../Assets/Character/LeaderboardSprite.png")
            neuroRect = pygame.Rect((0, 0), (60, 60))
            neuroRect.left = 95
            neuro = pygame_gui.elements.UIImage(relative_rect=neuroRect,
                                                image_surface=neuroImage,
                                                manager=self.manager,
                                                container=background,
                                                anchors={
                                                    'left': 'left',
                                                    'centery': 'centery'})
            self.elements.append(neuro)

        # Player name
        nameRect = pygame.Rect((0, 0), (400, y))
        nameRect.left = 100 + shiftRightNeuro
        name = pygame_gui.elements.UILabel(relative_rect=nameRect,
                                           text=self.data[1],
                                           manager=self.manager,
                                           object_id=pygame_gui.core.ObjectID(
                                               class_id=fontClass,
                                               object_id="#usernameLabel"),
                                           container=background,
                                           anchors={
                                               'left': 'left',
                                               'centery': 'centery'})
        self.elements.append(name)

        # Time taken
        timeRect = pygame.Rect((0, 0), (150, y))
        timeRect.left = 590
        time = pygame_gui.elements.UILabel(relative_rect=timeRect,
                                           text=self.data[2],
                                           manager=self.manager,
                                           object_id=pygame_gui.core.ObjectID(
                                               class_id=fontClass,
                                               object_id="#usertimeLabel"),
                                           container=background,
                                           anchors={
                                               'left': 'left',
                                               'centery': 'centery'})
        self.elements.append(name)

        # Score
        scoreRect = pygame.Rect((0, 0), (100, y))
        scoreRect.left = 810
        score = pygame_gui.elements.UILabel(relative_rect=scoreRect,
                                            text=self.data[3],
                                            manager=self.manager,
                                            object_id=pygame_gui.core.ObjectID(
                                                class_id=fontClass,
                                                object_id="#userscoreLabel"),
                                            container=background,
                                            anchors={
                                                'left': 'left',
                                                'centery': 'centery'})
        self.elements.append(score)

    def killAll(self):
        """
        Remove all elements on the screen.
        :return: None
        """
        for i in self.elements:
            i.kill()
