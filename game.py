import pygame as pg
from sprites import Creature, Food
from settings import *
from random import random, uniform
from statistics import mean

class Game:

    def __init__(self):
        pg.init()
        pg.display.set_caption("Evolutionary Algorithm")
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.done = False

        # Groups
        self.sprites = pg.sprite.Group()
        self.population = pg.sprite.Group()
        self.food = pg.sprite.Group()

        # User events
        pg.time.set_timer(pg.USEREVENT, DAY_LENGTH)
        pg.time.set_timer(pg.USEREVENT + 1, FOOD_RATE)

        # Days
        self.day = 1

        # Create food
        for _ in range(FOOD_SIZE):
            Food(self)

        # Create population
        for _ in range(POPULATION_SIZE):
            Creature(self)

    def run(self):
        while not self.done:
            self.events()
            self.update()
            self.draw()
            pg.display.flip()
            self.clock.tick(FPS)

    def events(self):
        # Listen for mouse and keyboard events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            # New day event
            if event.type == pg.USEREVENT:
                self.day += 1
                # Breed new creature
                for creature in self.population:
                    # Mutate creature
                    speed = uniform(creature.speed - 1, creature.speed + 1)
                    speed = max(1, min(speed, 10))
                    Creature(self, speed=speed)
            if event.type == pg.USEREVENT + 1:
                Food(self)

    def update(self):
        self.sprites.update()
        # Creature eat food
        collision = pg.sprite.collide_rect_ratio(0.8)
        for creature in pg.sprite.groupcollide(self.population, self.food, False, True, collision):
            # Increment health of creature
            creature.health = min(creature.health + FOOD_HEALTH, MAX_HEALTH)

    def draw(self):
        # Fill screen gray
        self.screen.fill(GRAY)
        self.sprites.draw(self.screen)
        # Draw Text
        surface = pg.Surface((WIDTH, 60), pg.SRCALPHA)
        surface.fill((0, 0, 0, 128))
        self.screen.blit(surface, (0, 0))
        self.draw_text(f"Average Speed: {mean([creature.speed for creature in self.population]):.2f}", 22, WHITE, WIDTH - 230, 20)
        self.draw_text(f"Day: {self.day}", 22, WHITE, 10, 20)

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(pg.font.get_default_font(), size)
        surface = font.render(text, True, color)
        rect = surface.get_rect(topleft=(x, y))
        self.screen.blit(surface, rect)
