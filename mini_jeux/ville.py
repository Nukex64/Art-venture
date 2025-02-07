from carte import Carte

class Ville(Carte):
    """
    Ce n'est pas un mini jeux juste un test de truc random
    (on peut peut etre en fair un plus tard)
    """
    def __init__(self):
        super().__init__("map/map.tmx")
        self.tp_2 = self.objet_par_nom("tp_2")
        self.tp_3 = self.objet_par_nom("tp_3")
        self.text_surface = self.font.render("Je suis un text", True, (0, 0, 0))

    def add_draw(self, screen):
        screen.blit(self.text_surface, (10, 10))

    def add_verif(self):
        if self.touche("t"):
            self.tp(200, 200)

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