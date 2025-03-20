#Projet : Art'Venture
#Auteurs : Anthony Ibanez-Esteban, Raphaël Prost, Aëlys-Coleen Surma Valtaer, Louis Gagne, Mathéo Faure

import pygame

import settings
from savefonction import sauvegarde


class Animation:
    def __init__(self):
        """
        Initialise le jeu, configure la fenêtre de jeu, et définit les cartes et mini-jeux disponibles.
        """
        self.saveload = sauvegarde()
        self.afficher = True
        self.screen = pygame.display.set_mode(settings.RES,pygame.SCALED)
        self.font = pygame.font.Font(settings.Font, 65)
        self.volume = self.saveload.changer_json("Volume")
        self.game_background = None
        self.frame = 0
        self.images = self._cut_img(4, 80)



        self.menu_background = pygame.image.load("img/ui/menu_back.png").convert_alpha()

        self.menu_image = pygame.image.load("img/ui/menu.png")

        self.rect_reprendre = pygame.Rect(225, 145, 340, 87)
        self.rect_parametre = pygame.Rect(225, 145+130, 340, 87)
        self.rect_quitter = pygame.Rect(225, 145+260, 340, 87)

        self.click_parametre = pygame.image.load("img/ui/BsettingsC.png")
        self.click_parametre.set_colorkey((255, 255, 255))
        self.click_exit = pygame.image.load("img/ui/BexitC.png")
        self.click_exit.set_colorkey((255, 255, 255))
        self.click_reprendre = pygame.image.load("img/ui/BbackC.png")
        self.click_reprendre.set_colorkey((255, 255, 255))

        img = pygame.image.load("img/txt.png")
        print(img.get_rect())
        self.slider_d = pygame.Surface([32, 32], pygame.SRCALPHA)
        self.slider_d.blit(img, (0, 0), (0, 0, 32, 32))
        self.slider_g = img.subsurface((38, 0, 32, 32))
        self.slider_m = pygame.transform.scale(self.slider_d.subsurface((30, 0, 2, 32)), (30, 32))


        self.end = False #ordonne de fermer le jeu

        self.button_survoller = False
        self.in_setting = False

    def _cut_img(self, x, y):
        """
        :x/y: int (coord)
        Decoupe l'image du joueur de taille 16x16 a l'emplacement (x,y)
        """
        image = pygame.Surface([16, 16], pygame.SRCALPHA)
        image.blit(pygame.image.load('img/player_sheet.png').convert_alpha(), (0, 0), (x, y, 16, 16))
        image = pygame.transform.scale(image, (32,32))
        return image

    def fist_draw(self):
        print("a")
        pass

    def draw(self):
        self.screen.blit(self.game_background,(0,0))
        self.screen.blit(self.images, (self.frame, self.frame))
        pygame.display.update((0,0,600,800))

    def _gerer_event(self):
        """
        Gère les événements du jeu (clavier, fermeture de la fenêtre, etc.).
        (60/s)
        """
        self.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # quitter
                self.afficher = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.in_setting:
                        self.in_setting = False
                    else:
                        self.afficher = False




    def reprendre(self):
        self.afficher = False # ferme le menu

    def open(self):
        print("-- Anim Start")

        self.afficher = True
        self.fist_draw()
        self.game_background = pygame.display.get_surface().subsurface(pygame.Rect(0, 0, 800,600)).copy() #copy du menu vide
        self.draw()

        while self.afficher:
            self.frame += 1
            self._gerer_event()
        print("-- Anim END")




    def open_parametre(self):
        self.in_setting = True
        self.screen.blit(self.game_background, (0, 0))
        self.screen.blit(self.slider_m, (350+40, 175))
        self.screen.blit(self.slider_d, (315, 175))
        self.screen.blit(self.slider_g, (450, 175))
        pygame.display.update((225, 145, 340, 87))