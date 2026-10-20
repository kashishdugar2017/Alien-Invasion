import pygame.font
from pygame.sprite import Group

from ship import Ship


class Scoreboard:
    """Display score, high score, level, and ships."""

    def __init__(self, ai_game):
        """Initialize scoreboard."""

        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # White text for space background.
        self.text_color = (255, 255, 255)

        self.font = pygame.font.SysFont(None, 48)
        self.label_font = pygame.font.SysFont(None, 48)

        # Little ships.
        self.ships = Group()

        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Prepare the score."""

        rounded_score = round(
            self.stats.score,
            -1
        )

        score_str = f"{rounded_score:,}"

        self.score_label_image = self.label_font.render(
            "SCORE:",
            True,
            self.text_color
        )

        self.score_label_rect = self.score_label_image.get_rect()

        self.score_image = self.font.render(
            score_str,
            True,
            self.text_color
        )

        self.score_rect = self.score_image.get_rect()

        self.score_rect.right = (
            self.screen_rect.right - 20
        )
        self.score_rect.top = 20

        self.score_label_rect.right = (
            self.score_rect.left - 10
        )
        self.score_label_rect.top = 20

    def prep_high_score(self):
        """Prepare the high score."""

        high_score = round(
            self.stats.high_score,
            -1
        )

        high_score_str = f"{high_score:,}"

        self.high_score_label_image = self.label_font.render(
            "HIGH SCORE:",
            True,
            self.text_color
        )

        self.high_score_label_rect = self.high_score_label_image.get_rect()

        self.high_score_image = self.font.render(
            high_score_str,
            True,
            self.text_color
        )

        self.high_score_rect = (
            self.high_score_image.get_rect()
        )

        self.high_score_rect.centerx = (
            self.screen_rect.centerx + 70
        )
        self.high_score_rect.top = 20

        self.high_score_label_rect.right = (
            self.high_score_rect.left - 10
        )
        self.high_score_label_rect.top = 20

    def prep_level(self):
        """Prepare the level."""

        level_str = str(
            self.stats.level
        )

        self.level_label_image = self.label_font.render(
            "LEVEL:",
            True,
            self.text_color
        )

        self.level_label_rect = self.level_label_image.get_rect()

        self.level_image = self.font.render(
            level_str,
            True,
            self.text_color
        )

        self.level_rect = (
            self.level_image.get_rect()
        )

        self.level_rect.right = (
            self.screen_rect.right - 20
        )
        self.level_rect.top = 70

        self.level_label_rect.right = (
            self.level_rect.left - 10
        )
        self.level_label_rect.top = 70

    def prep_ships(self):
        """Create little ship icons."""

        self.ships.empty()

        for ship_number in range(
            self.stats.ships_left
        ):

            ship = Ship(self.ai_game)

            ship.rect.x = (
                10
                + ship_number
                * (ship.rect.width + 10)
            )

            ship.rect.y = 10

            self.ships.add(ship)

    def show_score(self):
        """Draw all scoreboard information."""

        self.screen.blit(
            self.score_label_image,
            self.score_label_rect
        )

        self.screen.blit(
            self.score_image,
            self.score_rect
        )

        self.screen.blit(
            self.high_score_label_image,
            self.high_score_label_rect
        )

        self.screen.blit(
            self.high_score_image,
            self.high_score_rect
        )

        self.screen.blit(
            self.level_label_image,
            self.level_label_rect
        )

        self.screen.blit(
            self.level_image,
            self.level_rect
        )

        # Draw little ships.
        self.ships.draw(
            self.screen
        )

    def check_high_score(self):
        """Check for a new high score."""

        if self.stats.score > self.stats.high_score:

            self.stats.high_score = (
                self.stats.score
            )

            self.stats.save_high_score()

            self.prep_high_score()