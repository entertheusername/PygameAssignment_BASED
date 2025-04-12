# This file is for apple logic
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame
from BackEnd.GameEngine_constants import *


class Apple:
    def __init__(self, game, x, y, value, base, is_correct):
        self.game = game
        self.radius = APPLE_RADIUS
        self.x = x
        self.y = y
        self.value = value
        self.base = base
        self.is_correct = is_correct
        self.color = Colors.GREEN if is_correct else Colors.RED
        self.speed = GameSettings.SPEED / 2

    def draw(self, screen):
        # Draw the apple image
        screen.blit(pygame.image.load("../Assets/Character/GameTutel.png"),
                    (self.x - 75, self.y - self.radius))

        font_main = pygame.font.SysFont(None, 24)   # Font for answer value
        font_base = pygame.font.SysFont(None, 16)   # Font for number base (smaller)

        # Render the value and base
        value_text = font_main.render(str(self.value), True, Colors.BLACK)
        base_text = font_base.render(str(self.base), True, Colors.BLACK)

        # Position value in the center of the apple
        value_rect = value_text.get_rect(center=(self.x, self.y))

        # Position base to the bottom-right of the value
        base_rect = base_text.get_rect(midleft=(value_rect.right + 2, value_rect.bottom - 3))

        # Blit to screen
        screen.blit(value_text, value_rect)
        screen.blit(base_text, base_rect)

    def fall(self):
        self.y += self.speed
        return self.y > HEIGHT
