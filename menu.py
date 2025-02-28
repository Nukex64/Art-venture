import pygame
from savefonction import sauvegarde
import settings

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

    def musique(self):
        if self.saveload.changer_json('Musiques',None) == 1:
            pygame.mixer_music.pause()
            print("    musique off")
            self.saveload.changer_json('Musiques',0)
        elif self.saveload.changer_json('Musiques',None) == 0:
            pygame.mixer.music.play(loops=-1)
            print("    musique on")
            self.saveload.changer_json('Musiques', 1)

    def parametre(self, click):
        if click:
            self.musique()

    def open_parametre(self):
        self.in_setting = True
        self.screen.blit(self.game_background, (161, 22))
        pygame.display.update((225, 145, 340, 87))