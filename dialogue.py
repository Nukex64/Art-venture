#Projet : Art'Venture
#Auteurs : Anthony Ibanez-Esteban, Raphaël Prost, Aëlys-Coleen Surma Valtaer, Louis Gagne, Mathéo Faure
import os

import pygame

class Dialogue:
    def __init__(self, texte: str):
        """
        Initialise le système de dialogue avec un texte donné.

        :param texte: Le texte du dialogue à afficher, avec des retours à la ligne pour séparer les phrases.
        """
        self.screen = pygame.display.get_surface()
        self.afficher = False
        self.dialogue_box = pygame.image.load(self.get_url("img/txt.png"))
        self.dialogue_box = pygame.transform.scale(self.dialogue_box, (650, 265))
        self.font = pygame.font.Font(self.get_url("img/police.otf"), 24)


        self.liste_texte = texte.split("\n")
        self.texte_render = self.font.render(self.liste_texte[0], True, (0, 0, 0))
        self.index = 0
        self.game_background = None

    @staticmethod
    def get_url(url):
        print(url)
        url_list = url.split("/")
        return os.path.join(*url_list)

    def _gerer_event(self):
        """
        Gère les événements liés à l'interaction avec le dialogue.

        Permet de fermer le dialogue avec la touche 'Echap', de passer à la phrase suivante avec la touche 'Entrée',
        ou un clic de souris.
        """
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
        """
        Dessine le fond et le texte du dialogue sur l'écran.

        Affiche la boîte de dialogue ainsi que le texte actuel à l'écran.
        """
        self.screen.blit(self.game_background, (10, 485))
        self.screen.blit(self.dialogue_box, ((800-650)/2, 600-265))
        self.screen.blit(self.texte_render, (170, 430))
        pygame.display.flip()

    def next(self):
        """
        Passe à la phrase suivante dans le dialogue.

        Si le dialogue est terminé, ferme le dialogue. Sinon, affiche la phrase suivante.
        """
        if self.index < len(self.liste_texte) - 1:
            self.index += 1
            self.texte_render = self.font.render(self.liste_texte[self.index], True, (0, 0, 0))
            self.draw()
        else:
            self.afficher = False

    def open(self):
        """
        Ouvre le dialogue et commence à afficher le texte.

        Enregistre l'arrière-plan actuel, affiche la boîte de dialogue et gère les événements
        jusqu'à ce que le dialogue soit terminé.
        """
        self.afficher = True
        self.game_background = pygame.display.get_surface().subsurface(pygame.Rect(10, 485, 780, 109)).copy()
        self.draw()

        while self.afficher:
            self._gerer_event()
