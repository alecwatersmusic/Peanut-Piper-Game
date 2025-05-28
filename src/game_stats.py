class GameStats:
    """Track statistics for Peanut Piper."""

    def _init_(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.pipers_left = self.settings.piper_limit