import pygame

import settings
from savefonction import sauvegarde


class Menu:
    def __init__(self):
        """
        Initialise le jeu, configure la fenêtre de jeu, et définit les cartes et mini-jeux disponibles.
        """
        self.saveload = sauvegarde()
        self.afficher = True
        self.screen = pygame.display.set_mode(settings.RES,pygame.SCALED)
        self.font = pygame.font.Font(settings.Font, 65)

        self.game_background = None

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


    def fist_draw(self):
        self.screen.blit(self.menu_background, (0, 0))

    def draw(self):
        self.screen.blit(self.menu_image, (0, 0))
        pygame.display.update((225, 145, 340, 87))

    def _gerer_event(self):
        """
        Gère les événements du jeu (clavier, fermeture de la fenêtre, etc.).
        (60/s)
        """
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # quitter
                self.afficher = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.in_setting:
                        self.in_setting = False
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
        print("Reprendre")
        self.afficher = False # ferme le menu

    def quitter(self):
        print("Quitter")
        self.afficher = False # ferme le menu
        self.end = True # ferme le jeu

    def open(self):
        print("-- MENU OPEN")

        self.afficher = True
        self.fist_draw()
        self.game_background = pygame.display.get_surface().subsurface(pygame.Rect(161, 22, 474, 527)).copy() #copy du menu vide
        self.draw()

        while self.afficher:
            self._gerer_event()

        print("-- MENU END")

    def fullscreen(self):
        print("    fullscreen")
        pygame.display.toggle_fullscreen()
        pygame.display.flip()

    def musique_OnOff(self):
        if self.saveload.changer_json('Musiques',None) == 1:
            pygame.mixer_music.pause()
            print("    musique off")
            self.saveload.changer_json('Musiques',0)
        elif self.saveload.changer_json('Musiques',None) == 0:
            pygame.mixer.music.play(loops=-1)
            print("    musique on")
            self.saveload.changer_json('Musiques', 1)



    def parametre(self, click):
        a = pygame.mouse.get_pressed()[0]
        if a:
            pygame.mouse.set_visible(True)
            x = pygame.mouse.get_pos()[0]
            m = max(1, x - 357)
            print(m/218)
            if 326 <= x < 575:
                self.screen.blit(self.game_background, (161, 22))
                self.screen.blit(self.slider_d, (325, 175))
                self.slider_m = pygame.transform.scale(self.slider_m, (m, 32))
                self.screen.blit(self.slider_m, (357, 175))
                self.screen.blit(self.slider_g, (x, 175))
                pygame.display.update((225, 145, 340, 87))
                pygame.mixer.music.set_volume(m/218)
        else:
            pygame.mouse.set_visible(True)

    def open_parametre(self):
        self.in_setting = True
        self.screen.blit(self.game_background, (161, 22))
        self.screen.blit(self.slider_m, (350+40, 175))
        self.screen.blit(self.slider_d, (315, 175))
        self.screen.blit(self.slider_g, (450, 175))
        pygame.display.update((225, 145, 340, 87))