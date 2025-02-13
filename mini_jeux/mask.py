from carte import Carte
from enemy import Enemy
import pygame
from random import randint

class Car(Enemy):
    def __init__(self, src, x, y):
        super().__init__(src, x, y) #src = image bas voiture
        self.speed = 2
        self.mask = pygame.mask.from_surface(self.image)

class Mask(Carte):
    def __init__(self):
        super().__init__("map/road.tmx")
        self.image = pygame.image.load("img/test.png")

        self.player.speed = 3

        self.car = Car(self.image, 0, 0)
        self.groupe.add(self.car)


    def add_verif(self):
        offset = self.car.rect.x - self.player.feet.x, self.car.rect.y - self.player.feet.y
        if self.player.mask.overlap(self.car.mask, offset):
            self.game_over()

    def add_draw(self, screen):
        pass


    def game_over(self):
        self.tp(275, 360)

