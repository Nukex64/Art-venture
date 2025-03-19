# Projet : Art'Venture
# Auteurs : Anthony Ibanez-Esteban, Raphaël Prost, Aëlys-Coleen Surma Valtaer, Louis Gagne, Mathéo Faure

import pygame

class Tuto:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.afficher = False
        self.dialogue_box = pygame.image.load("img/txt.png")
        self.dialogue_box = pygame.transform.scale(self.dialogue_box, (760,560))
        self.font = pygame.font.Font("img/police.otf", 24)
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
        self.screen.blit(self.game_background, (0,0))
        self.screen.blit(self.dialogue_box, (20, 20))
        self.screen.blit(self.img, (30,(self.screen.get_height()-self.img.get_height())/2))
        self.screen.blit(self.texte_render, (240,50))
        pygame.display.flip()

    def next(self):
        if self.index < len(self.texte) - 1:
            self.index += 1
            self.texte_render = self.font.render(self.texte, True, (0, 0, 0))
            self.draw()
        else:
            self.afficher = False

    def open(self,texte, img = None):
        self.afficher = True
        self.texte = texte
        self.texte_render = self.font.render(self.texte, True, (0, 0, 0))
        if img:
            self.img = pygame.image.load(img)
            size = self.img.get_rect()
            vect = 200 / size[2]
            self.img = pygame.transform.scale(self.img,(200,size[3]*vect))


        self.game_background = pygame.display.get_surface().subsurface(pygame.Rect(0, 0, 800, 600)).copy()
        self.draw()

        while self.afficher:
            self._gerer_event()