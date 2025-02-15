import pygame

import settings
from settings import *

class Menu:
    def __init__(self):
        self.afficher = True
        self.screen = pygame.display.set_mode(RES,pygame.SCALED)
        self.font = pygame.font.Font(Font, 65)

        self.menu_background = pygame.image.load("img/ui/menu_back.png")

        self.menu_image = pygame.image.load("img/ui/menu.png")

        self.rect_reprendre = pygame.Rect(225, 145, 340, 87)
        self.rect_parametre = pygame.Rect(225, 145+130, 340, 87)
        self.rect_quitter = pygame.Rect(225, 145+260, 340, 87)

        self.click_parametre = pygame.image.load("img/ui/BsettingsC.png")
        self.click_parametre.set_colorkey((255, 255, 255))
        self.click_exit = pygame.image.load("img/ui/BexitC.png")
        self.click_exit.set_colorkey((255, 255, 255))
        self.click_reprendre = pygame.image.load("img/ui/BbackC.png")
        self.click_reprendre.set_colorkey((255, 255, 255))

        self.end = False #ordonne de fermer le jeu

        self.button_survoller = False

        self.screen.blit(self.menu_background, (0, 0))
        pygame.display.flip()

    def draw(self):
        self.screen.blit(self.menu_image, (0, 0))
        #pygame.draw.rect(self.screen, (0, 0, 0), self.reprendre)
        #pygame.draw.rect(self.screen, (0, 0, 0), self.settings)
        #pygame.draw.rect(self.screen, (0, 0, 0), self.rect_quitter)
        pygame.display.update((225, 145, 340, 87))

    def _gerer_event(self):
        """
        Gère les événements du jeu (clavier, fermeture de la fenêtre, etc.).
        (60/s)
        """
        click = False
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
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True

        x, y, = pygame.mouse.get_pos()


        if self.rect_reprendre.collidepoint(x, y):
            if not self.button_survoller:
                self.screen.blit(self.click_reprendre, (216, 141))
                pygame.display.update(self.rect_reprendre)
                self.button_survoller = True
            if click : self.reprendre()

        elif self.rect_parametre.collidepoint(x, y):
            if not self.button_survoller:
                self.screen.blit(self.click_parametre, (216, 142 + 130))
                pygame.display.update(self.rect_parametre)
                self.button_survoller = True
            if click: self.parametre()

        elif self.rect_quitter.collidepoint(x, y):
            if not self.button_survoller:
                self.screen.blit(self.click_exit, (214, 140 + 260))
                pygame.display.update(self.rect_quitter)
                self.button_survoller = True
            if click: self.quitter()

        else:
            if self.button_survoller:
                self.button_survoller = False
                self.draw()

    def reprendre(self):
        print("    Reprendre")
        self.afficher = False # ferme le menu

    def parametre(self):
        self.musique()
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
