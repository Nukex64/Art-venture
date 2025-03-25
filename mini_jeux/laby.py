#Projet : Art'Venture
#Auteurs : Anthony Ibanez-Esteban, Raphaël Prost, Aëlys-Coleen Surma Valtaer, Louis Gagne, Mathéo Faure

from random import randint

import pygame

import settings
from carte import Carte
from enemy import Enemy


class Laby(Carte):
    """
    Ce n'est pas un mini jeux juste un test de truc random
    (on peut peut etre en fair un plus tard)
    """
    def __init__(self):
        super().__init__("map/map.tmx")
        self.tp_1 = self.objet_par_nom('tp_1')
        self.tp_2 = self.objet_par_nom("tp_2")
        self.tp_3 = self.objet_par_nom("tp_3")
        self.radius = 110
        self.groupe.center((self.tmx_data.width,self.tmx_data.height))
        self.timer = 0
        self.orageframe = self.timer
        self.shadingstorm = 120
        self.backcolor = (0, 0, 0)
        self.roundcolor = (0, 0, 0, 0)
        self.enemytexture = Enemy("img/fire.png",30,30)
        self.groupe.add(self.enemytexture)
        self.map_layer.zoom = min(800/(16*self.tmx_data.width),600/(16*self.tmx_data.height))
        print(min(800/self.tmx_data.width,600/self.tmx_data.height))
        self.canbullet = False
        self.docenter = False

    def __str__(self):
        return "Laby"
    def eventenemy(self):
        self.radius = settings.FPS*2 #tps * sec
    def add_draw(self, screen):
        mask = pygame.Surface((800, 600), pygame.SRCALPHA)
        coord = self.fixe_coord(self.player.rect.center)
        mask.fill(self.backcolor)
        if self.roundcolor[3] != 120:
            for i in range(0,self.radius,2):
                pygame.draw.circle(mask, (self.roundcolor[0],self.roundcolor[1],self.roundcolor[2],max((255-(255*(i/self.radius))),0)), (coord[0], coord[1]), self.radius-i)
        else :
            pygame.draw.circle(mask, self.roundcolor, (coord[0], coord[1]),self.radius)
        screen.blit(mask, (0, 0))
    def add_verif(self):
        if self.radius !=50:
            self.radius -= 1
        if self.orageframe <= self.timer:
            self.backcolor = (0,0,0,255)
            self.roundcolor = (0,0,0,0)
        if self.collision(self.enemytexture.rect):
            self.eventenemy()
        self.timer += 1
        self.orage()
    def orage(self):
        if randint(0,3600) == 1:
            self.backcolor = (255,255,0,self.shadingstorm)
            self.roundcolor = (255, 255, 0, self.shadingstorm)
            self.orageframe = self.timer + 15

