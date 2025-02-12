import math
import pygame
from settings import WIDTH, HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self, src, x, y):
        super().__init__()
        self.image = pygame.image.load(src)
        self.image.set_colorkey([0, 0, 0])  # retire le fond noire au spawn du joueur

        self.rect = self.image.get_rect() # definit l'hitbox / le rectangle du joueur
        self.coord = [x, y]
        self.speed = 3
        self.alpha = 0
        self.speed = 20

    def update(self):
        """
        Pose le haut gauche du joueur et ses pied où il faut
        Ne pas renommer la methode _update pour que self.groupe._update() fonctionne
        """
        self.rect.topleft = self.coord

    def regarder(self, angle):
        radian = math.radians(angle)
        self.alpha += radian
        self.alpha %= math.tau #modulo 2 pi

    def invers_direction(self):
        self.alpha += math.pi
        self.alpha %= math.tau #modulo 360

    def viser(self, obj):
        x1, y1 = self.coord
        x2, y2 = obj
        vx, vy = x2-x1, y2-y1
        norm = math.sqrt(vx**2 + vy**2)
        if norm < 200:
            vx, vy = vx/norm, vy/norm
            self.coord[0]+=vx
            self.coord[1]+=vy

    def avancer(self): self.move("z")
    def reculer(self): self.move("s")
    def gauche(self): self.move("q")
    def droite(self): self.move("d")

    def move(self, sens):

        vx, vy = 0,0

        if sens == "z":
            vx += self.speed * math.cos(self.alpha)
            vy += self.speed * math.sin(self.alpha)

        if sens == "s":
            vx -= self.speed * math.cos(self.alpha)
            vy -= self.speed * math.sin(self.alpha)

        if sens == "d":
            vx -= self.speed * math.sin(self.alpha)
            vy += self.speed * math.cos(self.alpha)

        if sens == "q":
            vx += self.speed * math.sin(self.alpha)
            vy -= self.speed * math.cos(self.alpha)

        #norm = math.sqrt(vx ** 2 + vy ** 2)
        #if norm != 0:
        #    vx *= speed / norm
        #    vy *= speed / norm
        self.coord[0] += vx
        self.coord[1] += vy

    def is_off_screen(self):
        return self.rect.center[0] < 0-100 or self.rect.center[0] > WIDTH+100 or self.rect.center[1] < 0-100 or self.rect.center[1] > HEIGHT+100
