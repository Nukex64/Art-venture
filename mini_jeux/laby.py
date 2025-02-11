from random import randint

from carte import Carte
import pygame
import settings
from enemy import Enemy
import random
class Laby(Carte):
    """
    Ce n'est pas un mini jeux juste un test de truc random
    (on peut peut etre en fair un plus tard)
    """
    def __init__(self):
        super().__init__("map/map.tmx")
        self.radius = 100
        self.orageframe = 0
        self.backcolor = (0, 0, 0)
        self.timetorche = 100
        self.enemytexture = Enemy("img/fire.png",30,30)
        self.groupe.add(self.enemytexture)
        self.zoom = settings.ZOOM
    def __str__(self):
        return "Laby"
    def eventenemy(self):
        self.timetorche = settings.FPS*5 #tps * sec
    def add_draw(self, screen):
        mask = pygame.Surface((800, 600), pygame.SRCALPHA)
        coord = self.fixe_coord(self.player.rect.center)
        mask.fill(self.backcolor)
        pygame.draw.circle(mask, (0, 0, 0, 0), (coord[0], coord[1]), self.radius)
        screen.blit(mask, (0, 0))
    def add_verif(self):
        if self.timetorche !=100:
            self.timetorche -= 1
        if self.orageframe != 0:
            self.orageframe -= 1
        if self.orageframe == 0:
            self.backcolor = (0,0,0,255)
            self.radius = self.timetorche
        if self.timetorche == 100:
            self.radius = 100
        if self.collision(self.enemytexture.rect):
            self.eventenemy()
        self.orage()
    def orage(self):
        if randint(0,600) == 1 and self.orageframe == 0:
            self.backcolor = (255,255,0,120)
            self.orageframe = 15
