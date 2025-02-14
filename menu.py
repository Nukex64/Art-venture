import pygame
from savefonction import sauvegarde
import settings
from settings import *

class Menu():
    def __init__(self):
        """
        Initialise le jeu, configure la fenêtre de jeu, et définit les cartes et mini-jeux disponibles.
        """
        self.saveload = sauvegarde()
        self.afficher = True
        self.screen = pygame.display.set_mode(RES,pygame.NOFRAME|pygame.SCALED)
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
                if event.key == pygame.K_SPACE:
                    print("ok")
                    self.fullscreen()
                if event.key == pygame.K_m:
                    print("musique")
                    self.musique()
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("click")



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
        if self.saveload.changer_json('Musiques',None) == 1:
            pygame.mixer_music.pause()
            self.saveload.changer_json('Musiques',0)
        elif self.saveload.changer_json('Musiques',None) == 0:
            pygame.mixer.music.play(loops=-1)
            self.saveload.changer_json('Musiques',1)
