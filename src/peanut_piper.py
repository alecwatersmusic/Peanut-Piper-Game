import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
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

        self.screen = pygame.display.set_mode(
            self.settings.screen_width, self.settings.screen_height)
        pygame.display.set_caption("Peanut Piper")

        # Create an instance to store game statistics, and a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.piper = Piper(self)
        self.peanuts = pygame.sprite.Group()
        self.rats = pygame.sprite.Group()

        self._create_fleet()

        # Set the background color.
        self.bg_color = (50,230,50)

        # Start Peanut Piper in an inactive state.
        self.game_active = False

        # Make the Play button.
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.game_active:
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
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # Reset the game settings.
            self.settings.initialize_dynamic_settings()
            
            # Reset the game statistics.
            self.stats.reset_stats()
            self.sb.prep_score()
            self.game_active = True

            # Get rid of any remaining Peanuts and rats.
            self.peanuts.empty()
            self.rats.empty()

            # Create a new fleet and center the piper.
            self._create_fleet()
            self.piper.center_piper()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

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

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.game_active:
            self.play_button.draw_button()

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

        self._check_peanut_rat_collisions()

    def _check_peanut_rat_collisions(self):
        """Respond to Peanut-rat collisions."""
        # Remove any Peanuts and rats that have collided.
        collisions = pygame.sprite.groupcollide(
            self.peanuts, self.rats, True, True)
        
        if collisions:
            for rats in collisions.values():
                self.stats.score += self.settings.rat_points * len(rats)
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_pipers()
            self.sb.check_high_score()
        
        if not self.rats:
            # Destroy existing Peanuts and create new fleet.
            self.peanuts.empty()
            self._create_fleet()
            self.settings.increase_speed()

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

    def _update_rats(self):
        """Check if the fleet is at an edge, then update positions."""
        self._check_fleet_edges()
        self.rats.update()

        # Look for rat-piper collisions.
        if pygame.sprite.spritecollideany(self.piper, self.rats):
            self._piper_hit()

        # Look for rats hitting the bottom of the screen.
        self._check_rats_bottom()

    def _check_fleet_edges(self):
        """Respond appropriately if any rats have reached an edge."""
        for rat in self.rats.sprites():
            if rat.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for rat in self.rats.sprites():
            rat.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_rats_bottom(self):
        """Check if any rats have reached the bottom of the screen."""
        for rat in self.rats.sprites():
            if rat.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if the piper got hit.
                self._piper_hit()
                break

    def _piper_hit(self):
        """Respond to the piper being bit by a rat."""
        if self.stats.pipers_left > 0:
            # Decrement pipers left, and update scoreboard.
            self.stats.pipers_left -= 1
            self.sb.prep_pipers()

            # Get rid of remaining Peanuts and rats.
            self.peanuts.empty()
            self.rats.empty()

            # Create a new fleet and center the piper.
            self._create_fleet()
            self.piper.center_piper()

            # Pause.
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = PeanutPiper()
    ai.run_game()