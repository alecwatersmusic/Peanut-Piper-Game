import sys

import pygame

from settings import Settings
from piper import Piper
from peanut import Peanut
from rat import Rat

class PeanutPiper: 
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()

        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Peanut Piper")

        self.piper = Piper(self)
        self.peanuts = pygame.sprite.Group()
        self.rats = pygame.sprite.Group()

        self._create_fleet()

        # Set the background color.
        self.bg_color = (50,230,50)

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # Watch for keyboard and mouse events.
            self._check_events()
            self.piper.update()
            self._update_peanuts()
            self._update_rats()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.piper.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.piper.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_peanut()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.piper.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.piper.moving_left = False

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.bg_color)
        for peanut in self.peanuts.sprites():
            peanut.draw_peanut()
        self.piper.blitme()
        self.rats.draw(self.screen)

        pygame.display.flip()

    def _fire_peanut(self):
        """Create a new Peanut and add it to the Peanuts group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_peanut = Peanut(self)
            self.peanuts.add(new_peanut)

    def _update_peanuts(self):
        """Update position of Peanuts and get rid of old Peanuts."""
        # Update Peanut positions.
        self.peanuts.update()

        # Get rid of Peanuts that have disappeared.
        for peanut in self.peanuts.copy():
            if peanut.rect.bottom <= 0:
                self.peanuts.remove(peanut)
            print(len(self.peanuts))

    def _create_fleet(self):
        """Create the fleet of rats."""
        # Create a rat and keep adding rats until there's no room left.
        # Spacing between rats is one rat width and one rat height.
        rat = Rat(self)
        rat_width, rat_height = rat.rect.size

        current_x, current_y = rat_width, rat_height
        while current_y < (self.settings.screen_height - 3 * rat_height):
            while current_x < (self.settings.screen_width - 2 * rat_width):
                self._create_rat(current_x, current_y)
                current_x += 2 * rat_width

        # Finished a row; reset x value, and increment y value.
        current_x = rat_width
        current_y += 2 * rat_height

    def _create_rat(self, x_position, y_position):
        """Create an alien and place it in the row."""
        new_rat = Rat(self)
        new_rat.x = x_position
        new_rat.rect.x = x_position
        new_rat.rect.y = y_position
        self.rats.add(new_rat)

    def _update_aliens(self):
        """Update the positions of all rats in the fleet."""
        self.rats.update()

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = PeanutPiper()
    ai.run_game()