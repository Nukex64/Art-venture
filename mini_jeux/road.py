#Projet : Art'Venture
#Auteurs : Anthony Ibanez-Esteban, Raphaël Prost, Aëlys-Coleen Surma Valtaer, Louis Gagne, Mathéo Faure

from random import randint

import pygame

from carte import Carte
from enemy import Enemy


class Car(Enemy):
    def __init__(self, src, x, y, image_toit, speed=2):
        super().__init__(src, x, y) #src = image bas voiture
        self.speed = speed
        self.toit = image_toit #src = image du tois (hors hit box)


class Road(Carte):
    def __init__(self):
        super().__init__("map/road.tmx")
        self.tp_1 = self.objet_par_nom('tp_1')

        self.image_sheet = pygame.image.load("img/car_sheet.png")
        self.images = {1:self._cut_img_bas(0, 6), 4:self._cut_img_bas(37, 6),
                       2:self._cut_img_bas(0, 31), 5:self._cut_img_bas(37, 31),
                       3:self._cut_img_bas(0, 56), 6:self._cut_img_bas(37, 56),}

        self.images_toits = {1: self._cut_img_haut(0, 0), 4: self._cut_img_haut(37, 0),
                       2: self._cut_img_haut(0, 25), 5: self._cut_img_haut(37, 25),
                       3: self._cut_img_haut(0, 50), 6: self._cut_img_haut(37, 50), }

        self.cars = []
        self.spawn_car()
        self.difficulty = 25
        self.counter = self.difficulty
        self.spawn = self.objet_par_nom("spawn").midbottom
        self.player.speed = 1.5

    def _cut_img_bas(self, x, y):
        image = pygame.Surface([36, 19])
        image.blit(self.image_sheet, (0, 0), (x, y, 36, 25))
        image = pygame.transform.scale(image, (36*1.2,19*1.2))
        image.set_colorkey((0, 0, 0))
        return image

    def _cut_img_haut(self, x, y):
        image = pygame.Surface([35, 5])
        image.blit(self.image_sheet, (0, 0), (x, y, 35, 5))
        image = pygame.transform.scale(image, (35*1.2*2,5*1.2*2))
        image.set_colorkey((0, 0, 0))
        return image

    def add_verif(self):
        if self.counter <= 0:
            self.counter = self.difficulty
            self.spawn_car()
        self.counter -= 1

        if self.multi_collision(self.cars):
            self.game_over()


    def add_draw(self, screen):
        for car in self.cars:
            car.avancer()
            screen.blit(car.toit, self.fixe_coord((car.rect.x, car.rect.y - 5)))
            if car.coord[0] > 600 or car.coord[0] < -100:
                self.cars.remove(car)
                car.kill()

            if self.player.coord[1] < 50:
                self.objetif = "Ville"

            if self.collision(self.tp_1):
                self.objetif = "Ville"

    def spawn_car(self):
            route = randint(0, 1)
            x = randint(4, 6)
            car = Car(self.images[x], -100, 101 + route*128, self.images_toits[x], 5-route)
            self.groupe.add(car)
            self.cars.append(car)

            route = randint(2, 3)
            x = randint(4, 6)
            car = Car(self.images[x], -100, 101 + route * 128, self.images_toits[x], 5-route)
            self.groupe.add(car)
            self.cars.append(car)

            route = randint(0, 1)
            x = randint(1, 3)
            car = Car(self.images[x], 600, 165 + route*128, self.images_toits[x], 5-route)
            car.regarder(180)
            self.groupe.add(car)
            self.cars.append(car)

            route = randint(2, 3)
            x = randint(1, 3)
            car = Car(self.images[x], 600, 165 + route * 128, self.images_toits[x], 5-route)
            car.regarder(180)
            self.groupe.add(car)
            self.cars.append(car)


    def game_over(self):
        self.tp(self.spawn[0], self.spawn[1])

    def __str__(self):
        return "Road"

