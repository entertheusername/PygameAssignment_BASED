# This file is for apple logic
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame
from BackEnd.GameEngine_constants import *


class Apple:
    def __init__(self, game, x, y, value, is_correct):
        self.game = game
        self.radius = APPLE_RADIUS
        self.x = x
        self.y = y
        self.value = value
        self.is_correct = is_correct
        self.color = Colors.GREEN if is_correct else Colors.RED
        self.speed = GameSettings.SPEED / 2

    def draw(self, screen):
        screen.blit(pygame.image.load("../Assets/Character/GameTutel.png"),
                    (self.x - 75, self.y - self.radius))
        pygame.draw.circle(screen, self.color, (self.x, self.y), 10)  # Correct indicators (needed to be comment)
        font = pygame.font.SysFont(None, 24)
        text = font.render(self.value, True, Colors.BLACK)
        text_rect = text.get_rect(center=(self.x, self.y))
        screen.blit(text, text_rect)

    def fall(self):
        self.y += self.speed
        return self.y > HEIGHT
