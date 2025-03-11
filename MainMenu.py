import pygame
import pygame_gui


class MainMenu:
    def __init__(self, screen, display, manager):
        pygame.init()
        self.screen = screen
        self.display = display
        self.manager = manager
        self.isRunning = True

        self.manager.get_theme().load_theme("ThemeFile/MainMenu.json")
        self.manager.get_theme().load_theme("ThemeFile/MainButtons.json")

        self.uiSetup()

    def uiSetup(self):
        self.display.fill(pygame.Color('#FFE0E3'))

        # MainMenu Panel
        mainMenu = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0, 0), (750, 540)),
                                               manager=self.manager,
                                               anchors={'center': 'center'})

        # Logo Img
        logoImage = pygame.image.load("Assets/Logo.png")
        logoRect = pygame.Rect((-5, 0), (363, 138))
        logoRect.top = 10
        logo = pygame_gui.elements.UIImage(relative_rect=logoRect,
                                           image_surface=logoImage,
                                           manager=self.manager,
                                           anchors={'centerx': 'centerx',
                                                    'top': 'top'})

        # Neuro Img
        neuroImage = pygame.image.load("Assets/NeuroDeath.png")
        neuroRect = pygame.Rect((0, 0), (256, 256))
        neuroRect.bottomright = (-80, -20)
        neuro = pygame_gui.elements.UIImage(relative_rect=neuroRect,
                                            image_surface=neuroImage,
                                            manager=self.manager,
                                            anchors={'right': 'right',
                                                     'bottom': 'bottom'})

        # Tutel Img
        tutelImage = pygame.image.load("Assets/Tutel.png")
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


        initialYLabel = 40
        initialYInput = 50
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
        usernameInput = pygame_gui.elements.UITextEntryLine(relative_rect=usernameInputRect,
                                                            manager=self.manager,
                                                            object_id=pygame_gui.core.ObjectID(
                                                                class_id="@mainTextEntryLine",
                                                                object_id="#usernameInput"),
                                                            container=mainMenu,
                                                            anchors={
                                                                'right': 'right',
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
        emailInput = pygame_gui.elements.UITextEntryLine(relative_rect=emailInputRect,
                                                         manager=self.manager,
                                                         object_id=pygame_gui.core.ObjectID(
                                                             class_id="@mainTextEntryLine",
                                                             object_id="#emailInput"),
                                                         container=mainMenu,
                                                         anchors={
                                                             'right': 'right',
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
        passwordInput = pygame_gui.elements.UITextEntryLine(relative_rect=passwordInputRect,
                                                            manager=self.manager,
                                                            object_id=pygame_gui.core.ObjectID(
                                                                class_id="@mainTextEntryLine",
                                                                object_id="#passwordInput"),
                                                            container=mainMenu,
                                                            anchors={
                                                                'right': 'right',
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
        confirmPasswordInput = pygame_gui.elements.UITextEntryLine(relative_rect=confirmPasswordInputRect,
                                                                   manager=self.manager,
                                                                   object_id=pygame_gui.core.ObjectID(
                                                                       class_id="@mainTextEntryLine",
                                                                       object_id="#confirmPasswordInput"),
                                                                   container=mainMenu,
                                                                   anchors={
                                                                       'right': 'right',
                                                                       'top': 'top'})

        # Register Button
        registerButtonRect = pygame.Rect((-30, 0), (259, 76))
        registerButtonRect.bottom = -50
        registerButton = pygame_gui.elements.UIButton(relative_rect=registerButtonRect,
                                                      text="",
                                                      manager=self.manager,
                                                      object_id=pygame_gui.core.ObjectID(
                                                          class_id="@mainButton",
                                                          object_id="#registerButton"),
                                                      container=mainMenu,
                                                      anchors={'centerx': 'centerx',
                                                               'bottom': 'bottom'})
        #
        # loginButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 100), (226, 76)),
        #                                             text="",
        #                                             manager=self.manager,
        #                                             object_id=pygame_gui.core.ObjectID(
        #                                                 class_id="@mainButton",
        #                                                 object_id="#loginButton"))
        #

    def eventCheck(self, ev):
        match ev.type:
            case pygame_gui.UI_BUTTON_PRESSED:
                print(ev.ui_element.object_ids)
                match ev.ui_element.object_ids[1]:
                    case "#loginButton":
                        print("Hello World!")

                    case "#registerButton":
                        print("Hello Gay!")
                        self.screen("testMenu")

    def update(self, timeDelta):
        self.manager.update(timeDelta)
