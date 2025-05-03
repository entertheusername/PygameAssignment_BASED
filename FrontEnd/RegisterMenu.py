# Import modules
import sys
import os
import pygame
import pygame_gui

# Allow parent directory to system paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from BackEnd.Authentication import Authentication
from Popup import Popup
from BackEnd.Settings import Settings

class RegisterMenu:
    """
    Handle registration menu and render its interface.
    """
    def __init__(self, screen, display, manager, music):
        """
        Initialise the RegisterMenu class.
        :param screen: The pygame screen surface.
        :param display: The display surface for rendering.
        :param manager: The UI manager to handle UI elements.
        :param music: The music to be played in the menu.
        :return: None.
        """
        pygame.init()

        # Default
        self.screen = screen
        self.display = display
        self.manager = manager

        # Theme
        self.manager.get_theme().load_theme("../ThemeFile/LoginRegisterMenu.json")
        self.manager.get_theme().load_theme("../ThemeFile/Popup.json")

        # Audio
        if music != "":
            pygame.mixer.music.stop()

        sfxVolume = Settings().getKeyVariable("SFX")

        self.buttonClick = pygame.mixer.Sound("../Assets/Audio/ButtonClick.wav")
        self.buttonClick.set_volume(sfxVolume)

        # Register
        self.passwordInput = None
        self.confirmPasswordInput = None
        self.usernameInput = None
        self.emailInput = None

        self.usernameError = None
        self.emailError = None
        self.passwordError = None
        self.confirmPasswordError = None

        self.registerButton = None

        self.popup = None

        self.uiSetup()

    def uiSetup(self):
        """
        Setup basic GUI in the menu.
        :return: None.
        """
        # Background
        self.display.fill(pygame.Color('#FFE0E3'))

        # MainMenu Panel
        mainMenu = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0, 0), (750, 540)),
                                               manager=self.manager,
                                               anchors={'center': 'center'})

        # Logo Img
        logoImage = pygame.image.load("../Assets/Logo.png")
        logoRect = pygame.Rect((-5, 0), (363, 138))
        logoRect.top = 10
        logo = pygame_gui.elements.UIImage(relative_rect=logoRect,
                                           image_surface=logoImage,
                                           manager=self.manager,
                                           anchors={'centerx': 'centerx',
                                                    'top': 'top'})

        # Character Img
        neuroImage = pygame.image.load("../Assets/Character/NeuroDeath.png")
        neuroRect = pygame.Rect((0, 0), (256, 256))
        neuroRect.bottomright = (-80, -20)
        neuro = pygame_gui.elements.UIImage(relative_rect=neuroRect,
                                            image_surface=neuroImage,
                                            manager=self.manager,
                                            anchors={'right': 'right',
                                                     'bottom': 'bottom'})

        # Tutel Img
        tutelImage = pygame.image.load("../Assets/Character/Tutel.png")
        tutelRect = pygame.Rect((0, 0), (120, 120))
        tutelRect.bottomright = (-180, -100)
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

        # Email Label & Input
        emailLabelRect = textLineLabelRect
        emailLabelRect.topleft = (0, initialYLabel + stackY)
        emailLabel = pygame_gui.elements.UILabel(relative_rect=emailLabelRect,
                                                 text="EMAIL:",
                                                 manager=self.manager,
                                                 object_id=pygame_gui.core.ObjectID(
                                                     class_id="@mainLabel",
                                                     object_id="#emailLabel"),
                                                 container=mainMenu,
                                                 anchors={
                                                     'left': 'left',
                                                     'top': 'top'})

        emailInputRect = textLineInputRect
        emailInputRect.topright = (-90, initialYInput + stackY)
        self.emailInput = pygame_gui.elements.UITextEntryLine(relative_rect=emailInputRect,
                                                              manager=self.manager,
                                                              object_id=pygame_gui.core.ObjectID(
                                                                  class_id="@mainTextEntryLine",
                                                                  object_id="#emailInput"),
                                                              container=mainMenu,
                                                              anchors={
                                                                  'right': 'right',
                                                                  'top': 'top'})

        emailErrorRect = textLineErrorRect
        emailErrorRect.topleft = (270, initialYError + stackY)
        self.emailError = pygame_gui.elements.UILabel(relative_rect=emailErrorRect,
                                                      text="",
                                                      manager=self.manager,
                                                      object_id=pygame_gui.core.ObjectID(
                                                          class_id="@mainError",
                                                          object_id="#emailError"),
                                                      container=mainMenu,
                                                      anchors={
                                                          'left': 'left',
                                                          'top': 'top'})

        # Password Label & Input
        passwordLabelRect = textLineLabelRect
        passwordLabelRect.topleft = (0, initialYLabel + (stackY * 2))
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
        passwordInputRect.topright = (-90, initialYInput + (stackY * 2))
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
        passwordErrorRect.topleft = (270, initialYError + (stackY * 2))
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

        # Confirm Password Label & Input
        confirmPasswordTopLabelRect = textLineLabelRect
        confirmPasswordTopLabelRect.topleft = (-20, initialYLabel + (stackY * 2) + 40)
        confirmPasswordTopLabel = pygame_gui.elements.UILabel(relative_rect=confirmPasswordTopLabelRect,
                                                              text="CONFIRM",
                                                              manager=self.manager,
                                                              object_id=pygame_gui.core.ObjectID(
                                                                  class_id="@mainLabel",
                                                                  object_id="#confirmPasswordTopLabel"),
                                                              container=mainMenu,
                                                              anchors={
                                                                  'left': 'left',
                                                                  'top': 'top'})

        confirmPasswordBottomLabelRect = textLineLabelRect
        confirmPasswordBottomLabelRect.topleft = (0, initialYLabel + (stackY * 3))
        confirmPasswordBottomLabel = pygame_gui.elements.UILabel(relative_rect=confirmPasswordBottomLabelRect,
                                                                 text="PASSWORD:",
                                                                 manager=self.manager,
                                                                 object_id=pygame_gui.core.ObjectID(
                                                                     class_id="@mainLabel",
                                                                     object_id="#confirmPasswordBottomLabel"),
                                                                 container=mainMenu,
                                                                 anchors={
                                                                     'left': 'left',
                                                                     'top': 'top'})

        confirmPasswordInputRect = textLineInputRect
        confirmPasswordInputRect.topright = (-90, initialYInput + (stackY * 3))
        self.confirmPasswordInput = pygame_gui.elements.UITextEntryLine(relative_rect=confirmPasswordInputRect,
                                                                        manager=self.manager,
                                                                        object_id=pygame_gui.core.ObjectID(
                                                                            class_id="@mainTextEntryLinePassword",
                                                                            object_id="#confirmPasswordInput"),
                                                                        container=mainMenu,
                                                                        anchors={
                                                                            'right': 'right',
                                                                            'top': 'top'})

        confirmPasswordErrorRect = textLineErrorRect
        confirmPasswordErrorRect.topleft = (270, initialYError + (stackY * 3))
        self.confirmPasswordError = pygame_gui.elements.UILabel(relative_rect=confirmPasswordErrorRect,
                                                                text="",
                                                                manager=self.manager,
                                                                object_id=pygame_gui.core.ObjectID(
                                                                    class_id="@mainError",
                                                                    object_id="#confirmPasswordError"),
                                                                container=mainMenu,
                                                                anchors={
                                                                    'left': 'left',
                                                                    'top': 'top'})

        # Login Link
        loginLinkRect = pygame.Rect((0, 0), (350, 40))
        loginLinkRect.bottomleft = 40, -30
        loginLink = pygame_gui.elements.UITextBox(relative_rect=loginLinkRect,
                                                  html_text="<font face='pixeltype' pixel_size=25>"
                                                            "Already have an account? Login "
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

        # Register Button
        registerButtonRect = pygame.Rect((-30, 0), (259, 76))
        registerButtonRect.bottom = -80
        self.registerButton = pygame_gui.elements.UIButton(relative_rect=registerButtonRect,
                                                           text="",
                                                           manager=self.manager,
                                                           object_id=pygame_gui.core.ObjectID(
                                                               class_id="@mainButton",
                                                               object_id="#registerButton"),
                                                           container=mainMenu,
                                                           anchors={'centerx': 'centerx',
                                                                    'bottom': 'bottom'})

    def eventCheck(self, ev):
        """
        Check for events happening in this menu.
        :param ev: The pygame event variable.
        :return: None
        """
        match ev.type:
            case pygame_gui.UI_BUTTON_PRESSED:
                # print(ev.ui_element)
                match ev.ui_element:
                    case self.registerButton:
                        self.buttonClick.play()
                        self.usernameError.set_text("")
                        self.emailError.set_text("")
                        self.passwordError.set_text("")
                        self.confirmPasswordError.set_text("")
                        try:
                            auth = Authentication()
                            status = auth.registerCheck(self.usernameInput.get_text(), self.emailInput.get_text(),
                                                        self.passwordInput.get_text(), self.confirmPasswordInput.get_text())

                            if status['username'] is not None:
                                self.usernameError.set_text(status['username'])
                            if status['email'] is not None:
                                self.emailError.set_text(status['email'])
                            if status['password'] is not None:
                                self.passwordError.set_text(status['password'])
                                self.confirmPasswordError.set_text(status['password'])
                            if status['successful'] is True:
                                message = "Register successful!"
                                self.popup = Popup(self.manager, self.display, message, "Ok", "Register")
                                self.disableAllElements()
                        except:
                            self.screen("error;Database Error Occurred:;Please contact Admin to resolve the matter.")
                    case self.popup.closeButton:
                        self.buttonClick.play()
                        self.screen("loginMenu")
                    case self.popup.okButton:
                        self.buttonClick.play()
                        self.screen("loginMenu")


            case pygame_gui.UI_TEXT_BOX_LINK_CLICKED:
                self.screen("loginMenu")

    def update(self, timeDelta):
        """
        Update the events.
        :param timeDelta: The time elapsed since last update.
        :return: None.
        """
        self.manager.update(timeDelta)

    def disableAllElements(self):
        """
        Hide all elements from screen.
        :return: None
        """
        self.usernameInput.disable()
        self.emailInput.disable()
        self.passwordInput.disable()
        self.confirmPasswordInput.disable()
        self.registerButton.disable()

    def enableAllElements(self):
        """
        Show all elements on screen.
        :return: None
        """
        self.usernameInput.enable()
        self.emailInput.enable()
        self.passwordInput.enable()
        self.confirmPasswordInput.enable()
        self.registerButton.enable()

    def draw(self):
        """
        Draw elements onto the game.
        :return: None
        """
        pass
