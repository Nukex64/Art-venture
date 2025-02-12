import math
from carte import Carte
from enemy import Enemy
import pygame
from settings import *
from random import randint

class Road(Carte):
    def __init__(self):
        super().__init__("map/road.tmx")
        self.image_sheet = pygame.image.load("img/car_sheet.png")
        self.images = {1:self._cut_img(0, 0), 4:self._cut_img(37, 0),
                       2:self._cut_img(0, 25), 5:self._cut_img(37, 25),
                       3:self._cut_img(0, 50), 6:self._cut_img(37, 50),}
        self.cars_d = []
        self.cars_g = []
        self.spawn_car()
        self.difficulty = 25
        self.counter = self.difficulty
        self.mur_g = self.objet_par_nom('mur_g')
        self.mur_d = self.objet_par_nom('mur_d')

        self.player.speed = 1.5

    def _cut_img(self, x, y):
        image = pygame.Surface([36, 25])
        image.blit(self.image_sheet, (0, 0), (x, y, 36, 25))
        image = pygame.transform.scale(image, (36*1.2,25*1.2))
        image.set_colorkey((0, 0, 0))
        return image

    def add_verif(self):
        for car in self.cars_g:
            car.avancer()
            if car.coord[0] > 600:
                car.kill()

        for car in self.cars_d:
            car.avancer()
            if car.coord[0] < -100:
                car.kill()

        if self.counter <= 0:
            print("ok")
            self.counter = self.difficulty
            self.spawn_car()

        self.counter -= 1

        if self.multi_collision(self.cars_g) or self.multi_collision(self.cars_d):
            self.tp(275, 360)

    def add_draw(self, screen):
        pass

    def spawn_car(self):
            route = randint(0, 2)
            x = randint(4, 6)
            car = Enemy(self.images[x], -100, 45 + route*128)
            car.speed = 2
            self.groupe.add(car)
            self.cars_g.append(car)

            route = randint(0, 1)
            x = randint(1, 3)
            car = Enemy(self.images[x], 600, 109 + route*128)
            car.speed = 2
            car.regarder(180)
            self.groupe.add(car)
            self.cars_d.append(car)

