#Projet : Art'Venture
#Auteurs : Anthony Ibanez-Esteban, Raphaël Prost, Aëlys-Coleen Surma Valtaer, Louis Gagne, Mathéo Faure

import math

import pygame

from settings import WIDTH, HEIGHT


class Enemy(pygame.sprite.Sprite):
    def __init__(self, src: str, x: int, y: int):
        """
        Initialise un ennemi avec une image et une position initiale.

        :param src: Chemin de l'image ou l'image elle-même à utiliser pour l'ennemi.
        :param x: Position initiale en x de l'ennemi.
        :param y: Position initiale en y de l'ennemi.
        """
        super().__init__()
        if type(src) == str:
            self.image = pygame.image.load(src)
        else: self.image = src
        self.image.set_colorkey([0, 0, 0])  # retire le fond noire au spawn du joueur

        self.rect = self.image.get_rect() # definit l'hitbox rectangulaire / le rectangle de l'image du joueur
        self.mask = pygame.mask.from_surface(self.image)#  definit l'hitbox par pixel (le mieux)

        self.x = x
        self.y = y
        self.speed = 3
        self.alpha = 0
        self.speed = 20

        self.cible = (x, y)
        self.cible_i = 0

    def update(self):
        """
        Met à jour la position de l'ennemi selon ses coordonnées.
        Positionne le coin supérieur gauche de l'ennemi à sa position actuelle.
        """
        self.rect.topleft = self.coord

    def regarder(self, angle):
        """
        Modifie la direction de l'ennemi en fonction d'un angle donné.

        :param angle: Angle en degrés de la nouvelle direction.
        """
        radian = math.radians(angle)
        self.alpha += radian
        self.alpha %= math.tau #modulo 2 pi

    def invers_direction(self):
        self.alpha += math.pi
        self.alpha %= math.tau #modulo 360

    def viser(self, obj: tuple[int, int]):
        """
        Fait en sorte que l'ennemi se dirige vers une position donnée.

        :param obj: Coordonnées (x, y) de la cible que l'ennemi doit viser.
        """
        if obj != self.coord: # sinon infinie
            x1, y1 = self.coord
            x2, y2 = obj
            vx, vy = x2-x1, y2-y1
            norm = math.sqrt(vx**2 + vy**2)
            if norm > 1: # proche de plus de 1 pixel
                vx, vy = vx/norm, vy/norm
                self.x +=vx
                self.y +=vy
            else:
                self.x, self.y = obj #si trop proche corection (bug infinie sinon)

    def avancer(self): self.move("z")
    def reculer(self): self.move("s")
    def gauche(self): self.move("q")
    def droite(self): self.move("d")

    def move(self, sens: str):
        """
        Déplace l'ennemi dans une direction spécifiée.

        :param sens: Direction du mouvement ("z", "s", "q", "d").
        """

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
        self.x += vx
        self.y += vy

    def is_off_screen(self) -> bool:
        """
        :return: True si l'ennemi est hors de l'écran, sinon False.
        """
        return self.rect.center[0] < 0-100 or self.rect.center[0] > WIDTH+100 or self.rect.center[1] < 0-100 or self.rect.center[1] > HEIGHT+100

    @property
    def coord(self) -> tuple[int, int]:
        """
        Obtient les coordonnées actuelles de l'ennemi.
        :return: Tuple (x, y) représentant la position de l'ennemi.
        """
        return self.x, self.y

    def alternate(self, liste: list[tuple[int, int]]):
        """
        Permet à l'ennemi de suivre un parcours alternant entre les positions d'une liste.

        :param liste: Liste des positions que l'ennemi doit suivre.
        """
        if self.coord in liste:
            x = self.cible_i
            if self.alpha == 1:
                if x < len(liste)-1:
                    self.cible_i += 1
                    self.cible = liste[self.cible_i]
                else:
                    self.alpha = -1
                    self.cible_i -= 1
                    self.cible = liste[self.cible_i]
            else:
                if x > 0:
                    self.cible_i -= 1
                    self.cible = liste[self.cible_i]
                else:
                    self.alpha = 1
                    self.cible_i += 1
                    self.cible = liste[self.cible_i]
        self.viser(self.cible)