#Projet : Art'Venture
#Auteurs : Anthony Ibanez-Esteban, Raphaël Prost, Aëlys-Coleen Surma Valtaer, Louis Gagne, Mathéo Faure
import os

import pygame
from  random import randint, shuffle
import json
from settings import*

class Quiz:
    """
    Classe représentant un quiz interactif dans le jeu.
    Les joueurs doivent répondre à des questions basées sur des données dans un fichier JSON.
    """

    @staticmethod
    def get_url(url):
        url_list = url.split("/")
        return os.path.join(*url_list)

    def __init__(self):
        """
        Initialise un nouvel objet de quiz, charge les données depuis le fichier JSON,
        génère une question et prépare les réponses possibles.
        """
        self.victory = 0
        self.afficher = False
        with open(self.get_url(f"tableau.json"), "r+") as f:
            self.data = json.load(f)

        self.screen = pygame.display.set_mode(RES,pygame.SCALED)
        self.game_background = None

        self.timer = 0
        self.objetif = None
        self.nb = randint(1, 10)
        self.q_nb = randint(1, 3)
        self.q = {2: "Qui est l'auteur?", 3:"Quelle est la date ?", 1:"Quelle est le titre ?"}

        self.bonne_reponse = [self.data[str(self.nb)][self.q_nb]]

        self.mauvaise_r = []
        while len(self.mauvaise_r) < 3:
            x = randint(1, 10)
            txt = self.data[str(x)][self.q_nb]
            if txt not in self.mauvaise_r : self.mauvaise_r.append(txt)

        self.reponses = self.bonne_reponse + self.mauvaise_r

        self.img = pygame.image.load(self.get_url(f"img/tableau/{self.nb}.webp"))
        self.font = pygame.font.Font(None, 14)
        self.font_2 = pygame.font.Font(None, 28)
        self.copyr = self.font.render(self.data[str(self.nb)][0], False, (0, 0, 0))
        self.question = self.font_2.render(self.q[self.q_nb], False, (0, 0, 0))

        shuffle(self.reponses)
        self.good =self.reponses.index(self.bonne_reponse[0])
        self.r_1 = self.font_2.render(self.reponses[0], False, (0, 0, 0))
        self.r_2 = self.font_2.render(self.reponses[1], False, (0, 0, 0))
        self.r_3 = self.font_2.render(self.reponses[2], False, (0, 0, 0))
        self.r_4 = self.font_2.render(self.reponses[3], False, (0, 0, 0))

        self.rect_1 = pygame.Rect(100, 415, self.r_1.get_width(), 19)
        self.rect_2 = pygame.Rect(400, 415, self.r_2.get_width(), 19)
        self.rect_3 = pygame.Rect(100, 500, self.r_3.get_width(), 19)
        self.rect_4 = pygame.Rect(400, 500, self.r_4.get_width(), 19)
        self.rects = {0:self.rect_1, 1:self.rect_2, 2:self.rect_3, 3:self.rect_4}
        self.rect_afficher = [(0, 0, 0, 0), (0, 0, 0, 0)]

    def draw(self):
        """
        Affiche l'interface du quiz à l'écran.
        - Affiche l'image, la question, et les réponses sous forme de texte.
        - Dessine les cases de réponse et met en évidence les réponses sélectionnées.
        """
        self.screen.blit(self.game_background, (0, 0))
        pygame.draw.rect(self.screen, (50, 50, 50), (100, 415, 300+max(self.r_4.get_width(), self.r_2.get_width()),85+19))

        x = (800-self.img.get_width())//2
        y = self.img.get_height()
        self.screen.blit(self.copyr, (x, 10 + self.img.get_height()))
        self.screen.blit(self.question, ((800-self.question.get_width())//2, 10+self.img.get_height() + self.copyr.get_height()))
        self.screen.blit(self.r_1, (100, 415))
        self.screen.blit(self.r_2, (400, 415))
        self.screen.blit(self.r_3, (100, 500))
        self.screen.blit(self.r_4, (400, 500))
        self.screen.blit(self.img, (x, 10))

        if self.rect_afficher != [(0, 0, 0, 0), (0, 0, 0, 0)]:
            pygame.draw.rect(self.screen, (0, 255, 0), self.rect_afficher[0], 2)
            pygame.draw.rect(self.screen, (255, 0, 0), self.rect_afficher[1], 2)
            self.timer -= 1
            if self.timer <= 0: self.afficher = False

        pygame.display.flip()

    def _gerer_event(self):
        """
        Gère les événements du jeu, comme la fermeture de la fenêtre et les entrées utilisateur.
        Cette méthode est appelée à chaque frame (60 fois par seconde).
        """
        pass
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # quitter
                self.afficher = False

    def change(self, nb):
        """
        Change la question du quiz. Cette méthode génère une nouvelle question et de nouvelles réponses
        à partir du fichier JSON. Si `nb` est passé en argument, une question spécifique est sélectionnée.

        Args:
        - nb (int): Le numéro de la question à afficher. Si None, une question aléatoire est choisie.
        """
        self.victory = 0
        if nb : self.nb = nb
        else: self.nb = randint(1, 10)
        self.q_nb = randint(1, 3)
        self.q = {2: "Qui est l'auteur?", 3:"Quelle est la date ?", 1:"Quelle est le titre ?"}

        self.bonne_reponse = [self.data[str(self.nb)][self.q_nb]]
        self.mauvaise_r = []
        while len(self.mauvaise_r) < 3:
            x = randint(1, 10)
            txt = self.data[str(x)][self.q_nb]
            if txt not in self.mauvaise_r : self.mauvaise_r.append(txt)
        self.reponses = self.bonne_reponse + self.mauvaise_r

        self.img = pygame.image.load(self.get_url("img/tableau/{self.nb}.webp"))
        self.font = pygame.font.Font(None, 14)
        self.font_2 = pygame.font.Font(None, 28)
        self.copyr = self.font.render(self.data[str(self.nb)][0], False, (0, 0, 0))
        self.question = self.font_2.render(self.q[self.q_nb], False, (0, 0, 0))

        shuffle(self.reponses)
        self.good =self.reponses.index(self.bonne_reponse[0])

        self.r_1 = self.font_2.render(self.reponses[0], False, (0, 0, 0))
        self.r_2 = self.font_2.render(self.reponses[1], False, (0, 0, 0))
        self.r_3 = self.font_2.render(self.reponses[2], False, (0, 0, 0))
        self.r_4 = self.font_2.render(self.reponses[3], False, (0, 0, 0))

        self.rect_1 = pygame.Rect(100, 415, self.r_1.get_width(), 19)
        self.rect_2 = pygame.Rect(400, 415, self.r_2.get_width(), 19)
        self.rect_3 = pygame.Rect(100, 500, self.r_3.get_width(), 19)
        self.rect_4 = pygame.Rect(400, 500, self.r_4.get_width(), 19)
        self.rects = {0: self.rect_1, 1: self.rect_2, 2: self.rect_3, 3: self.rect_4}
        self.rect_afficher = [(0, 0, 0, 0), (0, 0, 0, 0)]

    def __str__(self):
        return "Quiz"

    def choice(self, nb):
        """
        Gère le choix de réponse du joueur. Compare la réponse sélectionnée avec la bonne réponse.
        - Si la réponse est correcte, le joueur gagne.
        - Si la réponse est incorrecte, l'option correcte est mise en évidence.

        Args:
        - nb (int): L'indice de la réponse choisie par le joueur.
        """
        if self.timer <= 0:
            self.timer = 450
            if nb == self.good:
                self.rect_afficher = [self.rects[self.good], (0, 0, 0, 0)]
                self.victory = 1
            else:
                self.rect_afficher = [self.rects[self.good], self.rects[nb]]
                self.victory = 0

    def update(self):
        if pygame.mouse.get_pressed()[0] :
            x, y = pygame.mouse.get_pos()
            if self.rect_1.collidepoint(x, y): self.choice(0)
            if self.rect_2.collidepoint(x, y): self.choice(1)
            if self.rect_3.collidepoint(x, y): self.choice(2)
            if self.rect_4.collidepoint(x, y): self.choice(3)

    def open(self, nb=None):
        """
        Ouvre et affiche le quiz à l'écran. Cette méthode génère une nouvelle question, attend la sélection du joueur,
        et affiche les résultats en fonction du choix du joueur.

        Args:
        - nb (int, optional): Le numéro de la question à afficher. Si None, une question aléatoire est choisie.

        Returns:
        - int: Retourne 1 si la réponse est correcte, 0 sinon.
        """
        self.change(nb)
        self.afficher = True
        self.game_background = pygame.display.get_surface().subsurface(pygame.Rect(0, 0, 800, 600)).copy() #copy du menu vid
        while self.afficher:
            self._gerer_event()
            self.update()
            self.draw()
        return self.victory