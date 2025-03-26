# Projet : Art'Venture
# Auteurs : Anthony Ibanez-Esteban, Raphaël Prost, Aëlys-Coleen Surma Valtaer, Louis Gagne, Mathéo Faure
import os

import pygame

class Tuto:
    """
    Docstring plus complet pour tester :
    Classe représentant le tutoriel du jeu Art'Venture. Gère l'affichage d'un dialogue
    interactif, ainsi que l'interaction de l'utilisateur avec les boutons de l'interface.

    Attributs:
    - screen (pygame.Surface): Surface de l'écran pour l'affichage.
    - afficher (bool): Détermine si le tutoriel est affiché ou non.
    - dialogue_box (pygame.Surface): Image de la boîte de dialogue.
    - font (pygame.font.Font): Police utilisée pour afficher le texte.
    - quit (int): Variable pour quitter le tutoriel (non utilisée dans ce code).
    - overbutton (int): Variable qui détermine si le curseur est au-dessus du bouton.
    - click_commence (pygame.Surface): Image du bouton "Commencer".
    - click_commence1 (pygame.Surface): Image du bouton "Commencer" lorsque la souris est dessus.
    - hbox (pygame.Rect): Zone délimitée par le bouton "Commencer".
    - index (int): Index de contrôle pour le texte.
    - game_background (pygame.Surface): Image de fond du jeu.
    - carparline (int): Nombre de caractères par ligne pour le texte.
    - texte (list): Liste contenant le texte du tutoriel.
    """
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.afficher = False
        self.dialogue_box = pygame.image.load(self.get_url("img/txt.png"))
        self.dialogue_box = pygame.transform.scale(self.dialogue_box, (760,560))
        self.font = pygame.font.Font(self.get_url("img/police.otf"), 30)
        self.quit = 0
        self.overbutton = 0
        self.click_commence = pygame.image.load(self.get_url("img/ui/commencer.png"))
        self.click_commence.set_colorkey((255, 255, 255))
        self.click_commence1 = pygame.image.load(self.get_url("img/ui/commencer2.png"))
        self.click_commence1.set_colorkey((255, 255, 255))
        self.hbox = pygame.rect.Rect((225, 450,225+self.click_commence.get_width(),450+self.click_commence.get_height()))

        self.index = 0
        self.game_background = None
        self.carparline = 38
        self.texte = []

    @staticmethod
    def get_url(url):
        url_list = url.split("/")
        return os.path.join(*url_list)

    def _gerer_event(self):
        """
        Gère les événements utilisateur tels que les clics et les mouvements de souris.

        Permet de fermer le tutoriel via l'appui sur la touche ESC ou le clic sur le bouton "Commencer".
        """
        x, y, = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # quitter
                self.afficher = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.afficher = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.overbutton:
                    self.afficher = False

        if self.hbox.collidepoint(x,y):
            self.overbutton = 1
        else:
            self.overbutton = 0

        if self.overbutton:
            self.screen.blit(self.click_commence,(225,450))
        else:
            self.screen.blit(self.click_commence1, (225, 450))

        pygame.display.flip()

    def splittexte(self):
        """
        Sépare le texte en plusieurs lignes en fonction du nombre de caractères par ligne
        défini par 'carparline'. Utilise des espaces pour couper le texte à la fin des mots.
        """
        i = self.carparline
        li = 0
        temptexte = []
        if len(self.texte) <= self.carparline:
            self.texte = [self.texte]
        else:
            while len(self.texte) > i:
                while self.texte[i] != ' ' or self.texte[i] == len(self.texte):
                    i-=1
                temptexte.append(self.texte[li:i])
                li = i+1
                if i+self.carparline<len(self.texte):
                    i+=self.carparline
                else:
                    i = len(self.texte)
        self.texte = temptexte

    def draw(self):
        """
        Dessine le fond du jeu, la boîte de dialogue, l'image associée et le texte sur l'écran.
        """
        self.screen.blit(self.game_background, (0,0))
        self.screen.blit(self.dialogue_box, (20, 20))
        self.screen.blit(self.img, (30,(self.screen.get_height()-self.img.get_height())/2))
        for texte in self.texte:
            a = self.font.render(texte,False,(0,0,0))
            self.screen.blit(a, (240,self.htexte))
            self.htexte += 20

        pygame.display.flip()



    def open(self,texte, img = None):
        self.afficher = True
        self.htexte = 200
        self.texte = texte
        self.splittexte()
        if img:
            self.img = pygame.image.load(img)
            size = self.img.get_rect()
            vect = 200 / size[2]
            self.img = pygame.transform.scale(self.img,(200,size[3]*vect))


        self.game_background = pygame.display.get_surface().subsurface(pygame.Rect(0, 0, 800, 600)).copy()
        self.draw()

        while self.afficher:
            self._gerer_event()