# This file is for whole game logic
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pygame
import sys
from BackEnd.GameEngine_basket import Basket
from BackEnd.GameEngine_game_generator import GameGenerator
from BackEnd.GameEngine_constants import *


class Game:
    def __init__(self, screen, display, manager, gamemode: str):
        pygame.init()

        self.screen = screen
        self.display = display
        self.manager = manager

        self.basket = Basket(self)  # Pass game reference to basket
        self.apples = []
        self.apples_fell = 0
        self.font = pygame.font.SysFont(None, 36)
        self.game_generator = GameGenerator(self, gamemode)

        self.score = 0
        self.current_question = ""
        self.game_active = True
        self.final_message = ""

        self.setup_new_question()

    def setup_new_question(self):
        self.current_question, self.apples = self.game_generator.generate_question()

    def eventCheck(self, event):
        if event.type == pygame.KEYDOWN and not self.game_active:
            if event.key == pygame.K_r:  # Restart game on R key
                self.screen("gameModeSelectMenu")

    def update(self, timeDelta):

        self.manager.update(timeDelta)

        if not self.game_active:
            return

        # Update basket position
        self.basket.update()

        # First check for correct apples caught
        caught_apple = None
        for apple in self.apples[:]:
            # Create a temporary rect for the apple for collision detection
            apple_rect = pygame.Rect(
                apple.x - apple.radius,
                apple.y - apple.radius,
                apple.radius * 2,
                apple.radius * 2
            )

            if self.basket.rect.colliderect(apple_rect):
                if apple.is_correct:
                    caught_apple = apple
                elif not caught_apple:
                    caught_apple = apple

            if apple.fall():  # Check for fallen apples
                self.apples.remove(apple)
                self.apples_fell += 1

        # Handle caught apple
        if caught_apple:
            self.apples.remove(caught_apple)
            if caught_apple.is_correct:
                self.score += 1
                self.setup_new_question()
            else:
                self.game_over("Wrong answer!")

        # End game if all apples fell
        if self.apples_fell == 3 and len(self.apples) == 0:
            self.game_over("Missed all apples!")

    def game_over(self, message):
        self.game_active = False
        self.final_message = f"{message} Final Score: {self.score}. Press R to restart"

    def draw(self):
        self.display.fill(Colors.BLACK)

        # Draw basket and apples
        self.basket.draw(self.display)
        for apple in self.apples:
            apple.draw(self.display)

        if self.game_active:
            # Draw score and question during gameplay
            score_text = self.font.render(f"Score: {self.score}", True, Colors.WHITE)
            question_text = self.font.render(self.current_question, True, Colors.WHITE)

            self.display.blit(score_text, (10, 10))
            self.display.blit(question_text, (WIDTH // 2 - question_text.get_width() // 2, 10))
        else:
            # Draw game over message
            game_over_text = self.font.render(self.final_message, True, Colors.WHITE)
            self.display.blit(game_over_text,
                              (WIDTH // 2 - game_over_text.get_width() // 2,
                               HEIGHT // 2 - game_over_text.get_height() // 2))

        pygame.display.update()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()
