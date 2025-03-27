# Projet : Art'Venture
# Auteurs : Anthony Ibanez-Esteban, Raphaël Prost, Aëlys-Coleen Surma Valtaer, Louis Gagne, Mathéo Faure
import os

import pygame
import math
import settings


class Victoire:
    def __init__(self):
        """
        Initialise les paramètres de l'animation.

        Configure la fenêtre de jeu, charge les images nécessaires et initialise les variables utilisées
        pour l'animation, y compris la position, la vitesse et les états d'affichage.
        """
        self.afficher = True
        self.coord = (0,0)
        self.screen = pygame.display.set_mode(settings.RES, pygame.SCALED)  # Création de la fenêtre du jeu
        self.font = pygame.font.Font(settings.Font, 65)
        self.game_background = None
        self.effect = pygame.image.load(self.get_url("img/lumeffect.png"))
        self.image = None  # initialise l'image
        self.x = None
        self.y = None
        self.alpha = math.pi
        self.frame = 0
        self.end = False  # Ordre de fermeture du jeu
        self.button_survoller = False
        self.in_setting = False

    def fist_draw(self):
        """
        Réinitialise l'animation en mettant la frame à zéro.
        Réinitialise la frame à zéro pour redémarrer l'animation.
        """
        self.frame = 0

    def draw(self):
        """
        Dessine les éléments de l'animation sur l'écran.
        Affiche l'arrière-plan du jeu, l'image animée du joueur et un cercle évolutif
        pour l'effet visuel.
        """
        self.screen.blit(self.game_background, (0, 0))  # Dessine l'arrière-plan
        self.screen.blit(self.effect, (self.coord[0]-300,self.coord[1]-300))  # Dessine l'effet
        self.screen.blit(self.image, self.coord)  # Dessine l'image de l'objet
        self.effect = pygame.transform.rotate(self.effect,1)
        pygame.display.flip()  # Rafraîchit l'écran

    def _gerer_event(self):
        """
        Gère les événements du jeu et met à jour l'animation.
        - Anime le joueur en modifiant son échelle et sa rotation.
        - Déplace le joueur en fonction des paramètres d'animation.
        - Gère les événements utilisateur comme la fermeture de la fenêtre.
        """
        self.draw()  # Dessine l'animation
        self.effect = pygame.transform.rotate(self.effect, 0)

        for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Quitte annimation
                    pygame.quit()




    def reprendre(self):
        """
        Interrompt l'affichage de l'animation et ferme le menu.

        Met fin à l'animation en modifiant l'état d'affichage.
        """
        self.afficher = False  # Ferme le menu

    def open(self,xy, image):
        """
        Ouvre l'animation, réinitialise les variables et commence l'animation à la position spécifiée.

        :param xy: Tuple contenant les coordonnées de départ (x, y) pour l'animation.
        :return: None
        """
        self.coord=xy
        self.speed = 1.5
        self.image = pygame.image.load(self.get_url(image))
        self.image = pygame.transform.scale(self.image,(40,40))
        self.alpha = math.pi
        self.frame = 0
        self.size = (32, 32)
        self.afficher = True
        self.fist_draw()  # Initialisation de la première frame
        self.game_background = pygame.display.get_surface().subsurface(pygame.Rect(0, 0, 800, 600)).copy()  # Copie du menu vide
        self.draw()  # Dessine l'animation

        while self.afficher:
            self.frame += 1  # Incrémente la frame
            self._gerer_event()  # Gère les événements à chaque frame

    @staticmethod
    def get_url(url):
        url_list = url.split("/")
        return os.path.join(*url_list)