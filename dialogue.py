#Projet : Art'Venture
#Auteurs : Anthony Ibanez-Esteban, Raphaël Prost, Aëlys-Coleen Surma Valtaer, Louis Gagne, Mathéo Faure

import pygame

class Dialogue:
    def __init__(self, texte):
        self.screen = pygame.display.get_surface()
        self.afficher = False
        self.dialogue_box = pygame.image.load("img/txt.png")
        self.dialogue_box = pygame.transform.scale(self.dialogue_box, (650, 265))
        self.font = pygame.font.Font("img/police.otf", 24)


        self.liste_texte = texte.split("\n")
        self.texte_render = self.font.render(self.liste_texte[0], True, (0, 0, 0))
        self.index = 0
        self.game_background = None

    def _gerer_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # quitter
                self.afficher = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.afficher = False
                if event.key == pygame.K_RETURN:
                    self.next()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.next()


    def draw(self):
        self.screen.blit(self.game_background, (10, 485))
        self.screen.blit(self.dialogue_box, ((800-650)/2, 600-265))
        self.screen.blit(self.texte_render, (170, 430))
        pygame.display.flip()

    def next(self):
        if self.index < len(self.liste_texte) - 1:
            self.index += 1
            self.texte_render = self.font.render(self.liste_texte[self.index], True, (0, 0, 0))
            self.draw()
        else:
            self.afficher = False

    def open(self):
        self.afficher = True
        self.game_background = pygame.display.get_surface().subsurface(pygame.Rect(10, 485, 780, 109)).copy()
        self.draw()

        while self.afficher:
            self._gerer_event()
