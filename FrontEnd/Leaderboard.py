import json
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pygame
import pygame_gui
from BackEnd.Settings import Settings
from BackEnd.LeaderboardManage import LeaderboardManage


class Leaderboard:
    def __init__(self, screen, display, manager, music, gameMode, timeFrame):
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

        :return:
        """
        # Background
        self.display.fill(pygame.Color('#FFE0E3'))  # Flooding the bg with pink make the pic brighter
        self.display.blit(pygame.image.load("../Assets/Background/BackgroundBlur.png"), (0, 0))

        # Background Img
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

        # title Img
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

        :param background:
        :return:
        """
        if self.leaderboardRows:
            for i in self.leaderboardRows:
                i.killAll()
            self.leaderboardRows.clear()

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

        try:
            leaderboard = LeaderboardManage()
            if self.timeFrame == "month":
                self.rowData = leaderboard.retrieveLeaderboard(self.gameMode, self.page, True)
            else:
                self.rowData = leaderboard.retrieveLeaderboard(self.gameMode, self.page)
        except:
            self.screen("error;Database Error Occurred:;Please contact Admin to resolve the matter.")

        initialY = 80
        stackY = 60
        times = -1
        for i in self.rowData:
            times += 1
            row = LeaderboardRow(self.manager, background, i, initialY + (stackY * times))
            self.leaderboardRows.append(row)

    def eventCheck(self, ev):
        """

        :param ev:
        :return:
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

        :param timeDelta:
        :return:
        """
        self.manager.update(timeDelta)

    def draw(self):
        """

        :return:
        """
        pass


class LeaderboardRow:
    def __init__(self, manager, container, data, y, title=False):
        self.manager = manager
        self.container = container
        self.data = data
        self.y = y
        self.title = title

        self.elements = []

        self.uiSetup()

    def uiSetup(self):
        """

        :return:
        """
        file = open("../loggedInUser.json", "r")
        data = json.load(file)
        file.close()

        y = 62

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

        match self.data[0]:
            case "1":
                rankID = "#1"
            case "2":
                rankID = "#2"
            case "3":
                rankID = "#3"
            case _:
                rankID = "#default"

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

        :return:
        """
        for i in self.elements:
            i.kill()

