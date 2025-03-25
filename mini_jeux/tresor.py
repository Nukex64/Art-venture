#Projet : Art'Venture
#Auteurs : Anthony Ibanez-Esteban, Raphaël Prost, Aëlys-Coleen Surma Valtaer, Louis Gagne, Mathéo Faure

import math

import pygame

from carte import Carte
from tuto import Tuto


class Tresor(Carte):
    def __init__(self):
        super().__init__("map/maptresortest.tmx") # on donne la map
        self.tuto = Tuto()
        self.tresors = self.points_par_classe("tresor")
        self.son01 = pygame.mixer.Sound("sounds/bip.mp3")
        self.frame = 0
        self.lastbip = 1
        self.bip = 1

        self.radar = Radar()
        self.groupe.add(self.radar)

    def add_draw(self,screen):
        if self.tresors:
            self.getraytresor(screen)
            self.trouver_tresor()

    def add_verif(self):
        self.frame += 1
        self.radar.set_middle(self.player.middle)
        if self.touche("RETURN"):
            self.tuto.open("Sed quid est quod in hac causa maxime homines admirentur et reprehendant meum consilium, cum ego idem antea multa decreverim, que magis ad hominis dignitatem quam ad rei publicae necessitatem pertinerent? Supplicationem quindecim dierum decrevi sententia mea. Rei publicae satis erat tot dierum quot C. Mario ; dis immortalibus non erat exigua eadem gratulatio quae ex maximis bellis. Ergo ille cumulus dierum hominis est dignitati tributus.","img/fire.png")


    def ray(self,screen,coord, ray=True):
        x2, y2 = self.fixe_coord(coord)
        x1, y1 = self.fixe_coord(self.player.rect.center)
        vx, vy = x2 - x1, y2 - y1
        norm = math.sqrt(vx ** 2 + vy ** 2)
        vx, vy = vx / (norm+0.0001), vy / (norm+0.0001)
        if norm < 75:
            x, y = x2, y2
        else:
            x, y = x1 + vx * 75, y1 + vy * 75
        if ray:
            pygame.draw.line(screen, 'red', (x1, y1), (x,y), 1)
        return norm

    def getraytresor(self,screen):
        liste = []
        self.coord = (0,0)
        pluspetit = 8000
        for tresor in self.tresors:
            liste.append(self.ray(screen,tresor,False))
            if self.ray(screen,tresor,False) < pluspetit:
                pluspetit=self.ray(screen,tresor,False)
                self.coord=tresor
        min_dist = round(min(liste))+5
        self.min_dist = min_dist-5
        if self.bip == self.frame or min_dist < self.bip - self.lastbip - min_dist + 10 :
            pygame.mixer.Sound.play(self.son01)
            self.bip = self.frame
            self.bip, self.lastbip = self.bip + min_dist, self.bip
            x = min(255, max(0, pluspetit))
            self.radar.green = x
            self.radar.create()

        self.ray(screen, self.coord)
    def trouver_tresor(self):
        if self.min_dist < 5:
            self.tresors.remove(self.coord)


class Radar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([50, 50], pygame.SRCALPHA)
        self.image.set_colorkey((0, 0, 0))

        self.rect = self.image.get_rect()
        self.coord = [100, 100]
        self.green = 0
        self.liste_radar = [0]

    def update(self):
        self.rect.topleft = self.coord
        self.image.fill((0, 0, 0))
        N = len(self.liste_radar)
        for i in range(N-1, -1, -1):
            circle = self.liste_radar[i]
            if circle < 25:
                pygame.draw.circle(self.image, (255-self.green, self.green, 0, 250-circle*9), (25, 25), circle, 3)
                self.liste_radar[i] += 0.5
            else:
                del self.liste_radar[i]

    def set_middle(self, coord):
        x, y = coord
        self.coord = (x-25, y-25)

    def create(self):
        self.liste_radar.append(0)

