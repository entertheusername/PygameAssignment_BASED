# Import modules
import sys
import os
import pygame
import pygame_gui

# Allow parent directory to system paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from BackEnd.Authentication import Authentication
from BackEnd.Settings import Settings

class LoginMenu:
    """
    Handle the login menu for user credentials and secure login function.
    """
    def __init__(self, screen, display, manager, music):
        """
        Initialise the LoginMenu class and setup the interface.

        :param screen: The pygame screen surface for rendering.
        :param display: The display manager for the game.
        :param manager: The UI manager to handle UI elements.
        :param music: The music to be played in the login menu.
        return: None
        """
        pygame.init()

        # Default
        self.screen = screen
        self.display = display
        self.manager = manager

        # Theme
        self.manager.get_theme().load_theme("../ThemeFile/LoginRegisterMenu.json")

        # Audio
        if music != "":
            pygame.mixer.music.stop()

        sfxVolume = Settings().getKeyVariable("SFX")

        self.buttonClick = pygame.mixer.Sound("../Assets/Audio/ButtonClick.wav")
        self.buttonClick.set_volume(sfxVolume)

        # Login
        self.usernameInput = None
        self.passwordInput = None

        self.usernameError = None
        self.passwordError = None

        self.loginButton = None

        self.uiSetup()

    def uiSetup(self):
        """
        Setup the basic GUI in the login menu.
        :return: None
        """
        # Background
        self.display.fill(pygame.Color('#FFE0E3'))

        # MainMenu Panel
        mainMenu = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0, 0), (750, 400)),
                                               manager=self.manager,
                                               anchors={'center': 'center'})

        # Logo Img
        logoImage = pygame.image.load("../Assets/Logo.png")
        logoRect = pygame.Rect((-5, 0), (363, 138))
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
        textLineLabelRect = pygame.Rect((0, 0), (260, 60))
        textLineInputRect = pygame.Rect((0, 0), (340, 40))
        textLineErrorRect = pygame.Rect((0, 0), (340, 30))

        initialYLabel = 40
        initialYInput = 50
        initialYError = 85
        stackY = 70

        # Username Label & Input
        usernameLabelRect = textLineLabelRect
        usernameLabelRect.topleft = (0, initialYLabel)
        usernameLabel = pygame_gui.elements.UILabel(relative_rect=usernameLabelRect,
                                                    text="USERNAME:",
                                                    manager=self.manager,
                                                    object_id=pygame_gui.core.ObjectID(
                                                        class_id="@mainLabel",
                                                        object_id="#usernameLabel"),
                                                    container=mainMenu,
                                                    anchors={
                                                        'left': 'left',
                                                        'top': 'top'})

        usernameInputRect = textLineInputRect
        usernameInputRect.topright = (-90, initialYInput)
        self.usernameInput = pygame_gui.elements.UITextEntryLine(relative_rect=usernameInputRect,
                                                                 manager=self.manager,
                                                                 object_id=pygame_gui.core.ObjectID(
                                                                     class_id="@mainTextEntryLine",
                                                                     object_id="#usernameInput"),
                                                                 container=mainMenu,
                                                                 anchors={
                                                                     'right': 'right',
                                                                     'top': 'top'})

        usernameErrorRect = textLineErrorRect
        usernameErrorRect.topleft = (270, initialYError)
        self.usernameError = pygame_gui.elements.UILabel(relative_rect=usernameErrorRect,
                                                         text="",
                                                         manager=self.manager,
                                                         object_id=pygame_gui.core.ObjectID(
                                                             class_id="@mainError",
                                                             object_id="#usernameError"),
                                                         container=mainMenu,
                                                         anchors={
                                                             'left': 'left',
                                                             'top': 'top'})

        # Password Label & Input
        passwordLabelRect = textLineLabelRect
        passwordLabelRect.topleft = (0, initialYLabel + stackY)
        passwordLabel = pygame_gui.elements.UILabel(relative_rect=passwordLabelRect,
                                                    text="PASSWORD:",
                                                    manager=self.manager,
                                                    object_id=pygame_gui.core.ObjectID(
                                                        class_id="@mainLabel",
                                                        object_id="#passwordLabel"),
                                                    container=mainMenu,
                                                    anchors={
                                                        'left': 'left',
                                                        'top': 'top'})

        passwordInputRect = textLineInputRect
        passwordInputRect.topright = (-90, initialYInput + stackY)
        self.passwordInput = pygame_gui.elements.UITextEntryLine(relative_rect=passwordInputRect,
                                                                 manager=self.manager,
                                                                 object_id=pygame_gui.core.ObjectID(
                                                                     class_id="@mainTextEntryLinePassword",
                                                                     object_id="#passwordInput"),
                                                                 container=mainMenu,
                                                                 anchors={
                                                                     'right': 'right',
                                                                     'top': 'top'})

        passwordErrorRect = textLineErrorRect
        passwordErrorRect.topleft = (270, initialYError + stackY)
        self.passwordError = pygame_gui.elements.UILabel(relative_rect=passwordErrorRect,
                                                         text="",
                                                         manager=self.manager,
                                                         object_id=pygame_gui.core.ObjectID(
                                                             class_id="@mainError",
                                                             object_id="#passwordError"),
                                                         container=mainMenu,
                                                         anchors={
                                                             'left': 'left',
                                                             'top': 'top'})

        # Login Link
        loginLinkRect = pygame.Rect((0, 0), (350, 40))
        loginLinkRect.bottomleft = 40, -30
        loginLink = pygame_gui.elements.UITextBox(relative_rect=loginLinkRect,
                                                  html_text="<font face='pixeltype' pixel_size=25>"
                                                            "Don't have an account? Register "
                                                            "<a href='toLogin'>here!</a>"
                                                            "</font>",
                                                  wrap_to_height=True,
                                                  manager=self.manager,
                                                  object_id=pygame_gui.core.ObjectID(
                                                      class_id="@UITextBox",
                                                      object_id="#loginLink"),
                                                  container=mainMenu,
                                                  anchors={'left': 'left',
                                                           'bottom': 'bottom'})

        # Login Button
        loginButtonRect = pygame.Rect((-30, 0), (226, 76))
        loginButtonRect.bottom = -80
        self.loginButton = pygame_gui.elements.UIButton(relative_rect=loginButtonRect,
                                                        text="",
                                                        manager=self.manager,
                                                        object_id=pygame_gui.core.ObjectID(
                                                            class_id="@mainButton",
                                                            object_id="#loginButton"),
                                                        container=mainMenu,
                                                        anchors={'centerx': 'centerx',
                                                                 'bottom': 'bottom'})

    def eventCheck(self, ev):
        """
        Check for events happening in this menu.
        :param ev: Pygame event variable.
        :return: None
        """
        match ev.type:
            case pygame_gui.UI_BUTTON_PRESSED:
                # print(ev.ui_element)
                match ev.ui_element:
                    case self.loginButton:
                        self.buttonClick.play()
                        self.usernameError.set_text("")
                        self.passwordError.set_text("")
                        # try:
                        auth = Authentication()
                        status = auth.login(self.usernameInput.get_text(), self.passwordInput.get_text(), True)

                        if status["banned"] == True:
                            self.screen("error;Banned!:;Please contact Admin to resolve the matter.")
                            return

                        match status["loginMsg"]:
                            case "User does not exist.":
                                self.usernameError.set_text(status["loginMsg"])
                            case "Invalid password.":
                                self.passwordError.set_text(status["loginMsg"])
                            case "Login successful!":
                                self.screen("gameMenu")

                        # except:
                        #     self.screen("error;Database Error Occurred:;Please contact Admin to resolve the matter.")

            case pygame_gui.UI_TEXT_BOX_LINK_CLICKED:
                self.screen("registerMenu")

    def update(self, timeDelta):
        """
        Update the events.
        :param timeDelta: The time elapsed since last update.
        :return: None
        """
        self.manager.update(timeDelta)

    def draw(self):
        """
        Draw elements onto the game.
        :return: None
        """
        pass
