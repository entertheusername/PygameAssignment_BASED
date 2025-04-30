import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pygame
import pygame_gui

class Error:
    def __init__(self, screen, display, manager, music, errorMsg):
        pygame.init()

        # Default
        self.screen = screen
        self.display = display
        self.manager = manager
        self.errorMsg = errorMsg

        # Theme
        self.manager.get_theme().load_theme("../ThemeFile/LoginRegisterMenu.json")

        # Audio
        if music != "":
            pygame.mixer.music.stop()

        # Error
        self.uiSetup()

    def uiSetup(self):
        """
        Setup basic GUI interface using pygame_gui.
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
        logoRect = pygame.Rect((0, 0), (363, 138))
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

        # Database Issue Label
        errorLabel = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((-20, 100), (400,60)),
                                                    text=self.errorMsg[0],
                                                    manager=self.manager,
                                                    object_id=pygame_gui.core.ObjectID(
                                                        class_id="@errorLabel",
                                                        object_id="#errorLabel"),
                                                    container=mainMenu,
                                                    anchors={
                                                        'top': 'top',
                                                        'centerx': 'centerx'})

        errorLabel = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((-20, 140), (600, 60)),
                                                 text=self.errorMsg[1],
                                                 manager=self.manager,
                                                 object_id=pygame_gui.core.ObjectID(
                                                     class_id="@errorLabel",
                                                     object_id="#errorLabel"),
                                                 container=mainMenu,
                                                 anchors={
                                                     'top': 'top',
                                                     'centerx': 'centerx'})


    def eventCheck(self, ev):
        """
        Check any specific game events happened.
        :param event: pygame event variable.
        :return: None
        """
        pass

    def update(self, timeDelta):
        """
        Update game events.
        :param timeDelta: Timing nonsense
        :return: None
        """
        self.manager.update(timeDelta)

    def draw(self):
        """
        Draw elements onto the game.
        :return: None
        """
        pass
