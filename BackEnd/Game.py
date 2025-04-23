# This file is for whole game logic
import sys
import os
import pygame
import pygame_gui
import random
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from BackEnd.Basket import Basket
from BackEnd.Apple import Apple
from BackEnd.Answer_generator import AnswerGenerator
from BackEnd.Question_generator import Question
from BackEnd import Constants
from BackEnd.LeaderboardManage import LeaderboardManage
from FrontEnd.PauseMenu import PauseMenu
from BackEnd.Settings import Settings


class Game:
    def __init__(self, screen, display, manager, music, gamemode: str):
        pygame.init()

        # Default
        self.screen = screen
        self.display = display
        self.manager = manager

        # Theme
        self.manager.get_theme().load_theme("../ThemeFile/Game.json")

        # Audio
        self.music = music
        if music != "Snowy":
            pygame.mixer.music.load("../Assets/Audio/Game-Undertale_Snowy.ogg")
            pygame.mixer.music.play(-1, fade_ms=3000)

        sfxVolume = Settings().getKeyVariable("SFX")

        self.buttonClick = pygame.mixer.Sound("../Assets/Audio/ButtonClick.wav")
        self.buttonClick.set_volume(sfxVolume)

        self.neuroDeath = pygame.mixer.Sound("../Assets/Audio/NeuroDeath.ogg")
        self.neuroDeath.set_volume(sfxVolume * 0.5)

        self.music_fade = 0
        self.music_fade_duration = 4

        # Game
        self.start_time = None
        self.end_time = None

        self.basket = Basket(self)  # Pass game reference to basket
        self.apples = []
        self.speed_increment = 0.3  # Speed increase per 5 points
        self.last_speed_update_score = 0

        self.font_size = 38
        self.sub_font_size = int(self.font_size * 0.6)
        self.text_color = Constants.COLOR_BLACK
        self.bold_offset = (1, 1)

        try:
            self.font = pygame.font.Font("../Assets/Text/Pixeltype.ttf", self.font_size)
            self.sub_font = pygame.font.Font("../Assets/Text/Pixeltype.ttf", self.sub_font_size)
        except pygame.error as e:
            print(f"Error loading font: {e}")
            self.font = pygame.font.SysFont(None, self.font_size)
            self.sub_font = pygame.font.SysFont(None, self.sub_font_size)

        self.score = 0
        self.game_active = True
        self.final_message = ""

        self.game_generator = AnswerGenerator(gamemode)
        self.current_question_obj: Question | None = None
        self.correct_answer_value = ""
        self.wrong_answer_values = []

        self.max_apples_on_screen = 8
        self.spawn_interval = 1  # Time between each spawn
        self.spawn_timer = 1.5  # Timer until next spawn wave
        self.prob_correct_spawn = 0.5  # Probability of spawning the correct answer

        self.paused = False
        self.pause_menu = None

        pause_button_rect = pygame.Rect((0, 0), (56, 56))
        pause_button_rect.topleft = 30, 30
        self.pause_button = pygame_gui.elements.UIButton(relative_rect=pause_button_rect,
                                                         text="",
                                                         object_id=pygame_gui.core.ObjectID(
                                                             class_id="@game_pause_button",
                                                             object_id="#pauseButton"),
                                                         manager=self.manager,
                                                         anchors={'left': 'left',
                                                                  'top': 'top'})

        self.background_img = None
        try:
            self.background_img = pygame.image.load("../Assets/Background/BackgroundClear.png")
        except pygame.error as e:
            print(f"Error loading background image: {e}")

        # For death animation
        self.death_animation_timer = 0
        self.death_animation_duration = 2
        self.show_correct_answer = False
        self.basket_visible = True
        self.blink_timer = 0
        self.blink_interval = 0.2

        self.setup_new_question()

    def setup_new_question(self):
        self.current_question_obj, self.wrong_answer_values = self.game_generator.generate_question_data()
        if self.current_question_obj:
            self.correct_answer_value = self.current_question_obj.correct_answer
        else:
            print("Error. No questions generated.")
            self.correct_answer_value = "Cant find an answer to ur life bitch"
        self.apples = []  # Clear existing apples
        self.spawn_timer = self.spawn_interval

    def eventCheck(self, event):
        self.manager.process_events(event)

        # switch to pause event check
        if self.paused and self.pause_menu:
            self.pause_menu.eventCheck(event)
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and self.game_active:
                self.pause_button.hide()
                # call pause menu
                self.paused = True
                self.pause_menu = PauseMenu(self, self.display, self.manager, self.current_question_obj.gamemode)
            # elif event.key == pygame.K_c and self.game_active: # Testing, if not then comment
            #     self.score += 1

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.pause_button:
                self.buttonClick.play()
                self.pause_button.hide()
                # call pause menu
                self.paused = True
                self.pause_menu = PauseMenu(self, self.display, self.manager, self.current_question_obj.gamemode)

    def spawn_apple(self):
        """Creates a new apple at a random position."""
        if not self.current_question_obj: return
        value_to_spawn = None
        spawn_is_correct = False
        target_base = self.current_question_obj.target_base
        spawn_correct = random.random() < self.prob_correct_spawn

        # Spawn the correct answer
        if spawn_correct:
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

        if 20 <= self.score < 40:
            self.switch_music("../Assets/Audio/Game-Undertale_Hotel.ogg", "Hotel", timeDelta)
        elif 40 <= self.score < 60:
            self.switch_music("../Assets/Audio/Game-Undertale_Dont_Give_Up.ogg", "DontGiveUp", timeDelta)
        elif 60 <= self.score < 80:
            self.switch_music("../Assets/Audio/Game-Undertale_Hopes_And_Dreams.ogg", "HopesAndDreams", timeDelta)
        elif 80 <= self.score < 100:
            self.switch_music("../Assets/Audio/Game-Undertale_Megalovania.ogg", "Megalovania", timeDelta)
        elif 100 <= self.score:
            self.switch_music("../Assets/Audio/Game-CHXI_Life_Arrangement.ogg", "LifeArrangement", timeDelta)

        self.manager.update(timeDelta)

        if self.paused:
            return

        if not self.game_active and self.show_correct_answer:
            # Update death animation timer
            self.death_animation_timer += timeDelta
            self.blink_timer += timeDelta

            # Blink blink effect
            if self.blink_timer >= self.blink_interval:
                self.blink_timer = 0
                self.basket_visible = not self.basket_visible
            # Transition to GameOverMenu
            if self.death_animation_timer >= self.death_animation_duration:
                self.screen(
                    f"gameOver;{self.score};{self.timer()};{LeaderboardManage().get_high_score(self.current_question_obj.gamemode)};{self.current_question_obj.gamemode}")
            return

        # Update basket position
        self.basket.update()

        # Spawn apples
        self.spawn_timer -= timeDelta
        if self.spawn_timer <= 0 and len(self.apples) < self.max_apples_on_screen:
            self.spawn_apple()
            self.spawn_timer = self.spawn_interval  # Reset timer

        # Update apples drop speed
        if self.score // 5 > self.last_speed_update_score:
            self.last_speed_update_score = self.score // 5
            for apple in self.apples:
                apple.speed = apple.base_speed + (self.speed_increment * self.last_speed_update_score)

        # Check collision and update position
        collided_apple = None
        for apple in self.apples[:]:
            if self.basket.collides_with(apple):
                collided_apple = apple
                break
            if apple.fall():
                self.apples.remove(apple)

        if collided_apple:
            self.apples.remove(collided_apple)  # Remove the caught apple
            if collided_apple.is_correct:
                self.score += 1
                self.setup_new_question()
            else:
                # Caught wrong apple -> Game over
                self.game_over()

    def game_over(self):
        self.neuroDeath.play()
        self.game_active = False
        self.end_time = time.time()
        self.final_message = f"Oopsie! You got it wrong! The correct answer is:  {self.correct_answer_value}"
        self.show_correct_answer = True
        leaderboard_manager = LeaderboardManage()
        leaderboard_manager.scoreSubmission(self.score, self.current_question_obj.gamemode, self.timer())

    def timer(self):
        if self.start_time is None:
            return "00:00:00"
        current_time = self.end_time if self.end_time else time.time()
        elapsed = current_time - self.start_time
        hours = int(elapsed // 3600)
        minutes = int((elapsed % 3600) // 60)
        seconds = int(elapsed % 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def draw(self):
        # Background
        try:
            self.display.blit(self.background_img, (0, 0))
        except pygame.error as e:
            print(f"Error loading background image: {e}")
            self.display.fill(pygame.Color('#FFE0E3'))  # Pinky Ponky Panky Punky

        # Draw apples
        for apple in self.apples:
            apple.draw(self.display)

        # Draw basket and death animation
        if self.game_active:
            # Draw score and question during gameplay
            score_text = self.font.render(f"Score: {self.score}", True, Constants.COLOR_WHITE)
            self.display.blit(score_text, (925, 35))

            if self.current_question_obj:
                self.current_question_obj.draw_question(self.display, self.font, self.sub_font, self.text_color,
                                                        self.bold_offset)

            if self.start_time is None:
                self.start_time = time.time()

            self.basket.draw(self.display)

        elif self.show_correct_answer:
            # Twinkle twinkle little star
            if self.basket_visible:
                death_pos = (
                    self.basket.rect.centerx - self.basket.death_img.get_width() // 2,
                    self.basket.rect.centery - self.basket.death_img.get_height() // 2
                )
                self.display.blit(self.basket.death_img, death_pos)
            else:
                # Draw the flipped death image
                death_pos = (
                    self.basket.rect.centerx - self.basket.death_img_right.get_width() // 2,
                    self.basket.rect.centery - self.basket.death_img_right.get_height() // 2
                )
                self.display.blit(self.basket.death_img_right, death_pos)

            # Draw game over message
            game_over_surf = self.font.render(self.final_message, True, Constants.COLOR_BLACK)
            game_over_rect = game_over_surf.get_rect(center=(Constants.SCREEN_WIDTH // 2, Constants.SCREEN_HEIGHT // 2))
            text_background = pygame.Surface((game_over_rect.width + 20, game_over_rect.height + 20))
            text_background.fill((255, 255, 255))
            text_background.set_alpha(100)
            text_background_rect = text_background.get_rect(center=game_over_rect.center)
            self.display.blit(text_background, text_background_rect.topleft)
            self.display.blit(game_over_surf, game_over_rect)

        if self.paused and self.pause_menu:
            self.pause_menu.draw()

        self.manager.draw_ui(self.display)
        pygame.display.update()

    def switch_music(self, song_path, Name, time_delta):
        if self.music != Name:
            pygame.mixer.music.fadeout(3000)
            self.music_fade += time_delta
            if self.music_fade >= self.music_fade_duration:
                pygame.mixer.music.load(song_path)
                pygame.mixer.music.play(-1, fade_ms=3000)
                self.music = Name
                self.music_fade = 0
