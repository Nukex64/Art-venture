import json
import pygame
import settings
from datetime import datetime


class MainMenu:
    def __init__(self):
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
        self.logo_background = pygame.image.load("img/logoepee2.png")
        self.save_background = pygame.image.load("img/ui/main_menu_save.png")
        self.save_background.set_colorkey((0, 0, 0))
        self.save_arrow = pygame.image.load("img/ui/main_menu_arrow.png")
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

    def start_save(self, nb):
        print(f"Save {nb} creer")
        save= {"date": datetime.now().strftime("%d/%m/%Y"),
               "progression": "0","temps": 0,"world": "Ville",
                "Musiques": 0, "Volume": 1, "Mute": 0, "Fps": 0, "finis":
                   { "Ville": 0, "Parcours": 0, "Laby": 0, "Road": 0, "Mask": 0, "Undertale": 0,
                     "tresor": 0, "piano": 0, "Museum": 0}}

        with open(f"save_{nb}.json", "w") as f:
            json.dump(save, f, indent=2)

    def reset_save(self, nb):
        print(f"Save {nb} delete")
        with open(f"save_{nb}.json", "w") as f:
            json.dump({}, f, indent=2)
        self.afficher = False
        self.reouvrir = True

    @staticmethod
    def secondes_en_jhms(secondes):
        heures, reste = divmod(secondes, 3600)  # 3600 sec = 1 heure
        minutes, secondes = divmod(reste, 60)  # 60 sec = 1 minute
        return f"{heures}h {minutes}m"

    def draw_arrow(self):
        pygame.draw.rect(self.screen, (255, 255, 255), (115, 375, 36, 32))
        pygame.draw.rect(self.screen, (255, 255, 255), (384, 375, 36, 32))
        pygame.draw.rect(self.screen, (255, 255, 255), (648, 375, 36, 32))
        self.screen.blit(self.save_arrow, self.arrow_dico[self.mouse_objetif])
        pygame.display.update((115, 375, 500, 32))

    def draw_save(self):
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # quitter
                self.afficher = False

            if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and self.logo_afficher:
                self.logo_afficher = False

            if event.type == pygame.MOUSEWHEEL:
                print(pygame.mouse.get_pos())

            if event.type == pygame.MOUSEBUTTONDOWN and self.save_afficher:
                x, y = pygame.mouse.get_pos()
                if self.del_rect_1.collidepoint(x, y) and self.save_1: self.reset_save(1)
                if self.del_rect_2.collidepoint(x, y) and self.save_2: self.reset_save(2)
                if self.del_rect_3.collidepoint(x, y) and self.save_3: self.reset_save(3)
                self.afficher = False

    def first_draw(self):
        self.screen.fill((100, 100, 100))
        self.screen.blit(self.logo_background, (150, 0))
        self.screen.blit(self.txt_1, ((800-self.txt_1.get_width())//2, 500))
        pygame.display.flip()

    def open(self):
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