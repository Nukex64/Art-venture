import pygame
from settings import *

class Menu:
    def __init__(self):
        """
        Initialise le jeu, configure la fenêtre de jeu, et définit les cartes et mini-jeux disponibles.
        """
        self.afficher = True
        self.screen = pygame.display.set_mode(RES)
        self.font = pygame.font.Font(Font, 65)
        self.text_2 = self.font.render("PAUSE", True, (0, 0, 0))

    def draw(self):
        self.screen.blit(self.text_2, (340, 100))
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("click")


    def open(self):
        print("-- MENU OPEN")

        self.afficher = True
        self.draw()

        while self.afficher:
            self._gerer_event()

        print("-- MENU END")