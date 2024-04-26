from pygame import SRCALPHA
import pygame
from pygame.math import Vector2
from pygame.sprite import Group
from pygame.sprite import Sprite
from pygame.surface import Surface
from pygame.draw import rect as draw_rect
from pygutils.timer import Timer

from entity import Entity


class HealthBar(Sprite):
    def __init__(self, entity: Entity, *groups: list[Group]) -> None:
        super().__init__(*groups)

        self.entity = entity

        self.image = Surface((self.entity.rect.width // 2, 16), SRCALPHA)
        self.rect = self.image.get_rect(
            midbottom=Vector2(self.entity.rect.midtop) + Vector2(0, -15)
        )

        self.alive_timer = Timer(3000)
        self.alive_timer.activate()

    def keep_alive(self) -> None:
        """Keep the object alive by deactivating and then activating
        the alive timer.
        """
        self.alive_timer.deactivate()
        self.alive_timer.activate()

    def update(self, dt) -> None:
        """
        Updates the health bar image based on the current health of the
        entity.

        This function calculates the percentage of the entity's health
        and updates the health bar image accordingly. If the entity's
        health is greater than 50% and the alive timer is not active,
        the health bar is killed. If the entity's health is 0, the
        health bar is also killed. Otherwise, the health bar is drawn
        with two rectangles: a black background rectangle and a colored
        rectangle representing the health percentage.
        """
        health_percent = self.entity.health / self.entity.max_health

        if (
            not self.alive_timer.active and health_percent > 0.5
        ) or health_percent == 0:
            self.kill()
            return

        draw_rect(
            surface=self.image,
            color=(0, 0, 0),
            rect=(0, 0, self.entity.rect.width // 2, 16),
            border_radius=5,
        )

        draw_rect(
            surface=self.image,
            color=(214, 75, 41),
            rect=(3, 3, self.entity.rect.width // 2 * health_percent - 6, 10),
            border_radius=3,
        )

        self.rect = self.image.get_rect(
            midbottom=Vector2(self.entity.rect.midtop) + Vector2(0, -15)
        )

        self.alive_timer.update()



class AmmoBar(Sprite):
    def __init__(self, entity: Entity, *groups: list[Group]) -> None:
        super().__init__(*groups)
        self.alive_timer = Timer(3000)
        self.alive_timer.activate()
        self.entity = entity

        self.image = Surface((self.entity.rect.width // 2, 16), SRCALPHA)
        self.rect = self.image.get_rect(
            midbottom=Vector2(self.entity.rect.midtop) + Vector2(0, -15)
        )

        self.reload_timer = self.entity.reload_time
    def keep_alive(self) -> None:
        """Keep the object alive by deactivating and then activating
        the alive timer.
        """
        self.alive_timer.deactivate()
        self.alive_timer.activate()
    def update(self, dt) -> None:
        """
        Updates the ammo bar image based on the remaining reload time of the
        entity.

        This function calculates the percentage of the remaining reload time
        and updates the ammo bar image accordingly. If the reload time is 0,
        the ammo bar is killed. Otherwise, the ammo bar is drawn with two
        rectangles: a black background rectangle and a colored rectangle
        representing the remaining reload time as a percentage.
        """
        reload_time = self.entity.reload_time  # Reload time in milliseconds
        reload_time_passed = pygame.time.get_ticks() - self.entity.last_shot_time
        ammo_percent = reload_time_passed / reload_time
        # ammo_percent = self.reload_timer.percent_left

        if ammo_percent >= 1:
            self.kill()
            return

        draw_rect(
            surface=self.image,
            color=(0, 0, 0),
            rect=(0, 0, self.entity.rect.width // 2, 16),
            border_radius=5,
        )

        draw_rect(
            surface=self.image,
            color=(255, 0, 0),
            rect=(3, 3, self.entity.rect.width // 2 * ammo_percent - 6, 10),
            border_radius=3,
        )

        self.rect = self.image.get_rect(
            midbottom=Vector2(self.entity.rect.midtop) + Vector2(0, -15)
        )
