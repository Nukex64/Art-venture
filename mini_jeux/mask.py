#Projet : Art'Venture
#Auteurs : Anthony Ibanez-Esteban, Raphaël Prost, Aëlys-Coleen Surma Valtaer, Louis Gagne, Mathéo Faure

import pygame

from carte import Carte
from enemy import Enemy


class Car(Enemy):
    def __init__(self, src, x, y):
        super().__init__(src, x, y) #src = image bas voiture
        self.speed = 2

class Mask(Carte):
    """
    un véhicule (voiture) interagit avec le joueur, et si une collision se produit,
    le jeu se termine. Le jeu utilise un système de cartes et de gestion d'ennemis pixel par pixel
    pour des collision parfaite
    """
    def __init__(self):
        super().__init__("map/road.tmx")
        self.image = pygame.image.load(self.get_url("img/test.png"))

        self.player.speed = 3

        self.car = Car(self.image, 0, 0)
        self.groupe.add(self.car)


    def add_verif(self):
        if self.sprite_collision(self.car):
            self.game_over()

    def add_draw(self, screen):
        pass


    def game_over(self):
        self.tp(275, 360)

