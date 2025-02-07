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

        image = pygame.Surface([16, 16])
        image.blit(self.image_sheet, (0, 0), (x, y, 16, 16))
        return image


    def add_draw(self, screen):
        screen.blit(self.text_1, self.fixe_coord((25, 25)))
        screen.blit(self.text_2, (625, 570))


    def add_verif(self):
        if self.touche("t"):
            print(pygame.mouse.get_pos())

            self.tp(195, 200)


    def quitter(self):
        """
        Si le joueur touche la statue et appuis sur entrer il rentre dans le parcour
        """
        if self.collision(self.tp_2):
            return "jeu_1"

        if self.collision(self.tp_3):
            return "jeu_2"

        return None

    def __str__(self):
        return "Ville"