# This file is for handling player movement

import pygame
from BackEnd.GameEngine_constants import GameSettings, Colors, WIDTH

class Basket:
    def __init__(self, game):
        self.game = game
        self.width = GameSettings.BASKET_WIDTH
        self.height = GameSettings.BASKET_HEIGHT
        self.speed = GameSettings.SPEED * 2
        self.rect = pygame.Rect(
            WIDTH // 2 - self.width // 2,
            GameSettings.HEIGHT - self.height - 10,
            self.width,
            self.height
        )
        self.color = Colors.BLUE
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
    
    def update(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 0:
            self.rect.x -= self.speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < WIDTH:
            self.rect.x += self.speed