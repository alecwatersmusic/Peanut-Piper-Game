import pygame

class Piper:
    """A class to manage the piper."""

    def __init__(self, ai_game):
        """Initialize the piper and set its starting position."""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load the piper image and get its rect.
        self.image = pygame.image.load('src/PeanutPiper.bmp')
        self.rect = self.image.get_rect()

        # Start each new piper at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a float for the ship's exact horizontal position.
        self.x = float (self.rect.x)

        # Movement flags; start with a piper that's not moving.
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the piper's position based on the movement flags."""
        # Update the ship's x value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.piper_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.piper_speed

        # Update rect object from self.x.
        self.rect.x = self.x

    def blitme(self):
        """Draw the piper at its current location."""
        self.screen.blit(self.image, self.rect)