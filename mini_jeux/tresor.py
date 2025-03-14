import math
from logging.config import listen

import pyscroll

from carte import Carte
from enemy import Enemy
import pygame

class Tresor(Carte):
    def __init__(self):
        super().__init__("map/maptresortest.tmx") # on donne la map
        self.tresors = self.points_par_classe("tresor")
        self.son01 = pygame.mixer.Sound("sounds/bip.mp3")
        self.frame = 0
        self.lastbip = 1
        self.bip = 1
        self.groupe2 = pyscroll.PyscrollGroup(map_layer=self.map_layer,
                                             default_layer=2)  # groupe de toutes les images pour pygame (default_layer = couche du joueur)
        self.groupe2.add(self.player)  # rajoute le joueur au groupe d'images

    def add_draw(self,screen):
        self.groupe2.draw(screen)
        self.getraytresor(screen)

    def add_verif(self):
        self.frame += 1



    def ray(self,screen,coord, ray=True):
        x2, y2 = self.fixe_coord(coord)
        x1, y1 = self.fixe_coord(self.player.rect.center)
        vx, vy = x2 - x1, y2 - y1
        norm = math.sqrt(vx ** 2 + vy ** 2)
        vx, vy = vx / (norm+0.0001), vy / (norm+0.0001)
        x, y = x1 + vx * 75, y1 + vy * 75
        if ray:
            pygame.draw.line(screen, 'red', (x1, y1), (x,y), 1)
        return norm
    def getraytresor(self,screen):
        liste = []
        coord = (0,0)
        pluspetit = 8000
        for tresor in self.tresors:
            liste.append(self.ray(screen,tresor,False))
            if self.ray(screen,tresor,False) < pluspetit:
                pluspetit=self.ray(screen,tresor,False)
                coord=tresor
        if self.bip == self.frame or round(min(liste)*0.75) < self.bip-self.lastbip-round(min(liste)*0.75)+10 :
            pygame.mixer.Sound.play(self.son01)
            self.bip = self.frame
            self.bip, self.lastbip = self.bip + round(min(liste) * 0.75), self.bip
        pygame.draw.circle(screen,((255-min(255,max(0,min(liste)))),(min(255,max(0,min(liste)))),0),self.fixe_coord(self.player.rect.center),30,4)
        self.ray(screen, coord)