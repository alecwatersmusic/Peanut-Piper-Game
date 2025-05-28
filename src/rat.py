import pygame
from pygame.sprite import Sprite

class Rat(Sprite):
    """A class to represent a single rat in the fleet."""

    def _init_(self, ai_game):
        """Initialize the rat and set its starting position."""
        super()._init_()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the rat image and set its rect attribute.
        self.image = pygame.image.load('Rat.bmp')
        self.rect = self.image.get_rect()

        # Start each new rat near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if rat is at edge of screen."""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    def update(self):
        """Move the rat right or left."""
        self.x += self.settings.rat_speed * self.settings.fleet_direction
        self.rect.x = self.x