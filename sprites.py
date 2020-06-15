import pygame as pg
import pygame.gfxdraw
from math import atan2, degrees, cos, sin, pi
from random import random
from settings import *

vector2 = pg.math.Vector2

class Creature(pg.sprite.Sprite):

    def __init__(self, game, speed=1):
        super().__init__([game.sprites, game.population])
        # Creature properties
        self.speed = speed
        self.health = MAX_HEALTH
        # Surface
        self.width = 15
        self.height = self.width / 1.5
        self.creature = pg.Surface((self.width, self.height), pg.SRCALPHA)
        pg.draw.polygon(self.creature, GREEN, [(0, 0), (0, self.height), (self.width, self.height // 2)])
        # Image. (Sprite group looks for this attribute to draw)
        self.image = self.creature.copy()
        # Rect. (Sprite group looks for this attribute for positioning)
        self.rect = self.image.get_rect()
        self.pos = vector2(random() * WIDTH, random() * HEIGHT)
        self.vel = vector2(0, 0)
        self.acc = vector2(0, 0)
        # Target for wandering behavior
        self.target = vector2(0, 0)

    def update(self):
        # Update health
        self.health = max(self.health - 5, 0)
        if self.health <= 0: self.kill()
        color = RED.lerp(GREEN, self.health / MAX_HEALTH)
        pg.draw.polygon(self.creature, color, [(0, 0), (0, self.height), (self.width, self.height // 2)])
        # Update target
        theta = random() * 2 * pi
        self.target = self.pos + self.vel * 250 + vector2(cos(theta), sin(theta)) * 30
        # Calculate desired velocity vector
        velocity = (self.target - self.pos).normalize() * self.speed
        # Keep creature away from wall
        if self.pos.x < 0: velocity.x = self.speed
        elif self.pos.x > WIDTH: velocity.x = -self.speed
        elif self.pos.y < 0: velocity.y = self.speed
        elif self.pos.y > HEIGHT: velocity.y = -self.speed
        # Calculate force
        F = velocity - self.vel
        # Update position
        self.acc += F
        self.vel += self.acc
        self.pos += self.vel
        # Rotate image
        angle = degrees(atan2(-self.vel.y, self.vel.x))
        self.image = pg.transform.rotate(self.creature, angle)
        # Reset accerleration
        self.acc = vector2(0, 0)
        self.rect.center = self.pos

class Food(pg.sprite.Sprite):

    def __init__(self, game):
        super().__init__([game.sprites, game.food])
        self.image = pg.Surface((8, 8), pg.SRCALPHA)
        pg.gfxdraw.filled_circle(self.image, 4, 4, 4, BLACK)
        self.rect = self.image.get_rect(center=(random() * WIDTH, random() * HEIGHT))

    def update(self):
        pass
