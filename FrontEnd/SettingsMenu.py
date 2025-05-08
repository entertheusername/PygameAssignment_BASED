# Import modules
import sys
import os
import pygame
import pygame_gui

# Allow parent directory to system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from BackEnd.Settings import Settings

class SettingMenu:
    """
    Handle the setting menu and render its interface.
    """
    def __init__(self, screen, display, manager, music):
        """
        Initialise the SettingMenu class.
        :param screen: The pygame screen surface.
        :param display: The display surface for rendering.
        :param manager: The UI manager to handle UI elements.
        :param music: The music to be played in the menu.
        :return: None
        """
        pygame.init()

        # Default
        self.screen = screen
        self.display = display
        self.manager = manager

        # Theme
        self.manager.get_theme().load_theme("../ThemeFile/SettingMenu.json")

        # Audio
        if music != "":
            pygame.mixer.music.stop()

        sfxVolume = Settings().getKeyVariable("SFX")

        self.buttonClick = pygame.mixer.Sound("../Assets/Audio/ButtonClick.wav")
        self.buttonClick.set_volume(sfxVolume)
        self.testPlay = pygame.mixer.Sound("../Assets/Audio/TestPlay-Undertale_Spooktune.ogg")
        self.testPlay.set_volume(0)

        # Setting
        self.setting = Settings()
        self.musicInput = None
        self.playMusicButton = None
        self.sfxInput = None
        self.playSfxButton = None

        self.uiSetup()

    def uiSetup(self):
        """
        Setup basic GUI for the settings menu.
        :return: None.
        """
        # Background
        self.display.fill(pygame.Color('#FFE0E3'))  # Flooding the bg with pink make the pic brighter
        self.display.blit(pygame.image.load("../Assets/Background/BackgroundBlur.png"), (0, 0))

        # MainMenu Panel
        mainMenu = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0, 0), (750, 400)),
                                               manager=self.manager,
                                               anchors={'center': 'center'})

        # Logo Img
        logoImage = pygame.image.load("../Assets/Logo.png")
        logoRect = pygame.Rect((5, 0), (363, 138))
        logoRect.top = 80
        logo = pygame_gui.elements.UIImage(relative_rect=logoRect,
                                           image_surface=logoImage,
                                           manager=self.manager,
                                           anchors={'centerx': 'centerx',
                                                    'top': 'top'})

        # Character Img
        neuroImage = pygame.image.load("../Assets/Character/NeuroAlive.png")
        neuroRect = pygame.Rect((0, 0), (256, 256))
        neuroRect.bottomright = (-80, -90)
        neuro = pygame_gui.elements.UIImage(relative_rect=neuroRect,
                                            image_surface=neuroImage,
                                            manager=self.manager,
                                            anchors={'right': 'right',
                                                     'bottom': 'bottom'})

        # Tutel Img
        tutelImage = pygame.image.load("../Assets/Character/Tutel.png")
        tutelRect = pygame.Rect((0, 0), (120, 120))
        tutelRect.bottomright = (-180, -170)
        tutel = pygame_gui.elements.UIImage(relative_rect=tutelRect,
                                            image_surface=tutelImage,
                                            manager=self.manager,
                                            anchors={'right': 'right',
                                                     'bottom': 'bottom'})

        # Initial Form Setup
        textLineLabelRect = pygame.Rect((0, 0), (130, 60))
        textLineInputRect = pygame.Rect((-20, 0), (340, 40))
        buttonRect = pygame.Rect((-20, 0), (340, 40))

        initialYLabel = 40
        initialYInput = 50
        initialYButton = 40
        stackY = 70

        # Music Label & Slider
        musicLabelRect = textLineLabelRect
        musicLabelRect.topleft = (0, initialYLabel)
        musicLabel = pygame_gui.elements.UILabel(relative_rect=musicLabelRect,
                                                 text="MUSIC",
                                                 manager=self.manager,
                                                 object_id=pygame_gui.core.ObjectID(
                                                     class_id="@settingLabel",
                                                     object_id="#musicLabel"),
                                                 container=mainMenu,
                                                 anchors={
                                                     'left': 'left',
                                                     'top': 'top'})

        musicBarImage = pygame.image.load("../Assets/WindowElements/SettingSliderBar.png")
        musicBarRect = pygame.Rect((-20, 0), (330, 20))
        musicBarRect.top = 60
        musicBar = pygame_gui.elements.UIImage(relative_rect=musicBarRect,
                                               image_surface=musicBarImage,
                                               manager=self.manager,
                                               container=mainMenu,
                                               anchors={'centerx': 'centerx',
                                                        'top': 'top'})

        musicInputRect = textLineInputRect
        musicInputRect.top = initialYInput
        self.musicInput = pygame_gui.elements.UIHorizontalSlider(relative_rect=musicInputRect,
                                                                 manager=self.manager,
                                                                 start_value=self.setting.getKeyVariable("Music") * 100,
                                                                 value_range=(0, 100),
                                                                 object_id=pygame_gui.core.ObjectID(
                                                                     class_id="@settingSliders",
                                                                     object_id="#musicInput"),
                                                                 container=mainMenu,
                                                                 anchors={
                                                                     'centerx': 'centerx',
                                                                     'top': 'top'})

        playMusicButtonRect = pygame.Rect((0, 0), (68, 53))
        playMusicButtonRect.topright = -100, initialYButton
        self.playMusicButton = pygame_gui.elements.UIButton(relative_rect=playMusicButtonRect,
                                                            text="",
                                                            object_id=pygame_gui.core.ObjectID(
                                                                class_id="@settingSoundButton",
                                                                object_id="#playMusicButton"),
                                                            manager=self.manager,
                                                            container=mainMenu,
                                                            anchors={'right': 'right',
                                                                     'top': 'top'})

        # SFX Label & Input
        sfxLabelRect = textLineLabelRect
        sfxLabelRect.topleft = (0, initialYLabel + stackY)
        sfxLabel = pygame_gui.elements.UILabel(relative_rect=sfxLabelRect,
                                               text="SFX",
                                               manager=self.manager,
                                               object_id=pygame_gui.core.ObjectID(
                                                   class_id="@settingLabel",
                                                   object_id="#sfxLabel"),
                                               container=mainMenu,
                                               anchors={
                                                   'left': 'left',
                                                   'top': 'top'})

        sfxBarImage = pygame.image.load("../Assets/WindowElements/SettingSliderBar.png")
        sfxBarRect = pygame.Rect((-20, 0), (330, 20))
        sfxBarRect.top = 60 + stackY
        sfxBar = pygame_gui.elements.UIImage(relative_rect=sfxBarRect,
                                               image_surface=sfxBarImage,
                                               manager=self.manager,
                                               container=mainMenu,
                                               anchors={'centerx': 'centerx',
                                                        'top': 'top'})

        sfxInputRect = textLineInputRect
        sfxInputRect.top = initialYInput + stackY
        self.sfxInput = pygame_gui.elements.UIHorizontalSlider(relative_rect=sfxInputRect,
                                                               manager=self.manager,
                                                               start_value=self.setting.getKeyVariable("SFX") * 100,
                                                               value_range=(0, 100),
                                                               object_id=pygame_gui.core.ObjectID(
                                                                   class_id="settingSliders",
                                                                   object_id="#sfxInput"),
                                                               container=mainMenu,
                                                               anchors={
                                                                   'centerx': 'centerx',
                                                                   'top': 'top'})

        playSfxButtonRect = pygame.Rect((0, 0), (68, 53))
        playSfxButtonRect.topright = -100, initialYButton + stackY
        self.playSfxButton = pygame_gui.elements.UIButton(relative_rect=playSfxButtonRect,
                                                          text="",
                                                          object_id=pygame_gui.core.ObjectID(
                                                              class_id="@settingSoundButton",
                                                              object_id="#playSfxButton"),
                                                          manager=self.manager,
                                                          container=mainMenu,
                                                          anchors={'right': 'right',
                                                                   'top': 'top'})

        # Tutorial Button
        tutorialButtonRect = pygame.Rect((-20, 0), (359, 62))
        tutorialButtonRect.bottom = -80
        self.tutorialButton = pygame_gui.elements.UIButton(relative_rect=tutorialButtonRect,
                                                           text="",
                                                           manager=self.manager,
                                                           object_id=pygame_gui.core.ObjectID(
                                                               class_id="@settingButton",
                                                               object_id="#tutorialButton"),
                                                           container=mainMenu,
                                                           anchors={'centerx': 'centerx',
                                                                    'bottom': 'bottom'})

        # Close button
        closeButtonRect = pygame.Rect((0, 0), (56, 56))
        closeButtonRect.topright = -180, 125
        self.closeButton = pygame_gui.elements.UIButton(relative_rect=closeButtonRect,
                                                        text="",
                                                        object_id=pygame_gui.core.ObjectID(
                                                            class_id="@settingButton",
                                                            object_id="#closeButton"),
                                                        manager=self.manager,
                                                        anchors={'right': 'right',
                                                                 'top': 'top'})

    def eventCheck(self, ev):
        """
        Check for event happening in this menu.
        :param ev: Pygame event variable.
        :return: None.
        """
        match ev.type:
            case pygame_gui.UI_BUTTON_PRESSED:
                # print(ev.ui_element)
                match ev.ui_element:
                    case self.tutorialButton:
                        self.buttonClick.play()
                        self.screen("tutorial;1;None")
                    case self.closeButton:
                        self.buttonClick.play()
                        self.testPlay.stop()
                        self.screen("gameMenu")
                    case self.playMusicButton:
                        self.testPlay.stop()
                        self.testPlay.set_volume(self.musicInput.get_current_value() / 100)
                        self.testPlay.play()
                    case self.playSfxButton:
                        self.testPlay.stop()
                        self.testPlay.set_volume(self.sfxInput.get_current_value() / 100)
                        self.testPlay.play()
            case pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                match ev.ui_element:
                    case self.musicInput:
                        self.setting.setKeyVariable("Music", self.musicInput.get_current_value() / 100)
                        pygame.mixer.music.set_volume(self.musicInput.get_current_value() / 100)
                    case self.sfxInput:
                        self.setting.setKeyVariable("SFX", self.sfxInput.get_current_value() / 100)

    def update(self, timeDelta):
        """
        Update the events.
        :param timeDelta: The time elapsed since last update.
        :return: None.
        """
        self.manager.update(timeDelta)

    def draw(self):
        """
        Draw UI elements onto the game.
        :return: None.
        """
        pass
