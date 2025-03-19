import pygame
from carte import Carte
from enemy import Enemy
from random import randint

class Swim(Carte):
    def __init__(self):
        super().__init__("map/map.tmx")
        self.temps = 5 * 60
        self.decompte = self.temps
        self.bubbles = []
        self.spawn_bubbles = [(randint(5, 380), randint(5, 300)), (randint(5, 380), randint(5, 300)), (randint(5, 380), randint(5, 300)),(randint(5, 380), randint(5, 300))]
        self.player.speed = 1
        self.spawn()
    def add_verif(self):
        if self.decompte <= 0:
            exit()
        for bub in self.bubbles:
            if self.sprite_collision(bub):
                self.decompte = self.temps
                self.groupe.remove(bub)
                self.bubbles.remove(bub)
                print(self.decompte)

        self.decompte -= 1

    def spawn(self):
        for x in range(len(self.spawn_bubbles)):
            bubble = Enemy("img/bubble.png", self.spawn_bubbles[x][0]  , self.spawn_bubbles[x][1])
            self.bubbles.append(bubble)
            self.groupe.add(bubble)
            self.decompte = self.temps

    def add_draw(self, screen):
        texte_render = self.font.render(str(round(self.decompte/60, 2)), True, (0, 0, 0))
        screen.blit(texte_render, (0, 0))







