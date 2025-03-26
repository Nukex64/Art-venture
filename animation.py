# Projet : Art'Venture
# Auteurs : Anthony Ibanez-Esteban, Raphaël Prost, Aëlys-Coleen Surma Valtaer, Louis Gagne, Mathéo Faure
import os

import pygame
import math
import settings


class Animation:
    def __init__(self):
        """
        Initialise les paramètres de l'animation.

        Configure la fenêtre de jeu, charge les images nécessaires et initialise les variables utilisées
        pour l'animation, y compris la position, la vitesse et les états d'affichage.
        """
        self.circle = 0
        self.afficher = True
        self.screen = pygame.display.set_mode(settings.RES, pygame.SCALED)  # Création de la fenêtre du jeu
        self.font = pygame.font.Font(settings.Font, 65)
        self.game_background = None
        self.image_originelle = self._cut_img(4, 80)  # Découpe de l'image du joueur
        self.image = self.image_originelle.copy()  # Copie de l'image
        self.x = None
        self.y = None
        self.speed = 1
        self.alpha = math.pi
        self.frame = 0
        self.size = (32, 32)
        self.sizefactor = -0.01
        self.menu_background = pygame.image.load(self.get_url("img/ui/menu_back.png")).convert_alpha()  # Arrière-plan du menu
        self.end = False  # Ordre de fermeture du jeu
        self.button_survoller = False
        self.in_setting = False

    def _cut_img(self, x, y):
        """
        Découpe une portion de l'image du joueur.

        :param x: Coordonnée x du coin supérieur gauche de la découpe.
        :param y: Coordonnée y du coin supérieur gauche de la découpe.
        :return: Surface contenant l'image découpée de 16x16 pixels.
        """
        image = pygame.Surface([16, 16], pygame.SRCALPHA)
        image.blit(pygame.image.load(self.get_url('img/player_sheet.png')).convert_alpha(), (0, 0), (x, y, 16, 16))
        return image

    def fist_draw(self):
        """
        Réinitialise l'animation en mettant la frame à zéro.
        Réinitialise la frame à zéro pour redémarrer l'animation.
        """
        self.frame = 0
        pass

    def draw(self):
        """
        Dessine les éléments de l'animation sur l'écran.
        Affiche l'arrière-plan du jeu, l'image animée du joueur et un cercle évolutif
        pour l'effet visuel.
        """
        self.screen.blit(self.game_background, (0, 0))  # Dessine l'arrière-plan
        self.screen.blit(self.image, (self.x, self.y))  # Dessine l'image du joueur
        pygame.draw.circle(self.screen, (255, 255, 255), (self.x, self.y), self.circle)  # Dessine le cercle animé
        pygame.display.flip()  # Rafraîchit l'écran

    def _gerer_event(self):
        """
        Gère les événements du jeu et met à jour l'animation.
        - Anime le joueur en modifiant son échelle et sa rotation.
        - Déplace le joueur en fonction des paramètres d'animation.
        - Gère les événements utilisateur comme la fermeture de la fenêtre.
        """
        self.draw()  # Dessine l'animation
        self.alpha += self.degre  # Incrémente l'angle pour l'animation
        self.degre += 0.0002  # Augmente le taux de changement de l'angle
        self.size = (max(self.size[0] + self.sizefactor, 0.01),
                     max(self.size[1] + self.sizefactor, 0.01))  # Modifie la taille de l'image
        self.image = pygame.transform.scale(self.image_originelle, self.size)  # Redimensionne l'image
        self.move()  # Déplace l'image selon l'angle

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quitte le jeu si l'utilisateur ferme la fenêtre
                pygame.quit()

        if self.frame >= 1720:  # Vérifie si la frame est terminée
            if self.circle >= 800:  # Si le cercle est assez grand, arrête l'animation
                self.afficher = False
            self.circle += 1  # Augmente la taille du cercle

    def move(self, sens="z"):
        """
         Déplace l'image du joueur en fonction de l'angle actuel.

         :param sens: Direction du mouvement ("z" par défaut pour avancer).
         """
        vx, vy = 0, 0
        if sens == "z":
            vx += self.speed * math.cos(self.alpha)  # Calcul de la vitesse en X
            vy += self.speed * math.sin(self.alpha)  # Calcul de la vitesse en Y
        self.x += vx  # Mise à jour de la position en X
        self.y += vy  # Mise à jour de la position en Y

    def regarder(self, angle):
        """
        Modifie l'orientation du joueur en fonction de l'angle spécifié.

        :param angle: Angle en degrés de la nouvelle direction du joueur.
        :return: None
        """
        radian = math.radians(angle)  # Convertit l'angle en radians
        self.alpha += radian  # Modifie l'angle d'orientation du joueur
        self.alpha %= math.tau  # Assure que l'angle reste dans l'intervalle [0, 2π]

    def reprendre(self):
        """
        Interrompt l'affichage de l'animation et ferme le menu.

        Met fin à l'animation en modifiant l'état d'affichage.
        """
        self.afficher = False  # Ferme le menu

    def open(self, xy):
        """
        Ouvre l'animation, réinitialise les variables et commence l'animation à la position spécifiée.

        :param xy: Tuple contenant les coordonnées de départ (x, y) pour l'animation.
        :return: None
        """
        self.circle = 0
        self.speed = 1.5
        self.alpha = math.pi
        self.degre = 0.03
        self.frame = 0
        self.x, self.y = xy[0], xy[1]
        self.size = (32, 32)
        self.image = self.image_originelle.copy()
        self.afficher = True
        self.fist_draw()  # Initialisation de la première frame
        self.game_background = pygame.display.get_surface().subsurface(
            pygame.Rect(0, 0, 800, 600)).copy()  # Copie du menu vide
        self.draw()  # Dessine l'animation

        while self.afficher:
            self.frame += 1  # Incrémente la frame
            self._gerer_event()  # Gère les événements à chaque frame

    def game_over(self, coord):
        """
        Affiche l'animation de fin de jeu, avec un cercle grandissant.

        :param coord: Coordonnées du centre du cercle.
        :return: None
        """
        self.game_background = pygame.display.get_surface().subsurface(
            pygame.Rect(0, 0, 800, 600)).copy()  # Copie du menu vide
        self.circle = 0
        while self.circle < 75:  # Affiche le cercle jusqu'à une taille maximale
            self.draw_game_over(coord)  # Dessine l'animation de fin de jeu
        self.circle = 0

    def draw_game_over(self, coord):
        """
        Dessine l'animation de fin de jeu, avec un cercle grandissant.

        :param coord: Coordonnées du centre du cercle.
        :return: None
        """
        self.circle += 0.25  # Augmente la taille du cercle
        self.screen.blit(self.game_background, (0, 0))  # Dessine l'arrière-plan
        pygame.draw.circle(self.screen, (255, 0, 0), coord, self.circle)  # Dessine un cercle rouge
        pygame.display.flip()  # Rafraîchit l'écran

    @staticmethod
    def get_url(url):
        url_list = url.split("/")
        return os.path.join(*url_list)