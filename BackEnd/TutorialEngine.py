import sys
import os
import pygame

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from BackEnd.Game import Game


class TutorialEngine(Game):
    def __init__(self, screen, display, manager, music, gamemode: str):
        super().__init__(screen, display, manager, "Snowy", gamemode)

        self.pause_button.disable()

        # Audio
        if music != "Sans":
            pygame.mixer.music.load("../Assets/Audio/Tutorial-Undertale_Sans.ogg")
            pygame.mixer.music.play(-1, fade_ms=3000)

        # TutorialEngine
        self.end_time = 1000
        self.gamemode = gamemode

    def update(self, timeDelta):  # override
        """
        Main tutorial update loop logic with slight changes to follow tutorial standards.
        :param timeDelta: timing nonsense.
        :return: None
        """
        self.manager.update(timeDelta)

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
                self.game_active = True
                self.show_correct_answer = False
                self.death_animation_timer = 0
                self.death_animation_duration = 2
                self.setup_new_question()
            return

        # if not self.game_active:
        #     now = pygame.time.get_ticks()
        #     if now - self.start_time >= self.end_time:
        #         self.final_message = ""
        #         self.game_active = True
        #         self.setup_new_question()
        #     return

        # Update basket position
        self.basket.update()

        # Spawn apples
        self.spawn_timer -= timeDelta
        if self.spawn_timer <= 0 and len(self.apples) < self.max_apples_on_screen:
            self.spawn_apple()
            self.spawn_timer = self.spawn_interval  # Reset timer

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
                # Change to the next game mode using the game_next function
                self.game_next()

            else:
                # Refresh new question with small player animation and audio (if possible)
                self.game_over()

    def game_over(self):  # override
        """
        Game over sequence with changes to cater to tutorial standards (no death only restart).
        :return: None
        """
        # Refresh new question with small player animation and audio (if possible)
        self.final_message = f"Ouch Wrong tutel! The answer is {self.correct_answer_value}."
        self.game_active = False
        self.show_correct_answer = True
        self.start_time = pygame.time.get_ticks()

    def timer(self):  # override
        """
        Not needed as it doesn't calculate time.
        :return: None
        """
        pass  # Removed as its not needed

    def game_next(self):
        """
        Changing between the tutorial game engine and the actual tutorial.
        :return: None
        """
        # Change to the next game mode using the game_next function
        match self.gamemode:
            case "conversion":
                self.screen("tutorial;2;None")
            case "basic_calculation":
                self.screen("tutorial;3;None")
            case "mixed_calculation":
                self.screen("tutorial;4;None")

    def eventCheck(self, event):
        """
        Check any specific game events happened.
        :param event: pygame event variable.
        :return: None
        """
        pass
