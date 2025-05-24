import pygame
from pygame.sprite import Sprite

class Peanut(Sprite):
    """A class to manage Peanuts fired by the Piper."""

    def _init_(self,ai_game):
        """Create a Peanut object at the Piper's current position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.peanut_color

        # Create a Peanut rect at (0,0) and then set correct position.
        self.rect = pygame.Rect(0,0,self.settings.peanut_width,
                                self.settings.peanut_height)
        self.rect.midtop = ai_game.piper.rect.midtop

        # Store the Peanut's position as a float.
        self.y = float(self.rect.y)

    def update(self):
        """Move the Peanut up the screen."""
        # Update the exact position of the Peanut.
        self.y -= self.settings.peanut_speed
        # Update the rect position.
        self.rect.y = self.y
    
    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen,self.color,self.rect)
