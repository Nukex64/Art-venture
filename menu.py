import pygame

import settings
from settings import *

class Menu:
    def __init__(self):
        """
        Initialise le jeu, configure la fenêtre de jeu, et définit les cartes et mini-jeux disponibles.
        """
        self.afficher = True
        self.screen = pygame.display.set_mode(RES,pygame.SCALED)
        self.font = pygame.font.Font(Font, 65)

        self.menu_image = pygame.image.load("img/ui/menu.png")
        self.menu_image.set_colorkey((255, 255, 255))

        self.rect_reprendre = pygame.Rect(225, 145, 340, 87)
        self.rect_parametre = pygame.Rect(225, 145+130, 340, 87)
        self.rect_quitter = pygame.Rect(225, 145+260, 340, 87)

        self.click_parametre = pygame.image.load("img/ui/BsettingsC.png")
        self.click_parametre.set_colorkey((255, 255, 255))
        self.click_exit = pygame.image.load("img/ui/BexitC.png")
        self.click_exit.set_colorkey((255, 255, 255))
        self.click_back = pygame.image.load("img/ui/BbackC.png")
        self.click_back.set_colorkey((255, 255, 255))

        self.end = False #ordonne de fermer le jeu

    def draw(self):
        self.screen.blit(self.menu_image, (0, 0))
        #pygame.draw.rect(self.screen, (0, 0, 0), self.reprendre)
        #pygame.draw.rect(self.screen, (0, 0, 0), self.settings)
        #pygame.draw.rect(self.screen, (0, 0, 0), self.rect_quitter)
        pygame.display.flip()

    def _gerer_event(self):
        """
        Gère les événements du jeu (clavier, fermeture de la fenêtre, etc.).
        (60/s)
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # quitter
                self.afficher = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.afficher = False

                if event.key == pygame.K_SPACE:
                    print("ok")
                    self.fullscreen()
                if event.key == pygame.K_m:
                    print("musique")
                    self.musique()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y, = pygame.mouse.get_pos()
                if self.rect_reprendre.collidepoint(x, y): self.reprendre()
                elif self.rect_parametre.collidepoint(x, y): self.parametre()
                elif self.rect_quitter.collidepoint(x, y): self.quitter()

        x, y, = pygame.mouse.get_pos()
        if self.rect_reprendre.collidepoint(x, y):
            self.screen.blit(self.click_back, (214, 140))
            pygame.display.flip()
        elif self.rect_parametre.collidepoint(x, y):
            self.screen.blit(self.click_parametre, (216, 142 + 130))
            pygame.display.flip()
        elif self.rect_quitter.collidepoint(x, y):
            self.screen.blit(self.click_exit, (214, 140 + 260))
            pygame.display.flip()
        else:
            self.draw()

    def reprendre(self):
        print("    Reprendre")
        self.afficher = False # ferme le menu

    def parametre(self):
        print("    Parametre")

    def quitter(self):
        print("    Quitter")
        self.afficher = False # ferme le menu
        self.end = True # ferme le jeu

    def open(self):
        print("-- MENU OPEN")

        self.afficher = True
        self.draw()

        while self.afficher:
            self._gerer_event()

        print("-- MENU END")

    def fullscreen(self):
        pygame.display.toggle_fullscreen()
        pygame.display.flip()

    def musique(self):
        if settings.Musiques == 1:
            pygame.mixer_music.pause()
            settings.Musiques = 0
        elif settings.Musiques == 0:
            pygame.mixer_music.play()
            settings.Musiques = 1
