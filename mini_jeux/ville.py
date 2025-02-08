import math

from carte import Carte
import pygame

class Ville(Carte):
    """
    Ce n'est pas un mini jeux juste un test de truc random
    (on peut peut etre en fair un plus tard)
    """
    def __init__(self):
        super().__init__("map/map.tmx")
        self.tp_2 = self.objet_par_nom("tp_2")
        self.tp_3 = self.objet_par_nom("tp_3")
        self.text_1 = self.font.render("Je suis un text fixe", True, (0, 0, 0))
        self.text_2 = self.font.render("Je suis un text d'UI", True, (0, 0, 0))



    def add_draw(self, screen):
        screen.blit(self.text_1, self.fixe_coord((25, 25)))
        screen.blit(self.text_2, (625, 570))
        self.ray(screen)

    def add_verif(self):
        if self.touche("t"):
            print(pygame.mouse.get_pos())


    def quitter(self):
        """
        Si le joueur touche la statue et appuis sur entrer il rentre dans le parcour
        """
        if self.collision(self.tp_2):
            return "jeu_1"

        if self.collision(self.tp_3):
            return "jeu_2"

        return None

    def ray(self, screen):
        x2, y2 = pygame.mouse.get_pos()
        x1, y1 = self.fixe_coord(self.player.rect.center)
        vx, vy = x2-x1, y2-y1
        norm = math.sqrt(vx**2 + vy**2)
        vx, vy = vx/norm, vy/norm
        x, y = x1+vx*75, y1+vy*75
        pygame.draw.line(screen, 'red', (x1, y1), (x,y), 1)

    def __str__(self):
        return "Ville"