# Import modules
import sys
import os
import pygame

class Basket:
    """
    Define the basket mechanism.
    """
    def __init__(self, game):
        """
        Initialize a basket for player's movement.
        :param game: The game instance that basket belongs to.
        """
        self.game = game
        self.speed = 10 # Set movement speed to 10

        try: # Load basket image
            self.img = pygame.image.load("../Assets/Character/NeuroAlive.png").convert_alpha()
        except pygame.error as e:
            print(f"Error loading basket image: {e}")

        # Create left and right image
        self.img_left = self.img
        self.img_right = pygame.transform.flip(self.img_left, True, False)
        # Create left and right image for death animation
        self.death_img = pygame.image.load("../Assets/Character/NeuroDeath.png").convert_alpha()
        self.death_img_right = pygame.transform.flip(self.death_img, True, False)
        # Get dimension of the basket image
        self.width = self.img.get_width()
        self.height = self.img.get_height()

        # Set rect for the initial basket position (bottom of the screen)
        self.rect = pygame.Rect(
            1080 // 2 - self.width // 2,
            640 - self.height - 10,
            self.width,
            self.height
        )

        # Get mask for collision detect
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, screen):
        """
		Draw the basket.
        :param screen: The pygame screen surface to draw basket.
        """
        screen.blit(self.img, self.rect)

    def update(self):
        """
		Updates the basket position based on player's input.
        """
        keys = pygame.key.get_pressed() # Get the player's keyboard's key
        new_img_position = False # Check if position is moved

        # Move left
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 0:
            self.img = self.img_left
            new_img_position = True
            self.rect.x -= self.speed
        # Move right
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < 1080:
            self.img = self.img_right
            new_img_position = True
            self.rect.x += self.speed

        # Update basket position
        if new_img_position:
            self.mask = pygame.mask.from_surface(self.img)

    def collides_with(self, other_sprite):
        """
		Check collision between basket and other sprites (apples).
        :param other_sprite: The sprite to check collision with (apple).
        :return: True if a collision occurs, false otherwise.
        """
        # Check if other sprites has mask and rect
        if not hasattr(other_sprite, 'rect') or not hasattr(other_sprite, 'mask'):
            print(f"Error checking collisions: {other_sprite} missing rect or mask.")
            return False

        # Calculate offset between basket and other sprites
        offset_x = other_sprite.rect.x - self.rect.x
        offset_y = other_sprite.rect.y - self.rect.y
        # Check collision using mask
        collision_point = self.mask.overlap(other_sprite.mask, (offset_x, offset_y))
        return collision_point is not None # Return true if a collision happened
