import math

import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, src, x, y):
        super().__init__()
        self.image = pygame.image.load(src)
        self.image.set_colorkey([0, 0, 0])  # retire le fond noire au spawn du joueur

        self.rect = self.image.get_rect() # definit l'hitbox / le rectangle du joueur
        self.coord = [x, y]
        self.speed = 3
        self.direction = 0

    def update(self):
        """
        Pose le haut gauche du joueur et ses pied où il faut
        Ne pas renommer la methode _update pour que self.groupe._update() fonctionne
        """
        self.rect.topleft = self.coord

    def regarder(self, angle):
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect()

    # x est un multiplieur si on ne met rien c'est *1
    def haut(self, x=1):
        self.coord[1] -= self.speed * x
    def bas(self, x=1):
        self.coord[1] += self.speed * x
    def gauche(self, x=1):
        self.coord[0] -= self.speed * x
    def droite(self, x=1):
        self.coord[0] += self.speed * x

    def avancer(self):
        if self.direction == 270: self.bas()
        if self.direction == 90: self.haut()
        if self.direction == 180: self.gauche()
        if self.direction == 0: self.droite()

    def invers_direction(self):
        self.direction += 180
        self.direction %= 360 #modulo 360

    def viser(self, obj):
        x1, y1 = self.coord
        x2, y2 = obj
        vx, vy = x2-x1, y2-y1
        norm = math.sqrt(vx**2 + vy**2)
        if norm < 200:
            vx, vy = vx/norm, vy/norm
            self.coord[0]+=vx
            self.coord[1]+=vy