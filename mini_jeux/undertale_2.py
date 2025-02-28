from carte import Carte
from enemy import Enemy
from random import*
class Undertale(Carte):
    def __init__(self):
        super().__init__("map/map.tmx")
        self.enemies = {}
        self.nombre = 0
        self.timer = 0



    def spawn(self):
        r = randint(0, 1)
        if r ==0:
            return randint(0, 800), 0
        else:
            return 0, randint(0, 600)


    def coord_random(self):
        r = randint(0, 1)
        if r == 0:
            return 800, randint(0, 600)
        else:
            return randint(0, 800), 600

    def add_verif(self):
        if self.timer == 0:
            self.create()
        if self.timer != 0:
            self.timer -= 1
        for keys in self.enemies:
            self.enemies[keys].viser(self.coord_random())


    def create(self):
        self.timer = 1/10*60 #sec * tps
        self.enemies["enemie"+str(self.nombre)] = Enemy("img/meteor.png", self.spawn()[0], self.spawn()[1])
        self.enemies["enemie" + str(self.nombre)].vitesse = 4
        self.groupe.add(self.enemies["enemie"+str(self.nombre)])
        self.nombre += 1






