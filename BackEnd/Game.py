# This file is for whole game logic
import sys
import os
import pygame
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from BackEnd.Basket import Basket
from BackEnd.Apple import Apple
from BackEnd.Answer_generator import AnswerGenerator
from BackEnd.Question_generator import Question
from BackEnd import Constants

# Helper function skibidi ahhhhhh (To avoid repetition of code in draw_question)
def render_number_with_base(screen, value: str, base: int, x: int, y: int, font: pygame.font.Font, sub_font: pygame.font.Font, color) -> int:
    """Renders value and base subscript."""
    value_surf = font.render(value, True, color)
    base_surf = sub_font.render(str(base), True, color)
    base_x = x + value_surf.get_width()
    base_y = y + value_surf.get_height() - base_surf.get_height()

    screen.blit(value_surf, (x, y))
    screen.blit(base_surf, (base_x, base_y))

    return value_surf.get_width() + base_surf.get_width()

class Game:
    def __init__(self, screen, display, manager, gamemode: str):
        pygame.init()

        self.screen = screen
        self.display = display
        self.manager = manager

        self.basket = Basket(self)  # Pass game reference to basket
        self.apples = []

        self.font_size = 36
        self.sub_font_size = int(self.font_size * 0.6)
        self.font = pygame.font.SysFont(None, self.font_size)
        self.sub_font = pygame.font.SysFont(None, self.sub_font_size)
        self.text_color = Constants.COLOR_BLACK

        self.score = 0
        self.game_active = True
        self.final_message = ""

        self.game_generator = AnswerGenerator(gamemode)
        self.current_question_obj: Question | None = None
        self.correct_answer_value = ""
        self.wrong_answer_values = []

        self.max_apples_on_screen = 8
        self.spawn_interval = 1 # Time between each spawn
        self.spawn_timer = 1.5 # Timer until next spawn wave
        self.prob_correct_spawn = 0.35 # Probability of spawning the correct answer randomly

        self.background_img = None
        try:
            self.background_img = pygame.image.load("../Assets/Background/BackgroundBlur.png")
        except pygame.error as e:
            print(f"Error loading background image: {e}")

        self.setup_new_question()

    def setup_new_question(self):
        self.current_question_obj, self.wrong_answer_values = self.game_generator.generate_question_data()
        if self.current_question_obj:
            self.correct_answer_value = self.current_question_obj.correct_answer
        else:
            print("Error. No questions generated.")
            self.correct_answer_value = "Cant find an answer to ur life bitch"
        self.apples = [] # Clear existing apples
        self.spawn_timer = self.spawn_interval

    def eventCheck(self, event):
        if event.type == pygame.KEYDOWN and not self.game_active:
            if event.key == pygame.K_r:  # Restart game on R key
                self.screen("gameModeSelectMenu")
        self.manager.process_events(event)

    def spawn_apple(self):
        """Creates a new apple at a random position."""
        if not self.current_question_obj: return
        value_to_spawn = None
        spawn_is_correct = False
        correct_on_screen = any(apple.is_correct for apple in self.apples)
        target_base = self.current_question_obj.target_base

        if not correct_on_screen:
            # Force spawn the correct answer
            value_to_spawn = self.correct_answer_value
            spawn_is_correct = True
        else:
            # Random spawn the correct answer
            random_spawn_correct = random.random() < self.prob_correct_spawn
            if random_spawn_correct:
                value_to_spawn = self.correct_answer_value
                spawn_is_correct = True
            else:
                # Spawn a wrong answer
                if self.wrong_answer_values:
                    # Ignore values that are already on screen
                    wrong_on_screen = {apple.value for apple in self.apples if not apple.is_correct}
                    available_wrong_values = [value for value in self.wrong_answer_values if value not in wrong_on_screen]

                    if available_wrong_values:
                        # Randomly spawn from list of available wrong answers
                        value_to_spawn = random.choice(available_wrong_values)
                        spawn_is_correct = False

        if value_to_spawn is None:
             print("Error. No answer to be spawned.")
             return

        values_on_screen = {apple.value for apple in self.apples}
        if value_to_spawn in values_on_screen:
            return

        # Start spawning
        apple_width = Apple(self, 0, 0, value_to_spawn, target_base, spawn_is_correct).rect.width
        apple_height = Apple(self, 0, 0, value_to_spawn, target_base, spawn_is_correct).rect.height
        x = None
        y = None

        # Validate spawn position
        for _ in range(100):  # Loop to get valid position
            x = random.randint(apple_width // 2 + 15, Constants.SCREEN_WIDTH - apple_width // 2 - 15)
            y = random.randint(-60, -30)  # Start slightly above the screen

            # Check for collision with existing apples
            new_rect = pygame.Rect(x, y, apple_width, apple_height)
            if all(new_rect.colliderect(apple.rect.inflate(30, 30)) == False for apple in self.apples):
                break
        else:
            print("Error finding valid position after 100 attempts.")
            return
    
        new_apple = Apple(self, x, y, value_to_spawn, target_base, spawn_is_correct)
        self.apples.append(new_apple)

    def update(self, timeDelta):
        """Main game update loop logic."""
        self.manager.update(timeDelta)

        if not self.game_active:
            return

        # Update basket position
        self.basket.update()

        # Spawn apples
        self.spawn_timer -= timeDelta
        if self.spawn_timer <= 0 and len(self.apples) < self.max_apples_on_screen:
            self.spawn_apple()
            self.spawn_timer = self.spawn_interval # Reset timer

        # Check collision and update position
        collided_apple = None
        for apple in self.apples[:]:
            if self.basket.collides_with(apple):
                collided_apple = apple
                break
            if apple.fall():
                self.apples.remove(apple)

        if collided_apple:
            self.apples.remove(collided_apple) # Remove the caught apple
            if collided_apple.is_correct:
                self.score += 1
                self.setup_new_question()
            else:
                # Caught wrong apple -> Game over
                self.game_over(f"Wrong Apple! The answer is {self.correct_answer_value}.")

    def game_over(self, message):
        self.game_active = False
        self.final_message = f"\n{message} Final Score: {self.score}. Press R to restart"

    def draw_question(self):
        """Render questions with subscript bases"""
        if not self.game_active or not self.current_question_obj:
            return
        
        ques = self.current_question_obj
        y_pos = 15
        padding = 8

        # Render CONVERSION
        if ques.question_type == "CONVERSION":
            text_p1 = "Convert "
            text_p2 = f" to base {ques.target_base}"

            surf_p1 = self.font.render(text_p1, True, self.text_color)
            surf_p2 = self.font.render(text_p2, True, self.text_color)

            val_surf_temp = self.font.render(ques.operand1, True, self.text_color)
            sub_surf_temp = self.sub_font.render(str(ques.base1), True, self.text_color)
            num_width = val_surf_temp.get_width() + sub_surf_temp.get_width()
            total_width = surf_p1.get_width() + num_width + surf_p2.get_width()
            start_x = (Constants.SCREEN_WIDTH - total_width) // 2
            current_x = start_x

            self.display.blit(surf_p1, (current_x, y_pos))
            current_x += surf_p1.get_width() + padding
            width_drawn = render_number_with_base(self.display, ques.operand1, ques.base1, current_x, y_pos, self.font, self.sub_font, self.text_color)
            current_x += width_drawn + padding

            self.display.blit(surf_p2, (current_x, y_pos))

        else: # Render BASIC / MIXED CALCULATION
            render_elements = []
            render_elements.append({'type': 'num', 'value': ques.operand1, 'base': ques.base1}) # OP1
            render_elements.append({'type': 'op', 'text': f" {ques.operator} "}) # Operator
            if ques.operand2 is not None and ques.base2 is not None: # OP2
                render_elements.append({'type': 'num', 'value': ques.operand2, 'base': ques.base2})
            render_elements.append({'type': 'op', 'text': " = ?"}) # Question mark wtsigma

            total_width = 0
            calculated_widths = [] # Store widths
            for element in render_elements:
                width = 0
                if element['type'] == 'num':
                    val_surf = self.font.render(element['value'], True, self.text_color)
                    sub_surf = self.sub_font.render(str(element['base']), True, self.text_color)
                    width = val_surf.get_width() + sub_surf.get_width()
                else: # OP
                    op_surf = self.font.render(element['text'], True, self.text_color)
                    width = op_surf.get_width()
                calculated_widths.append(width)
                total_width += width + padding
            total_width -= padding # Remove last padding

            start_x = (Constants.SCREEN_WIDTH - total_width) // 2
            current_x = start_x

            # Draw
            for i, element in enumerate(render_elements):
                element_width = calculated_widths[i]
                if element['type'] == 'num':
                    render_number_with_base(self.display, element['value'], element['base'], current_x, y_pos, self.font, self.sub_font, self.text_color)
                    current_x += element_width + padding
                else: # OP
                    op_surf = self.font.render(element['text'], True, self.text_color)
                    op_y = y_pos + (self.font_size - op_surf.get_height()) // 2
                    self.display.blit(op_surf, (current_x, op_y))
                    current_x += element_width + padding

    def draw(self):
        # Background
        try:
            self.display.blit(self.background_img, (0, 0))
        except pygame.error as e:
            print(f"Error loading background image: {e}")
            self.display.fill(pygame.Color('#FFE0E3')) # Pinky Ponky Panky Punky

        # Draw basket and apples
        self.basket.draw(self.display)
        for apple in self.apples:
            apple.draw(self.display)

        if self.game_active:
            # Draw score and question during gameplay
            score_text = self.font.render(f"Score: {self.score}", True, Constants.COLOR_WHITE)
            self.display.blit(score_text, (10, 10))
            self.draw_question()
        else:
            # Draw game over message
            game_over_surf = self.font.render(self.final_message, True, Constants.COLOR_WHITE)
            game_over_rect = game_over_surf.get_rect(center=(Constants.SCREEN_WIDTH // 2, Constants.SCREEN_HEIGHT // 2))
            self.display.blit(game_over_surf, game_over_rect)

        self.manager.draw_ui(self.display)
        pygame.display.update()
