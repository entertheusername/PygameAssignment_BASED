import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pygame
import pygame_gui


class Popup:
    def __init__(self, manager, display, message, type, purpose):
        # Default
        self.manager = manager
        self.display = display
        self.message = message
        self.type = type
        self.purpose = purpose

        # Popup
        self.yesButton = None
        self.noButton = None
        self.okButton = None
        self.closeButton = None

        self.elements = []

        self.uiSetup()

    def uiSetup(self):

        # Popup itself
        popupRect = pygame.Rect((0, 0), (300, 150))
        popup = pygame_gui.elements.UIWindow(rect=popupRect,
                                             manager=self.manager,
                                             window_display_title="Popup",
                                             resizable=False,
                                             draggable=False,
                                             object_id=pygame_gui.core.ObjectID(
                                                 class_id="@popup",
                                                 object_id="#popup"))
        self.closeButton = popup.close_window_button
        self.centerWindow(popup)
        self.elements.append(popup)

        # Message
        messageLineRect = pygame.Rect((0, 0), (280, 50))
        messageLineRect.top = 20
        messageLine = pygame_gui.elements.UILabel(relative_rect=messageLineRect,
                                                  text=self.message,
                                                  manager=self.manager,
                                                  object_id=pygame_gui.core.ObjectID(
                                                      class_id="@popupMessage",
                                                      object_id="#popupMessage"),
                                                  container=popup,
                                                  anchors={
                                                      'centerx': 'centerx',
                                                      'top': 'top'})
        self.elements.append(messageLine)

        if self.type == "YesNo":

            if self.purpose == "Logout":
                words = ("Logout", "Exit")
                sizes = (70, 50)
            else:
                words = ("Yes", "No")
                sizes = (45, 45)

            # Yes button
            yesButtonRect = pygame.Rect((0, 0), (sizes[0], 35))
            yesButtonRect.bottomleft = 50, -10
            self.yesButton = pygame_gui.elements.UIButton(relative_rect=yesButtonRect,
                                                          text=words[0],
                                                          manager=self.manager,
                                                          object_id=pygame_gui.core.ObjectID(
                                                              class_id="@popupButton",
                                                              object_id="#yesButton"),
                                                          container=popup,
                                                          anchors={'left': 'left',
                                                                   'bottom': 'bottom'})
            self.elements.append(self.yesButton)

            # No button
            noButtonRect = pygame.Rect((0, 0), (sizes[1], 35))
            noButtonRect.bottomright = -50, -10
            self.noButton = pygame_gui.elements.UIButton(relative_rect=noButtonRect,
                                                         text=words[1],
                                                         manager=self.manager,
                                                         object_id=pygame_gui.core.ObjectID(
                                                             class_id="@popupButton",
                                                             object_id="#noButton"),
                                                         container=popup,
                                                         anchors={'right': 'right',
                                                                  'bottom': 'bottom'})
            self.elements.append(self.noButton)

        elif self.type == "Ok":
            # Ok button
            okButtonRect = pygame.Rect((0, 0), (45, 35))
            okButtonRect.bottom = -10
            self.okButton = pygame_gui.elements.UIButton(relative_rect=okButtonRect,
                                                         text="Ok",
                                                         manager=self.manager,
                                                         object_id=pygame_gui.core.ObjectID(
                                                             class_id="@popupButton",
                                                             object_id="#okButton"),
                                                         container=popup,
                                                         anchors={'centerx': 'centerx',
                                                                  'bottom': 'bottom'})
            self.elements.append(self.okButton)

    def centerWindow(self, window: pygame_gui.elements.UIWindow):
        window_size = window.get_relative_rect().size
        displayX, displayY = self.display.get_size()
        new_x = (displayX - window_size[0]) // 2
        new_y = (displayY - window_size[1]) // 2
        window.set_position((new_x, new_y))

    def killAll(self):
        for i in self.elements:
            i.kill()
