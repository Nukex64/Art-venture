#Projet : Art'Venture
#Auteurs : Anthony Ibanez-Esteban, Raphaël Prost, Aëlys-Coleen Surma Valtaer, Louis Gagne, Mathéo Faure

import math

import pygame

from carte import Carte
from enemy import Enemy


class Ville(Carte):
    """
    Ce n'est pas un mini jeux juste un test de truc random
    (on peut peut etre en fair un plus tard)
    """
    def __init__(self):
        super().__init__("map/map.tmx")
        self.tp_1 = self.objet_par_nom('tp_1')
        self.tp_2 = self.objet_par_nom("tp_2")
        self.tp_3 = self.objet_par_nom("tp_3")
        self.text_1 = self.font.render("Je suis un text fixe", True, (0, 0, 0))
        self.text_2 = self.font.render("Je suis un text d'UI", True, (0, 0, 0))

        self.fire = Enemy("img/fire.png", 10, 10)
        self.fire.speed = 1
        self.fire.direction = 0
        self.groupe.add(self.fire)


        self.car = Enemy("img/car.png", 100, 184)
        self.car.speed = 1
        self.car_img = pygame.image.load("img/car.png")
        self.car.direction = 0
        self.groupe.add(self.car)




    def add_draw(self, screen):
        screen.blit(self.text_1, self.fixe_coord((25, 25)))
        screen.blit(self.text_2, (625, 570))
        self.ray()

    def add_verif(self):
        if self.touche("RETURN") and not self.objetif:
            if self.collision(self.tp_1):
                self.objetif =  "Road"
            if self.collision(self.tp_2):
                self.objetif = "Parcours"

            if self.collision(self.tp_3):
                self.objetif = "Laby"

        if self.touche("KP_6"):
            self.fire.regarder(90)


        if self.collision(self.fire.rect):
            self.fire.x, self.fire.y = 5, 5
            self.fire.regarder(90)

        if self.car.rect.collidelist(self.mur) > -1:
            self.car.invers_direction()

        if self.collision(self.car.rect):
            self.tp(250, 250)


        self.car.move("z")
        self.fire.viser(self.player.rect.center)


        self.timer += 1


    def ray(self):
        x2, y2 = pygame.mouse.get_pos()
        x1, y1 = self.fixe_coord(self.player.rect.center)
        vx, vy = x2-x1, y2-y1
        norm = math.sqrt(vx**2 + vy**2)
        vx, vy = vx/norm, vy/norm
        x, y = x1+vx*75, y1+vy*75
        #pygame.draw.line(screen, 'red', (x1, y1), (x,y), 1)
        return x1, x2, y1, y2, x, y


    def __str__(self):
        return "Ville"
