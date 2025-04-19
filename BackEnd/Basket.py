# This file is for handling player movement
import sys
import os
import pygame

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from BackEnd import Constants

class Basket:
    def __init__(self, game):
        self.game = game
        self.speed = 10

        try:
            self.img = pygame.image.load("../Assets/Character/NeuroAlive.png").convert_alpha()
        except pygame.error as e:
            print(f"Error loading basket image: {e}")

        self.img_left = self.img
        self.img_right = pygame.transform.flip(self.img_left, True, False)
        self.death_img = pygame.image.load("../Assets/Character/NeuroDeath.png").convert_alpha()
        self.death_img_right = pygame.transform.flip(self.death_img, True, False)
        self.width = self.img.get_width()
        self.height = self.img.get_height()

        self.rect = pygame.Rect(
            Constants.SCREEN_WIDTH // 2 - self.width // 2,
            Constants.SCREEN_HEIGHT - self.height - 10,
            self.width,
            self.height
        )

        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, screen):
        screen.blit(self.img, self.rect)

    def update(self):
        keys = pygame.key.get_pressed()
        new_img_position = False

        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 0:
            self.img = self.img_left
            new_img_position = True
            self.rect.x -= self.speed
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < Constants.SCREEN_WIDTH:
            self.img = self.img_right
            new_img_position = True
            self.rect.x += self.speed
        
        if new_img_position:
            self.mask = pygame.mask.from_surface(self.img)

    def collides_with(self, other_sprite):
        if not hasattr(other_sprite, 'rect') or not hasattr(other_sprite, 'mask'):
            print(f"Error checking collisions: {other_sprite} missing rect or mask.")
            return False

        offset_x = other_sprite.rect.x - self.rect.x
        offset_y = other_sprite.rect.y - self.rect.y
        collision_point = self.mask.overlap(other_sprite.mask, (offset_x, offset_y))
        return collision_point is not None 
