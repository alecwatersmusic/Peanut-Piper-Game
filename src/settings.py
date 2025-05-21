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

        # Peanut Settings
        self.peanut_speed = 2.0
        self.peanut_width = 3
        self.peanut_height = 15
        self.peanut_color = (60,60,60)
        self.peanuts_allowed = 3