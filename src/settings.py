class Settings:
    """A class to store all settings for Peanut Piper."""

    def __init__(self):
        """Initializes the game's settings."""
        # Screen Settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (50,230,50)

        # Piper Settings
        self.piper_speed = 1.5
        self.piper_limit = 3

        # Peanut Settings
        self.peanut_speed = 2.5
        self.peanut_width = 3
        self.peanut_height = 15
        self.peanut_color = (60,60,60)
        self.peanuts_allowed = 3

        # Rat settings
        self.rat_speed = 1.0
        self.fleet_drop_speed = 10
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1