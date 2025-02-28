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
        self.canbullet = False

        self.frame_jump = 35 # timer de jump
        self.last_y = 0
        self.start_y = 0

    def add_verif(self):
        if self.frame_jump > 0:
            self.jump()

        if self.multi_collision(self.liste_echelle):
            self.anti_gravity()

        self.gravity()

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

        if self.multi_collision(self.liste_sol) and self.frame_jump == 0:
            if self.touche("SPACE"): # jump
                self.frame_jump = 36 #36
                self.start_y = self.player.coord[1]
                self.last_y  = self.player.coord[1]



    def quitter(self):
        if self.multi_collision(self.sortie):
            return "Ville"
        return None

    def __str__(self):
        return "Parcours"

    @staticmethod
    def f(x):
        return (x * (36 - x)) / 162

    def gravity(self):
        self.player.vy += 2

    def anti_gravity(self):
        self.player.vy -= 2

    def jump(self):
        self.anti_gravity()
        new_y = self.f(self.frame_jump)*16 + self.start_y #nouvelle coordonné
        vy = new_y - self.last_y # de combien il doit monter
        print(new_y, self.frame_jump)
        self.player.vy -= vy
        self.last_y = new_y
        self.frame_jump -= 1


