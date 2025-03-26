#Projet : Art'Venture
#Auteurs : Anthony Ibanez-Esteban, Raphaël Prost, Aëlys-Coleen Surma Valtaer, Louis Gagne, Mathéo Faure
import os

import pygame

import settings
from savefonction import sauvegarde

class Menu:
    """
    Classe représentant le menu principal du jeu, permettant à l'utilisateur d'interagir avec les options
    telles que la musique, le mode plein écran, le volume, et les paramètres du jeu.

    Le menu propose également une interface pour reprendre une partie, ouvrir les paramètres, ou quitter le jeu.
    """

    def __init__(self, save_nb):
        """
        Initialise le menu avec les paramètres de sauvegarde et les éléments d'interface.

        Args:
            save_nb (int): Le numéro de la sauvegarde à charger.
        """
        self.saveload = sauvegarde(save_nb)
        self.afficher = True
        self.screen = pygame.display.set_mode(settings.RES,pygame.SCALED)
        self.font = pygame.font.Font(settings.Font, 65)
        self.font_setting = pygame.font.Font(settings.Font, 40)
        self.txt_music = self.font_setting.render("Musique", True, (0, 0, 0))
        self.txt_fs = self.font_setting.render("Mode large", True, (0, 0, 0))
        self.txt_volume = self.font_setting.render("Volume", True, (0, 0, 0))
        self.txt_fps = self.font_setting.render("Fps", True, (0, 0, 0))
        self.volume = self.saveload.changer_json("Volume")
        self.game_background = None

        self.menu_background = pygame.image.load(self.get_url("img/ui/menu_back.png")).convert_alpha()

        self.menu_image = pygame.image.load(self.get_url("img/ui/menu.png"))

        self.rect_reprendre = pygame.Rect(225, 145, 340, 87)
        self.rect_parametre = pygame.Rect(225, 145+130, 340, 87)
        self.rect_quitter = pygame.Rect(225, 145+260, 340, 87)

        self.click_parametre = pygame.image.load(self.get_url("img/ui/BsettingsC.png"))
        self.click_parametre.set_colorkey((255, 255, 255))
        self.click_exit = pygame.image.load(self.get_url("img/ui/BexitC.png"))
        self.click_exit.set_colorkey((255, 255, 255))
        self.click_reprendre = pygame.image.load(self.get_url("img/ui/BbackC.png"))
        self.click_reprendre.set_colorkey((255, 255, 255))

        img = pygame.image.load(self.get_url("img/ui/slider_yellow_.png"))
        self.slider_d = pygame.Surface([32, 32], pygame.SRCALPHA)
        self.slider_d.blit(img, (0, 0), (0, 0, 32, 32))
        self.slider_g = img.subsurface((38, 0, 32, 32))
        self.slider_m = pygame.transform.scale(self.slider_d.subsurface((30, 0, 2, 32)), (30, 32))
        self.slider_back = pygame.image.load(self.get_url("img/ui/slider_grey_.png"))
        self.slider_size = self.saveload.changer_json("Volume")*218

        self.button_fs_f = pygame.image.load(self.get_url("img/ui/check_button_off.png"))
        self.button_fs_o = pygame.image.load(self.get_url("img/ui/check_button_on.png"))
        self.rect_music = pygame.Rect((325, 215, 48, 48))
        self.rect_fs = pygame.Rect((325, 275, 48, 48))
        self.rect_fps = pygame.Rect((325, 350, 48, 48))

        self.fs = False
        self.music = self.saveload.changer_json("Mute")
        self.fps = self.saveload.changer_json("Fps")
        self.end = False  # ordonne de fermer le jeu

        self.button_survoller = False
        self.in_setting = False


    @staticmethod
    def get_url(url):
        url_list = url.split("/")
        return os.path.join(*url_list)

    def fist_draw(self):
        self.screen.blit(self.menu_background, (0, 0))

    def draw(self):
        self.screen.blit(self.menu_image, (0, 0))
        pygame.display.update((225, 145, 340, 87))

    def _gerer_event(self):
        """
        Gère les événements du jeu, y compris la gestion des clics de souris et des touches du clavier.
        Permet de quitter le jeu ou d'ouvrir les paramètres du menu.
        """
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # quitter
                self.quitter()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.in_setting:
                        self.in_setting = False
                        self.screen.blit(self.game_background, (161, 22))
                    else:
                        self.afficher = False

                if event.key == pygame.K_SPACE:
                    self.fullscreen()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True

        x, y, = pygame.mouse.get_pos()

        if not self.in_setting:
            if self.rect_reprendre.collidepoint(x, y):
                if not self.button_survoller:
                    self.screen.blit(self.click_reprendre, (216, 141))
                    pygame.display.update(self.rect_reprendre)
                    self.button_survoller = True
                if click : self.reprendre()

            elif self.rect_parametre.collidepoint(x, y):
                if not self.button_survoller:
                    self.screen.blit(self.click_parametre, (216, 142 + 130))
                    pygame.display.update(self.rect_parametre)
                    self.button_survoller = True

                if click: self.open_parametre()

            elif self.rect_quitter.collidepoint(x, y):
                if not self.button_survoller:
                    self.screen.blit(self.click_exit, (214, 140 + 260))
                    pygame.display.update(self.rect_quitter)
                    self.button_survoller = True
                if click: self.quitter()

            else:
                if self.button_survoller:
                    self.button_survoller = False
                    self.draw()

        # PARAMETRE ----------------------------------
        else:
            self.parametre(click)


    def reprendre(self):
        """
        Ferme le menu et reprend le jeu.
        """
        self.afficher = False # ferme le menu

    def quitter(self):
        """
        Ferme le menu et termine le jeu.
        """
        self.afficher = False # ferme le menu
        self.end = True # ferme le jeu

    def open(self):
        """
        Affiche le menu principal et gère les événements jusqu'à ce que l'utilisateur quitte ou ferme le menu.

        Enregistre les paramètres actuels (FPS, volume, musique) à la fermeture
        """
        self.afficher = True
        self.fist_draw()
        self.game_background = pygame.display.get_surface().subsurface(pygame.Rect(161, 22, 474, 527)).copy() #copy du menu vide
        self.draw()

        while self.afficher:
            self._gerer_event()

        self.saveload.changer_json("Fps", self.fps)
        self.saveload.changer_json("Volume", round(self.volume,4))
        self.music = self.saveload.changer_json("Mute", self.music)

    def fps_OnOff(self):
        """
        Active ou désactive l'option FPS.
        """
        self.fps = (0 if self.fps else 1)

    def fullscreen(self):
        """
        Passe le jeu en mode plein écran ou le remet en mode fenêtré.
        """
        self.fs = (False if self.fs else True)
        pygame.display.toggle_fullscreen()
        pygame.display.flip()

    def musique_OnOff(self):
        """
        Active ou désactive la musique du jeu. Enregistre l'état dans la sauvegarde.
        """
        if self.saveload.changer_json('Musiques',None) == 1:
            self.music = 0
            pygame.mixer_music.pause()
            self.saveload.changer_json('Musiques',0)
        elif self.saveload.changer_json('Musiques',None) == 0:
            self.music = 1
            pygame.mixer.music.play(loops=-1)
            self.saveload.changer_json('Musiques', 1)



    def parametre(self, first_press):
        """
        Gère l'affichage et l'interaction avec les paramètres du menu (volume, musique, plein écran, FPS).
        Modifie le volume selon la position du curseur et active/désactive les options en fonction des clics.

        Args:
            first_press (bool): Indique si le premier clic a été effectué sur l'un des boutons de paramétrage.
        """
        a = pygame.mouse.get_pressed()[0]
        if a:
            self.screen.blit(self.game_background, (161, 22))
            x, y = pygame.mouse.get_pos()
            if abs(175 - y) < 32:
                m = max(1, x - 357)
                if 325 <= x < 575:
                    self.slider_size = m
                    pygame.mixer.music.set_volume(m/218)
                    self.volume = m/218
            if first_press:
                if self.rect_music.collidepoint(x, y) : self.musique_OnOff()
                elif self.rect_fs.collidepoint(x, y) : self.fullscreen()
                elif self.rect_fps.collidepoint(x, y) : self.fps_OnOff()

            self.draw_slider()
            self.draw_txt()
            self.check_button()
            pygame.display.update((225, 145, 340, 87))

    def open_parametre(self):
        """
        Affiche l'interface des paramètres du jeu et permet à l'utilisateur d'ajuster les réglages.
        """
        self.in_setting = True
        self.draw_txt()
        self.screen.blit(self.game_background, (161, 22))
        self.draw_slider()
        self.check_button()
        pygame.display.update((225, 145, 340, 87))

    def draw_slider(self):
        """
        Dessine le curseur de volume et l'ajuste en fonction de la position de la souris.
        """
        self.screen.blit(self.slider_back, (325, 174))
        self.screen.blit(self.slider_d, (325, 175))
        if self.slider_size > 1.1:
            self.slider_m = pygame.transform.scale(self.slider_m, (self.slider_size , 32))
            self.screen.blit(self.slider_m, (357, 175))
            self.screen.blit(self.slider_g, (357 + self.slider_size , 175))

    def check_button(self):
        """
        Vérifie l'état des boutons de contrôle (mode plein écran, musique, FPS) et les affiche en conséquence.
        """
        if self.fs :self.screen.blit(self.button_fs_o, (340, 290))
        else:self.screen.blit(self.button_fs_f, (340, 290))
        if self.music:self.screen.blit(self.button_fs_o, (340, 225))
        else:self.screen.blit(self.button_fs_f, (340, 225))
        if self.fps:self.screen.blit(self.button_fs_o, (340, 350))
        else:self.screen.blit(self.button_fs_f, (340, 350))

    def draw_txt(self):
        """
        Dessine les textes des différentes options (Volume, Musique, Mode plein écran, FPS) sur l'écran.
        """
        self.screen.blit(self.txt_volume, (181, 180))
        self.screen.blit(self.txt_music, (181, 236))
        self.screen.blit(self.txt_fs, (181, 298))
        self.screen.blit(self.txt_fps, (181, 355))