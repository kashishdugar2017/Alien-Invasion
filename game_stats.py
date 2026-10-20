class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize statistics."""

        self.settings = ai_game.settings

        try:
            with open("high_score.txt", "r") as file:
                self.high_score = int(file.read())
        except (FileNotFoundError, ValueError):
            self.high_score = 0

        self.reset_stats()

    def reset_stats(self):
        """Initialize statistics that change during the game."""

        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
        self.game_active = False

    def save_high_score(self):
        """Save high score."""

        with open("high_score.txt", "w") as file:
            file.write(str(self.high_score))