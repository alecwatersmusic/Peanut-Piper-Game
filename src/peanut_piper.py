import sys

import pygame

from settings import Settings
from piper import Piper

class PeanutPiper: 
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()

        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Peanut Piper")

        self.piper = Piper(self)

        # Set the background color.
        self.bg_color = (50,230,50)

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # Watch for keyboard and mouse events.
            self._check_events()
            self.piper.update()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.piper.moving_right = True
                    elif event.key == pygame.K_LEFT:
                        self.piper.moving_left = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.piper.moving_right = False
                    if event.key == pygame.K_LEFT:
                        self.piper.moving_left = False

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.bg_color)
        self.piper.blitme()

        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = PeanutPiper()
    ai.run_game()