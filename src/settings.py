class Settings:
    """A class to store all settings for Peanut Piper."""

    def __init__(self):
        """Initializes the game's static settings."""
        # Screen Settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (50,230,50)

        # Piper Settings
        self.piper_limit = 3

        # Peanut Settings
        self.peanut_width = 3
        self.peanut_height = 15
        self.peanut_color = (60,60,60)
        self.peanuts_allowed = 3

        # Rat settings
        self.fleet_drop_speed = 10

        # How quickly the game speeds up
        self.speedup_scale = 1.1
        # How quickly the rat point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 1.5
        self.peanut_speed = 2.5
        self.rat_speed = 1.0

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Scoring settings
        self.rat_points = 50

    def increase_speed(self):
        """Increase speed settings and rat point values."""
        self.piper_speed *= self.speedup_scale
        self.peanut_speed *= self.speedup_scale
        self.rat_speed *= self.speedup_scale

        self.rat_points = int(self.rat_points * self.score_scale)