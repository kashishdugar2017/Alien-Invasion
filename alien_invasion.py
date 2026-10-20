import sys
from time import sleep

import pygame

from settings import Settings
from ship import Ship
from game_stats import GameStats
from scoreboard import Scoreboard
from bullet import Bullet
from alien import Alien
from button import Button


class AlienInvasion:
    """Overall class to manage the game."""

    def __init__(self):
        """Initialize the game and create game resources."""

        pygame.init()

        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (
                self.settings.screen_width,
                self.settings.screen_height
            )
        )

        pygame.display.set_caption("Alien Invasion")

        self.background = pygame.image.load(
            "images/space.png"
        ).convert()

        self.background = pygame.transform.scale(
            self.background,
            (
                self.settings.screen_width,
                self.settings.screen_height
            )
        )

        self.stats = GameStats(self)

        self.sb = Scoreboard(self)

        self.ship = Ship(self)

        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        self.stats.game_active = False

        self.play_button = Button(
            self,
            "Play"
        )

    def run_game(self):
        """Start the main game loop."""

        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

            self.clock.tick(60)

    def _check_events(self):
        """Respond to keyboard and mouse events."""

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
        """Start a new game when Play is clicked."""

        button_clicked = (
            self.play_button.rect.collidepoint(
                mouse_pos
            )
        )

        if button_clicked and not self.stats.game_active:

            self.settings.initialize_dynamic_settings()

            self.stats.reset_stats()

            self.sb.prep_score()
            self.sb.prep_high_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            self.stats.game_active = True

            self.bullets.empty()
            self.aliens.empty()

            self._create_fleet()
            self.ship.center_ship()

            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Respond to key presses."""

        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True

        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True

        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases."""

        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False

        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a bullet."""

        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update bullets and check collisions."""

        self.bullets.update()

        for bullet in self.bullets.copy():

            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""

        collisions = pygame.sprite.groupcollide(
            self.bullets,
            self.aliens,
            True,
            True
        )

        if collisions:

            for aliens in collisions.values():
                self.stats.score += (
                    self.settings.alien_points
                    * len(aliens)
                )

            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:

            self.bullets.empty()

            self._create_fleet()

            self.settings.increase_speed()

            self.stats.level += 1

            self.sb.prep_level()

    def _ship_hit(self):
        """Respond when an alien hits the ship."""

        if self.stats.ships_left > 0:

            self.stats.ships_left -= 1

            self.sb.prep_ships()

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            sleep(0.5)

        else:

            self.stats.game_active = False

            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check if aliens reached the bottom."""

        for alien in self.aliens.sprites():

            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

    def _update_aliens(self):
        """Update alien positions."""

        self._check_fleet_edges()

        self.aliens.update()

        if pygame.sprite.spritecollideany(
            self.ship,
            self.aliens
        ):
            self._ship_hit()

        self._check_aliens_bottom()

    def _create_fleet(self):
        """Create the alien fleet."""

        alien = Alien(self)

        alien_width, alien_height = alien.rect.size

        current_x = alien_width
        current_y = alien_height

        while current_y < (
            self.settings.screen_height
            - 3 * alien_height
        ):

            while current_x < (
                self.settings.screen_width
                - 2 * alien_width
            ):

                self._create_alien(
                    current_x,
                    current_y
                )

                current_x += alien_width * 2

            current_x = alien_width
            current_y += alien_height * 2

    def _create_alien(self, x_position, y_position):
        """Create one alien."""

        alien = Alien(self)

        alien.rect.x = x_position
        alien.rect.y = y_position

        alien.x = float(alien.rect.x)

        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Check whether the fleet reached an edge."""

        for alien in self.aliens.sprites():

            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the fleet and reverse direction."""

        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.alien_drop_speed

        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Draw everything on the screen."""

        self.screen.blit(
            self.background,
            (0, 0)
        )

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.ship.blitme()

        self.aliens.draw(self.screen)

        self.sb.show_score()

        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()