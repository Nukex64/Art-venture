#Projet : Art'Venture
#Auteurs : Anthony Ibanez-Esteban, Raphaël Prost, Aëlys-Coleen Surma Valtaer, Louis Gagne, Mathéo Faure

import pygame

import math
import settings
from savefonction import sauvegarde


class Animation:
    def __init__(self):
        """
        Initialise le jeu, configure la fenêtre de jeu, et définit les cartes et mini-jeux disponibles.
        """
        self.circle = 0
        self.afficher = True
        self.screen = pygame.display.set_mode(settings.RES,pygame.SCALED)
        self.font = pygame.font.Font(settings.Font, 65)
        self.game_background = None
        self.image_originelle = self._cut_img(4, 80)
        self.image = self.image_originelle.copy()
        self.x = None
        self.y = None
        self.speed = 1
        self.alpha = math.pi
        self.frame = 0
        self.size = (32,32)
        self.sizefactor = -0.01


        self.menu_background = pygame.image.load("img/ui/menu_back.png").convert_alpha()


        self.end = False #ordonne de fermer le jeu

        self.button_survoller = False
        self.in_setting = False

    def _cut_img(self, x, y):
        """
        :x/y: int (coord)
        Decoupe l'image du joueur de taille 16x16 a l'emplacement (x,y)
        """
        image = pygame.Surface([16, 16], pygame.SRCALPHA)
        image.blit(pygame.image.load('img/player_sheet.png').convert_alpha(), (0, 0), (x, y, 16, 16))
        return image

    def fist_draw(self):
        self.frame = 0
        pass

    def draw(self):
        self.screen.blit(self.game_background,(0,0))
        self.screen.blit(self.image, (self.x, self.y))
        pygame.draw.circle(self.screen, (255, 255, 255), (self.x, self.y),self.circle)


        pygame.display.flip()

    def _gerer_event(self):
        """
        Gère les événements du jeu (clavier, fermeture de la fenêtre, etc.).
        (60/s)
        """
        self.draw()
        self.alpha += self.degre
        self.degre += 0.0002
        self.size = (max(self.size[0]+self.sizefactor,0.01),max(self.size[1]+self.sizefactor,0.01))
        self.image = pygame.transform.scale(self.image_originelle, self.size)
        self.move()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # quitter
                pygame.quit()

        if self.frame >= 1720:
            if self.circle >= 800:
                self.afficher = False
            self.circle += 1




    def move(self, sens = "z"):
        vx, vy = 0,0

        if sens == "z":
            vx += self.speed * math.cos(self.alpha)
            vy += self.speed * math.sin(self.alpha)
        self.x += vx
        self.y += vy

    def regarder(self, angle):
        radian = math.radians(angle)
        self.alpha += radian
        self.alpha %= math.tau #modulo 2 pi


    def reprendre(self):
        self.afficher = False # ferme le menu

    def open(self,xy):
        self.circle = 0
        self.speed = 1.5
        self.alpha = math.pi
        self.degre = 0.03
        self.frame = 0
        self.x, self.y = xy[0], xy[1]
        self.size = (32, 32)
        self.image = self.image_originelle.copy()
        self.afficher = True
        self.fist_draw()
        self.game_background = pygame.display.get_surface().subsurface(pygame.Rect(0, 0, 800,600)).copy() #copy du menu vide
        self.draw()

        while self.afficher:
            self.frame += 1
            self._gerer_event()

    def game_over(self, coord):
        self.game_background = pygame.display.get_surface().subsurface(pygame.Rect(0, 0, 800,600)).copy() #copy du menu vide
        self.circle = 0
        while self.circle < 75:
            self.draw_game_over(coord)
        self.circle = 0

    def draw_game_over(self, coord):
        self.circle += 0.25
        self.screen.blit(self.game_background, (0, 0))
        pygame.draw.circle(self.screen, (255, 0, 0), coord,self.circle)
        pygame.display.flip()

