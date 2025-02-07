#Exemple
from carte import Carte
class Game_Jump(Carte):
    """
    Exemple de mini jeux de jump / parcoure
    """
    def __init__(self):
        super().__init__("map/jump.tmx") # on donne la map
        self.liste_echelle = self.objets_par_classe('echelle') # on recupere les echelles
        self.sortie = self.objets_par_classe('sortie')
        self.liste_sol = self.objet_par_calque('sol') # on recupere les sols
        self.time_jump = 0 # timer de jump

    def add_verif(self):
        if self.time_jump: # jump
            self.player.haut(1.75) # effet 1.75 - gravité = 0.75 (voir player)
            self.time_jump -= 1

        if self.multi_collision(self.liste_echelle):
            self.player.haut() # contre l'effet de la gravité sur les echelles

        self.player.bas() # gravité

    def clavier(self):
        if self.touche("d"):
            self.player.droite()
            self.player.regarder('droite')

        if self.touche("q"):
            self.player.gauche()
            self.player.regarder('gauche')

        if self.multi_collision(self.liste_echelle): # si il est sur l'echelle
            self.player.regarder('haut')
            if self.touche("z") :
                self.player.haut()
            if self.touche("s"):
                self.player.bas()

        if self.multi_collision(self.liste_sol):
            if self.touche("SPACE"): # jump
                self.time_jump = 200*0.06 #200ms (0.06 car 60/s = 0.06/ms)



    def quitter(self):
        if self.multi_collision(self.sortie):
            return "ville"
        return None

    def __str__(self):
        return "Parcours"

