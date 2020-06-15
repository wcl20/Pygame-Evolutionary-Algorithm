import pygame as pg
vector3 = pg.math.Vector3

WIDTH = 800
HEIGHT = 600
FPS = 60

# Colors
WHITE = vector3(255, 255, 255)
GRAY = vector3(214, 214, 214)
BLACK = vector3(97, 97, 97)
RED = vector3(244, 67, 54)
GREEN = vector3(76, 175, 80)

# Creature
MAX_HEALTH = 1000

# Evolutionary Algorithm
POPULATION_SIZE = 10
FOOD_SIZE = 1000
FOOD_HEALTH = 200
FOOD_RATE = 50
DAY_LENGTH = 20000
