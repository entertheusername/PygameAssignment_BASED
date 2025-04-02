# This file is for apple logic

import pygame
from GameEngine_constants import *

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
        self.apple_rect = pygame.Rect(
                self.x - self.radius,
                self.y - self.radius,
                self.radius * 2,
                self.radius * 2
            )
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        font = pygame.font.SysFont(None, 24)
        text = font.render(self.value, True, Colors.BLACK)
        text_rect = text.get_rect(center=(self.x, self.y))
        screen.blit(text, text_rect)
    
    def fall(self):
        self.y += self.speed
        return self.y > HEIGHT