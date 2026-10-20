import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Represent a single alien."""

    def __init__(self, ai_game):
        super().__init__()

        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load BMP alien.
        self.image = pygame.image.load(
            "images/alien.bmp"
        ).convert()

        # Make the gray background transparent.
        self.image.set_colorkey(
            self.image.get_at((0, 0))
        )

        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def check_edges(self):

        screen_rect = self.screen.get_rect()

        if self.rect.right >= screen_rect.right:
            return True

        if self.rect.left <= 0:
            return True

        return False

    def update(self):

        self.x += (
            self.settings.alien_speed
            * self.settings.fleet_direction
        )

        self.rect.x = self.x