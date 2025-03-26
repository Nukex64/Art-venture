import json
import os

import pygame
import settings
from datetime import datetime


class MainMenu:
    """
    Classe représentant le menu principal du jeu. Ce menu permet à l'utilisateur de :
    - Choisir de continuer une partie à partir de trois slots de sauvegarde.
    - Commencer une nouvelle partie dans l'un des slots de sauvegarde.
    - Réinitialiser une sauvegarde.

    Le menu inclut une animation de logo et une interface pour afficher les informations de sauvegarde.
    """
    def __init__(self):
        """
        Initialise le menu principal avec l'écran, les polices de texte, les images et les sauvegardes.

        Cette méthode charge les fichiers de sauvegarde existants, configure les images,
        et prépare les éléments graphiques nécessaires à l'affichage du menu principal.
        """
        self.reouvrir = False
        self.afficher = True
        self.screen = pygame.display.set_mode(settings.RES,pygame.SCALED)
        self.font = pygame.font.Font(settings.Font_medievale, 45)
        self.normal_font = pygame.font.Font(settings.Font, 22)
        self.date_font = pygame.font.Font(settings.Font_medievale, 22)

        self.arrow_dico = {1:(115, 375), 2:(384, 375), 3:(648, 375)}
        self.rect_1 = pygame.rect.Rect(52, 183, 166, 242)
        self.rect_2 = pygame.rect.Rect(318, 183, 166, 242)
        self.rect_3 = pygame.rect.Rect(585, 185, 166, 242)

        self.txt_1 = self.font.render("Appuyer sur un bouton", False, (0, 0, 0))
        self.logo_background = pygame.image.load(self.get_url("img/logoepee2.png"))
        self.save_background = pygame.image.load(self.get_url("img/ui/main_menu_save.png"))
        self.save_background.set_colorkey((0, 0, 0))
        self.save_arrow = pygame.image.load(self.get_url("img/ui/main_menu_arrow.png"))
        self.save_arrow.set_colorkey((0, 0, 0))
        self.logo_afficher = True
        self.logo_gamma = 255

        self.save_afficher = False
        self.save_gamma = 0

        with open("save_1.json", "r") as f:
            self.save_1 = json.load(f)
        with open("save_2.json", "r") as f:
            self.save_2 = json.load(f)
        with open("save_3.json", "r") as f:
            self.save_3 = json.load(f)

        self.saves = {1:self.save_1, 2:self.save_2, 3:self.save_3}
        self.rects = {1: self.rect_1, 2: self.rect_2, 3: self.rect_3}
        if self.save_1:
            self.jouer_1  = self.date_font.render("Continuer", True, (0, 0, 0))
            self.date_1 = self.date_font.render(self.save_1["date"], True, (0, 0, 0))
            self.progression_1 = self.date_font.render(f"Progression : {self.save_1['progression']} %", True, (0, 0, 0))
            self.temp_1 = self.date_font.render(f"Temps : {self.secondes_en_jhms(self.save_1['temps'])}", True, (0, 0, 0))
        else: self.jouer_1  = self.date_font.render("Commencer", True, (0, 0, 0))

        if self.save_2:
            self.jouer_2 = self.date_font.render("Continuer", True, (0, 0, 0))
            self.date_2 = self.date_font.render(self.save_2["date"], True, (0, 0, 0))
            self.progression_2 = self.date_font.render(f"Progression : {self.save_2['progression']} %", True, (0, 0, 0))
            self.temp_2 = self.date_font.render(f"Temps : {self.secondes_en_jhms(self.save_2['temps'])}", True, (0, 0, 0))
        else:self.jouer_2 = self.date_font.render("Commencer", True, (0, 0, 0))

        if self.save_3:
            self.jouer_3 = self.date_font.render("Continuer", True, (0, 0, 0))
            self.date_3 = self.date_font.render(self.save_3["date"], True, (0, 0, 0))
            self.progression_3 = self.date_font.render(f"Progression : {self.save_3['progression']} %", True, (0, 0, 0))
            self.temp_3 = self.date_font.render(f"Temps : {self.secondes_en_jhms(self.save_3['temps'])}", True, (0, 0, 0))
        else: self.jouer_3 = self.date_font.render("Commencer", True, (0, 0, 0))

        self.delete = self.date_font.render('X', False, (255, 0, 0))
        self.del_rect_1 = pygame.Rect(200, 185, 13, 18)
        self.del_rect_2 = pygame.Rect(469, 185, 13, 18)
        self.del_rect_3 = pygame.Rect(733, 185, 13, 18)
        self.mouse_objetif = 1

    @staticmethod
    def get_url(url):
        url_list = url.split("/")
        return os.path.join(*url_list)

    def start_save(self, nb):
        """
        Crée une nouvelle sauvegarde avec des valeurs par défaut.

        Cette méthode crée un fichier JSON pour une nouvelle sauvegarde, initialisant les données
        telles que la date de création, la progression à 0%, le temps à 0, et les informations relatives
        à chaque niveau du jeu.

        Args:
            nb (int): Le numéro de la sauvegarde (1, 2 ou 3) pour laquelle une nouvelle partie sera créée.
        """
        save= {"date": datetime.now().strftime("%d/%m/%Y"),
               "progression": "0","temps": 0,"world": "Museum",
                "Musiques": 0, "Volume": 1, "Mute": 0, "Fps": 0, "finis":
                { "Ville": 0, "Parcours": 0, "Laby": 0, "Road": 0, "Mask": 0, "Undertale": 0,
                "tresor": 0, "piano": 0, "Museum": 0},"tableau_quiz": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}

        with open(f"save_{nb}.json", "w") as f:
            json.dump(save, f, indent=2)

    def reset_save(self, nb):
        """
        Réinitialise une sauvegarde existante en écrivant un fichier JSON vide.

        Cette méthode permet de réinitialiser une sauvegarde en effaçant toutes les données de progression
        et en revenant à un état initial. Elle entraîne également la fermeture du menu principal.

        Args:
            nb (int): Le numéro de la sauvegarde à réinitialiser (1, 2 ou 3).
        """
        with open(f"save_{nb}.json", "w") as f:
            json.dump({}, f, indent=2)
        self.afficher = False
        self.reouvrir = True

    @staticmethod
    def secondes_en_jhms(secondes):
        """
        Convertit un nombre de secondes en format heures, minutes et secondes.

        Cette méthode prend un nombre de secondes et le convertit en un format lisible sous la forme
        "hh:mm:ss", afin d'afficher correctement le temps de jeu écoulé.

        Args:
            secondes (int): Le nombre de secondes à convertir.

        Returns:
            str: Le temps sous la forme "hh:mm:ss".
        """
        heures, reste = divmod(secondes, 3600)  # 3600 sec = 1 heure
        minutes, secondes = divmod(reste, 60)  # 60 sec = 1 minute
        return f"{heures}h {minutes}m"

    def draw_arrow(self):
        """
        Affiche une flèche indiquant la sauvegarde sélectionnée par l'utilisateur.

        Cette méthode dessine une flèche qui se déplace en fonction de la sélection de l'utilisateur
        parmi les trois options de sauvegarde disponibles. La flèche est affichée sur l'écran à
        la position correspondante.
        """
        pygame.draw.rect(self.screen, (255, 255, 255), (115, 375, 36, 32))
        pygame.draw.rect(self.screen, (255, 255, 255), (384, 375, 36, 32))
        pygame.draw.rect(self.screen, (255, 255, 255), (648, 375, 36, 32))
        self.screen.blit(self.save_arrow, self.arrow_dico[self.mouse_objetif])
        pygame.display.update((115, 375, 500, 32))

    def draw_save(self):
        """
        Affiche les informations relatives aux trois slots de sauvegarde.

        Cette méthode dessine les informations sur chaque sauvegarde, y compris la date de la dernière
        utilisation, la progression en pourcentage, le temps écoulé, et un bouton de suppression pour
        chaque slot. Ces informations sont affichées sur l'écran du menu principal.
        """
        self.screen.blit(self.delete, (200, 185))
        self.screen.blit(self.jouer_1, (90, 185))
        if self.save_1:
            self.screen.blit(self.progression_1, (55, 207))
            self.screen.blit(self.temp_1, (55, 230))
            self.screen.blit(self.date_1, (88, 433))


        self.screen.blit(self.delete, (469, 185))
        self.screen.blit(self.jouer_2, (359, 185))
        if self.save_2:
            self.screen.blit(self.progression_2, (324, 207))
            self.screen.blit(self.temp_2, (324, 230))
            self.screen.blit(self.date_2, (359, 433))

        self.screen.blit(self.delete, (733, 185))
        self.screen.blit(self.jouer_3, (629, 185))
        if self.save_3:
            self.screen.blit(self.progression_3, (594, 207))
            self.screen.blit(self.temp_3, (594, 230))
            self.screen.blit(self.date_3, (620, 433))

        pygame.display.flip()

    def update(self):
        """
        Met à jour l'affichage du menu principal en fonction de l'état actuel du jeu.

        Cette méthode effectue les transitions entre l'écran de logo et l'écran de sauvegarde, gère
        les animations et rafraîchit l'affichage des éléments graphiques (logo, sauvegardes).
        """
        if not self.logo_afficher and self.logo_gamma > 0:
            self.logo_gamma -=1
            self.screen.fill((100, 100, 100))
            self.logo_background.set_alpha(self.logo_gamma)
            self.txt_1.set_alpha(self.logo_gamma)
            self.screen.blit(self.logo_background, (150, 0))
            self.screen.blit(self.txt_1, ((800 - self.txt_1.get_width()) // 2, 500))
            if self.logo_gamma == 0 : self.save_afficher = True
            pygame.display.flip()

        if self.save_afficher:
            if self.save_gamma < 255:
                self.save_gamma += 1
                self.screen.fill((100, 100, 100))
                self.save_background.set_alpha(self.save_gamma)
                self.screen.blit(self.save_background, (0, 0))
                if self.save_gamma == 255: self.draw_save()
                pygame.display.flip()
            else:
                x, y = pygame.mouse.get_pos()
                if self.rect_1.collidepoint(x, y) and self.mouse_objetif != 1:
                    self.mouse_objetif = 1
                    self.draw_arrow()
                elif self.rect_2.collidepoint(x, y) and self.mouse_objetif != 2:
                    self.mouse_objetif = 2
                    self.draw_arrow()
                elif self.rect_3.collidepoint(x, y) and self.mouse_objetif != 3:
                    self.mouse_objetif = 3
                    self.draw_arrow()

    def gerer_event(self):
        """
        Gère les événements utilisateur (clics de souris et touches du clavier).

        Cette méthode traite les événements du jeu, y compris les clics de souris sur les boutons
        de sauvegarde pour sélectionner ou réinitialiser les sauvegardes. Elle gère également les
        pressions de touches pour interagir avec le menu.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # quitter
                self.afficher = False

            if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and self.logo_afficher:
                self.logo_afficher = False

            if event.type == pygame.MOUSEBUTTONDOWN and self.save_afficher:
                x, y = pygame.mouse.get_pos()
                if self.del_rect_1.collidepoint(x, y) and self.save_1: self.reset_save(1)
                if self.del_rect_2.collidepoint(x, y) and self.save_2: self.reset_save(2)
                if self.del_rect_3.collidepoint(x, y) and self.save_3: self.reset_save(3)
                self.afficher = False

    def first_draw(self):
        """
        Affiche l'écran d'introduction avec le logo du jeu avant de montrer les options de sauvegarde.

        Cette méthode dessine le logo du jeu et le texte d'instruction à l'écran avant de permettre à
        l'utilisateur de faire son choix parmi les sauvegardes disponibles.
        """
        self.screen.fill((100, 100, 100))
        self.screen.blit(self.logo_background, (150, 0))
        self.screen.blit(self.txt_1, ((800-self.txt_1.get_width())//2, 500))
        pygame.display.flip()


    def open(self):
        """
        Ouvre le menu principal, permettant à l'utilisateur de sélectionner une sauvegarde ou d'en créer une nouvelle.

        Cette méthode gère l'ouverture du menu, l'affichage des informations de sauvegarde, et le traitement
        des entrées de l'utilisateur. Elle attend que l'utilisateur fasse un choix avant de renvoyer le
        numéro de la sauvegarde sélectionnée, ou une demande de réouverture du menu.

        Returns:
            int or bool: Le numéro de la sauvegarde sélectionnée (1, 2 ou 3) ou un indicateur de réouverture du menu.
        """
        self.first_draw()
        while self.afficher:
            self.gerer_event()
            self.update()

        if not self.reouvrir:
            if not self.saves[self.mouse_objetif]:
                self.start_save(self.mouse_objetif)
            return self.mouse_objetif
        else:
            return self.reopen()

    def reopen(self):
        """
        Réinitialise l'état du menu principal et permet de le rouvrir.

        Cette méthode réinitialise tous les éléments du menu principal à leur état initial, réaffiche le logo,
        et recharge les données de sauvegarde pour permettre à l'utilisateur de choisir ou de réinitialiser
        ses sauvegardes.

        Returns:
            int or bool: Le numéro de la sauvegarde sélectionnée (1, 2 ou 3) ou un indicateur de réouverture du menu.
        """
        self.reouvrir = False
        self.afficher = True
        self.logo_afficher = True
        self.logo_gamma = 255
        self.save_afficher = False
        self.save_gamma = 0
        self.logo_background.set_alpha(255)
        self.save_background.set_alpha(0)
        self.txt_1.set_alpha(255)
        with open("save_1.json", "r") as f:
            self.save_1 = json.load(f)
        with open("save_2.json", "r") as f:
            self.save_2 = json.load(f)
        with open("save_3.json", "r") as f:
            self.save_3 = json.load(f)
        self.saves = {1: self.save_1, 2: self.save_2, 3: self.save_3}
        self.rects = {1: self.rect_1, 2: self.rect_2, 3: self.rect_3}
        if self.save_1:
            self.jouer_1 = self.date_font.render("Continuer", True, (0, 0, 0))
            self.date_1 = self.date_font.render(self.save_1["date"], True, (0, 0, 0))
            self.progression_1 = self.date_font.render(f"Progression : {self.save_1['progression']} %", True, (0, 0, 0))
            self.temp_1 = self.date_font.render(f"Temps : {self.secondes_en_jhms(self.save_1['temps'])}", True,(0, 0, 0))
        else:self.jouer_1 = self.date_font.render("Commencer", True, (0, 0, 0))

        if self.save_2:
            self.jouer_2 = self.date_font.render("Continuer", True, (0, 0, 0))
            self.date_2 = self.date_font.render(self.save_2["date"], True, (0, 0, 0))
            self.progression_2 = self.date_font.render(f"Progression : {self.save_2['progression']} %", True, (0, 0, 0))
            self.temp_2 = self.date_font.render(f"Temps : {self.secondes_en_jhms(self.save_2['temps'])}", True,(0, 0, 0))
        else:self.jouer_2 = self.date_font.render("Commencer", True, (0, 0, 0))

        if self.save_3:
            self.jouer_3 = self.date_font.render("Continuer", True, (0, 0, 0))
            self.date_3 = self.date_font.render(self.save_3["date"], True, (0, 0, 0))
            self.progression_3 = self.date_font.render(f"Progression : {self.save_3['progression']} %", True, (0, 0, 0))
            self.temp_3 = self.date_font.render(f"Temps : {self.secondes_en_jhms(self.save_3['temps'])}", True,(0, 0, 0))
        else:self.jouer_3 = self.date_font.render("Commencer", True, (0, 0, 0))

        self.delete = self.date_font.render('X', False, (255, 0, 0))
        self.del_rect_1 = pygame.Rect(200, 185, 13, 18)
        self.del_rect_2 = pygame.Rect(469, 185, 13, 18)
        self.del_rect_3 = pygame.Rect(733, 185, 13, 18)
        self.mouse_objetif = 1

        return self.open()