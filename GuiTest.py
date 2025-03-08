import pygame
import pygame_gui

pygame.init()

pygame.display.set_caption('Quick Start')
windowSurface = pygame.display.set_mode((1080, 640))

background = pygame.Surface((1080, 640))
background.fill(pygame.Color('#FFE0E3'))

manager = pygame_gui.UIManager((1080, 640))
manager.get_theme().load_theme("ThemeFile/MainMenu.json")
manager.get_theme().load_theme("ThemeFile/MainButtons.json")

# MainMenu Panel
mainMenu = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0, 10), (750, 520)),
                                       manager=manager,
                                       anchors={'center': 'center'})

# Logo Img
logoImage = pygame.image.load("Assets/Logo.png")
logoRect = pygame.Rect((-5, 0), (363, 138))
logoRect.top = 30
logo = pygame_gui.elements.UIImage(relative_rect=logoRect,
                                   image_surface=logoImage,
                                   manager=manager,
                                   anchors={'centerx': 'centerx',
                                            'top': 'top'})

# Neuro Img
neuroImage = pygame.image.load("Assets/NeuroDeath.png")
neuroRect = pygame.Rect((0, 0), (256, 256))
neuroRect.bottomright = (-80, -20)
neuro = pygame_gui.elements.UIImage(relative_rect=neuroRect,
                                    image_surface=neuroImage,
                                    manager=manager,
                                    anchors={'right': 'right',
                                             'bottom': 'bottom'})

# Tutel Img
tutelImage = pygame.image.load("Assets/Tutel.png")
tutelRect = pygame.Rect((0, 0), (120, 120))
tutelRect.bottomright = (-180, -100)
tutel = pygame_gui.elements.UIImage(relative_rect=tutelRect,
                                    image_surface=tutelImage,
                                    manager=manager,
                                    anchors={'right': 'right',
                                             'bottom': 'bottom'})

# Initial Form Setup
textLineLabelRect = pygame.Rect((0, 0), (260, 60))
textLineInputRect = pygame.Rect((0, 0), (340, 40))

# Username Label & Input
usernameLabelRect = textLineLabelRect
usernameLabelRect.topleft = (0, 50)
usernameLabel = pygame_gui.elements.UILabel(relative_rect=usernameLabelRect,
                                            text="TEST:",
                                            manager=manager,
                                            object_id=pygame_gui.core.ObjectID(
                                                class_id="@mainLabel",
                                                object_id="#usernameLabel"),
                                            container=mainMenu,
                                            anchors={
                                                'left': 'left',
                                                'top': 'top'})

usernameInputRect = textLineInputRect
usernameInputRect.topright = (-90, 60)
usernameInput = pygame_gui.elements.UITextEntryLine(relative_rect=usernameInputRect,
                                                    manager=manager,
                                                    object_id=pygame_gui.core.ObjectID(
                                                        class_id="@mainTextEntryLine",
                                                        object_id="#usernameInput"),
                                                    container=mainMenu,
                                                    anchors={
                                                        'right': 'right',
                                                        'top': 'top'})

# Email Label & Input
emailLabelRect = textLineLabelRect
emailLabelRect.topleft = (0, 120)
emailLabel = pygame_gui.elements.UILabel(relative_rect=emailLabelRect,
                                            text="EMAIL:",
                                            manager=manager,
                                            object_id=pygame_gui.core.ObjectID(
                                                class_id="@mainLabel",
                                                object_id="#emailLabel"),
                                            container=mainMenu,
                                            anchors={
                                                'left': 'left',
                                                'top': 'top'})

emailInputRect = textLineInputRect
emailInputRect.topright = (-90, 130)
emailInput = pygame_gui.elements.UITextEntryLine(relative_rect=emailInputRect,
                                                    manager=manager,
                                                    object_id=pygame_gui.core.ObjectID(
                                                        class_id="@mainTextEntryLine",
                                                        object_id="#emailInput"),
                                                    container=mainMenu,
                                                    anchors={
                                                        'right': 'right',
                                                        'top': 'top'})

# Password Label & Input
passwordLabelRect = textLineLabelRect
passwordLabelRect.topleft = (0, 190)
passwordLabel = pygame_gui.elements.UILabel(relative_rect=passwordLabelRect,
                                            text="PASSWORD:",
                                            manager=manager,
                                            object_id=pygame_gui.core.ObjectID(
                                                class_id="@mainLabel",
                                                object_id="#passwordLabel"),
                                            container=mainMenu,
                                            anchors={
                                                'left': 'left',
                                                'top': 'top'})

passwordInputRect = textLineInputRect
passwordInputRect.topright = (-90, 200)
passwordInput = pygame_gui.elements.UITextEntryLine(relative_rect=passwordInputRect,
                                                    manager=manager,
                                                    object_id=pygame_gui.core.ObjectID(
                                                        class_id="@mainTextEntryLine",
                                                        object_id="#passwordInput"),
                                                    container=mainMenu,
                                                    anchors={
                                                        'right': 'right',
                                                        'top': 'top'})

# Confirm Password Label & Input
confirmPasswordTopLabelRect = textLineLabelRect
confirmPasswordTopLabelRect.topleft = (-20, 240)
confirmPasswordTopLabel = pygame_gui.elements.UILabel(relative_rect=confirmPasswordTopLabelRect,
                                            text="CONFIRM",
                                            manager=manager,
                                            object_id=pygame_gui.core.ObjectID(
                                                class_id="@mainLabel",
                                                object_id="#confirmPasswordTopLabel"),
                                            container=mainMenu,
                                            anchors={
                                                'left': 'left',
                                                'top': 'top'})

confirmPasswordBottomLabelRect = textLineLabelRect
confirmPasswordBottomLabelRect.topleft = (0, 270)
confirmPasswordBottomLabel = pygame_gui.elements.UILabel(relative_rect=confirmPasswordBottomLabelRect,
                                            text="PASSWORD:",
                                            manager=manager,
                                            object_id=pygame_gui.core.ObjectID(
                                                class_id="@mainLabel",
                                                object_id="#confirmPasswordBottomLabel"),
                                            container=mainMenu,
                                            anchors={
                                                'left': 'left',
                                                'top': 'top'})

confirmPasswordInputRect = textLineInputRect
confirmPasswordInputRect.topright = (-90, 270)
confirmPasswordInput = pygame_gui.elements.UITextEntryLine(relative_rect=confirmPasswordInputRect,
                                                    manager=manager,
                                                    object_id=pygame_gui.core.ObjectID(
                                                        class_id="@mainTextEntryLine",
                                                        object_id="#confirmPasswordInput"),
                                                    container=mainMenu,
                                                    anchors={
                                                        'right': 'right',
                                                        'top': 'top'})

# Register Button
registerButtonRect = pygame.Rect((-30, 0), (259, 76))
registerButtonRect.bottom = -60
registerButton = pygame_gui.elements.UIButton(relative_rect=registerButtonRect,
                                            text="",
                                            manager=manager,
                                            object_id=pygame_gui.core.ObjectID(
                                                class_id="@mainButton",
                                                object_id="#registerButton"),
                                            container=mainMenu,
                                            anchors={'centerx': 'centerx',
                                                     'bottom': 'bottom'})

loginButtonRect = pygame.Rect((-30, 0), (259, 76))
loginButtonRect.bottom = -120
loginButton = pygame_gui.elements.UIButton(relative_rect=loginButtonRect,
                                            text="",
                                            manager=manager,
                                            object_id=pygame_gui.core.ObjectID(
                                                class_id="@mainButton",
                                                object_id="#loginButton"),
                                            container=mainMenu,
                                            anchors={'centerx': 'centerx',
                                                     'bottom': 'bottom'})
#
# loginButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 100), (226, 76)),
#                                             text="",
#                                             manager=manager,
#                                             object_id=pygame_gui.core.ObjectID(
#                                                 class_id="@mainButton",
#                                                 object_id="#loginButton"))
#

clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60) / 1000.0
    for ev in pygame.event.get():
        manager.process_events(ev)
        match ev.type:
            case pygame.QUIT:
                is_running = False

            case pygame_gui.UI_BUTTON_PRESSED:
                print(ev.ui_element.object_ids)
                match ev.ui_element.object_ids[1]:
                    case "#loginButton":
                        print("Hello World!")
                    case "#registerButton":
                        print("Hello Gay!")

        manager.process_events(ev)

    manager.update(time_delta)

    windowSurface.blit(background, (0, 0))
    manager.draw_ui(windowSurface)

    pygame.display.update()

