# Projet : Art'Venture
# Auteurs : Anthony Ibanez-Esteban, Raphaël Prost, Aëlys-Coleen Surma Valtaer, Louis Gagne, Mathéo Faure
import change_url
import json
import pygame
from MainMenu import MainMenu
from menu import Menu
from mini_jeux.laby import Laby
from mini_jeux.mask import Mask
from mini_jeux.parcours import *
from mini_jeux.piano import Piano
from mini_jeux.road import Road
from mini_jeux.swim import Swim
from mini_jeux.tresor import Tresor
from mini_jeux.undertale_2 import Undertale
from mini_jeux.ville import Ville
from museum import *
from savefonction import sauvegarde
from settings import *
from datetime import datetime
import os

class Jeu:
    def __init__(self):
        """
        Initialise le jeu en configurant la fenêtre, la musique, les mini-jeux et les cartes disponibles.
        Charge également les paramètres initiaux comme la fréquence d'affichage et l'icône de la fenêtre.
        """
        self.save_nb = None
        pygame.mixer.music.load(self.get_url("sounds/projectnsi.mp3"))
        pygame.mixer.music.set_volume(0)  # Mettre la musique à 0 au démarrage
        self.run = True
        self.screen = pygame.display.set_mode(RES, pygame.NOFRAME | pygame.SCALED)  # Création de la fenêtre du jeu
        self.clock = pygame.time.Clock()
        self.draw_fps = 60  # Fréquence d'affichage par défaut
        self.saveload = None  # Variable pour charger la sauvegarde
        ico = pygame.image.load(self.get_url("img/logoepee2.png")).convert_alpha()
        pygame.display.set_icon(ico)  # Définit l'icône du jeu

        # Initialisation des mini-jeux et cartes
        ville = Ville()
        parcour_1 = Game_Jump()
        laby = Laby()
        road = Road()
        mask = Mask()
        piano = Piano()
        undertale = Undertale()
        tresor = Tresor()
        museum_haut = None
        museum_hall = None
        museum_bas = None
        swim = Swim()

        # Dictionnaire des cartes et mini-jeux
        self.dico_game = {"Ville": ville, "Parcours": parcour_1, "Laby": laby, "Road": road, "Mask": mask,
                          "Undertale": undertale,
                          "Tresor": tresor, "piano": piano, "Museum_haut": museum_haut, "Museum_hall": museum_hall,
                          "Museum_bas": museum_bas, "swim": swim}
        self.time_entry = 0  # Stocke le temps de début de session
        self.carte = None  # Carte actuelle du jeu (sera chargée plus tard)
        self.menu = None
        self.main_menu = MainMenu()  # Menu principal du jeu

    @staticmethod
    def get_url(url):
        url_list = url.split("/")
        return os.path.join(*url_list)

    def charger_save(self, nb):
        """
        Charge une sauvegarde spécifique et initialise les paramètres du jeu (cartes, musique, volume, FPS).

        :param nb: Numéro de la sauvegarde à charger.
        """
        self.save_nb = nb

        # Chargement des musées en fonction de la sauvegarde
        museum_haut = Museum_haut(self.save_nb)
        museum_hall = Museum_hall(self.save_nb)
        museum_bas = Museum_bas(self.save_nb)
        self.dico_game["Museum_hall"] = museum_hall
        self.dico_game["Museum_bas"] = museum_bas
        self.dico_game["Museum_haut"] = museum_haut

        self.saveload = sauvegarde(nb)  # Chargement de la sauvegarde
        self.menu = Menu(nb)  # Initialisation du menu de jeu
        pygame.mixer.music.set_volume(self.saveload.changer_json("Volume", None))  # Applique le volume enregistré
        if self.saveload.changer_json("Musiques", None):
            pygame.mixer.music.play(loops=-1)  # Joue la musique en boucle
        self.draw_fps = self.saveload.changer_json("Fps")  # Récupération des FPS sauvegardés
        self.carte = self.dico_game[self.saveload.changer_json("world")]  # Chargement de la carte actuelle

    def _get_suface(self):
        """
        Crée et renvoie la surface à dessiner sur l'écran. Cette surface contient la carte actuelle du jeu.

        :return: Surface avec la carte actuelle dessinée dessus.
        """
        surface = pygame.Surface(RES)
        self.carte.draw(surface)  # Dessine la carte sur la surface
        return surface

    def _update(self):
        """
        Met à jour l'affichage et l'état du jeu. Cette méthode est appelée à chaque frame du jeu.
        Limite l'affichage à 60 FPS et met à jour les objets du jeu.
        """
        self.clock.tick(60)  # Limite l'affichage à 60 FPS
        self.carte.update()  # Met à jour les objets du jeu
        self.screen.blit(self._get_suface(), (0, 0))  # Affiche la carte sur l'écran
        if self.draw_fps:
            pygame.display.set_caption(f"Art'venture {self.clock.get_fps():.1f}")
        else:
            pygame.display.set_caption("Art'venture")
        pygame.display.flip()  # Rafraîchit l'écran

    def _changer_carte(self):
        """
        Change la carte actuelle en fonction des transitions du jeu.
        Si un objectif est atteint sur la carte actuelle, cette méthode charge la nouvelle carte.
        """
        objetif = self.carte.objetif  # Récupération de la nouvelle carte
        self.carte.objetif = None
        if objetif in self.dico_game:
            if objetif not in ["Museum_hall", "Museum_bas", "Museum_haut"]:
                self.carte.appelanimation()
            self.carte = self.dico_game[objetif]
            self.saveload.reload_json()
            self.saveload.changer_json("world", str(self.carte))  # Sauvegarde la nouvelle carte

    def quitter(self):
        """
        Quitte proprement le jeu en sauvegardant le temps de jeu écoulé.
        """
        temps_ecoule = datetime.now() - self.time_entry
        last_time = self.saveload.changer_json("temps")
        self.saveload.changer_json("temps", last_time + temps_ecoule.total_seconds())
        self.run = False

    def _gerer_event(self):
        """
        Gère les événements du jeu tels que les entrées clavier et souris, ainsi que la fermeture de la fenêtre.
        Appelle également les méthodes liées aux interactions du joueur avec la carte et les menus.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quitter()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    print(pygame.mouse.get_pos())
                if event.key == pygame.K_KP0:
                    self.carte = self.dico_game["Ville"]
                if event.key == pygame.K_ESCAPE:
                    self.menu.open()
                    self.saveload.reload_json()
                    self.draw_fps = self.saveload.changer_json("Fps")
                    if self.menu.end:
                        self.run = False
                self.carte.keypressed(event)

        if self.carte.objetif:
            self._changer_carte()

    def running(self):
        """
        Démarre la boucle principale du jeu.
        Charge une sauvegarde, gère les événements du jeu, et met à jour l'affichage à chaque frame.
        """
        save = 1
        # save = self.main_menu.open() #mettre en commentaire pour coder sans
        self.time_entry = datetime.now()
        self.charger_save(save)
        while self.run:
            self._gerer_event()
            self._update()


if __name__ == '__main__':
    #change_url.transform_to() NE PAS FAIRE
    pygame.init()
    jeu = Jeu()
    jeu.running()
    pygame.quit()
