import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """Manage the player's ship."""

    def __init__(self, ai_game):
        super().__init__()

        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load BMP ship.
        self.image = pygame.image.load(
            "images/ship.bmp"
        ).convert()

        # Make the gray background transparent.
        self.image.set_colorkey(
            self.image.get_at((0, 0))
        )

        self.rect = self.image.get_rect()

        self.rect.midbottom = self.screen_rect.midbottom

        self.x = float(self.rect.x)

        self.moving_right = False
        self.moving_left = False

    def update(self):

        if (
            self.moving_right
            and self.rect.right < self.screen_rect.right
        ):
            self.x += self.settings.ship_speed

        if (
            self.moving_left
            and self.rect.left > 0
        ):
            self.x -= self.settings.ship_speed

        self.rect.x = self.x

    def center_ship(self):

        self.rect.midbottom = self.screen_rect.midbottom

        self.x = float(self.rect.x)

    def blitme(self):

        self.screen.blit(
            self.image,
            self.rect
        )