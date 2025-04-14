# This file is for apple logic
import sys
import os
import pygame

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from BackEnd import Constants

class Apple:
    def __init__(self, game, x, y, value: str, base: int, is_correct: bool):
        self.game = game
        self.value = str(value)
        self.base = base
        self.is_correct = is_correct
        self.color = Constants.COLOR_GREEN if is_correct else Constants.COLOR_RED
        self.speed = 2.5

        try:
            self.image = pygame.image.load("../Assets/Character/GameTutel.png").convert_alpha()
        except pygame.error as e:
            print(f"Error loading apple image: {e}")

        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.font_size = 30
        self.subscript_size = int(self.font_size * 0.6)
        self.font = pygame.font.Font("../Assets/Text/Pixeltype.ttf", self.font_size)
        self.sub_font = pygame.font.Font("../Assets/Text/Pixeltype.ttf", self.subscript_size)
        self.text_color = (255, 206, 27)
        self.sub_font.set_bold(True)
        self.text_surf = self.font.render(self.value, True, Constants.COLOR_WHITE)
        self.text_rect = self.text_surf.get_rect()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        value_surf = self.font.render(self.value, True, self.text_color)
        base_surf = self.sub_font.render(str(self.base), True, self.text_color)
        combined_text_width = value_surf.get_width() + base_surf.get_width() * 0.6
        combined_text_rect = pygame.Rect(0, 0, combined_text_width, value_surf.get_height())
        combined_text_rect.center = (self.rect.centerx + 10, self.rect.centery - 5)
        value_pos = combined_text_rect.topleft
        base_x = value_pos[0] + value_surf.get_width()
        base_y = value_pos[1] + value_surf.get_height() - base_surf.get_height() + 1
        # Correct indicators (FOR TESTING, COMMENT IF NOT NEEDED)
        pygame.draw.circle(screen, self.color, combined_text_rect.center, 25)
        screen.blit(value_surf, value_pos)
        screen.blit(base_surf, (base_x, base_y))

    def fall(self):
        self.rect.y += self.speed
        return self.rect.top > 1080
