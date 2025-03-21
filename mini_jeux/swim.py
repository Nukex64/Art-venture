import pygame
from carte import Carte
from enemy import Enemy
from random import randint

class Swim(Carte):
    def __init__(self):
        super().__init__("map/eau.tmx")
        self.temps = 5 * 60
        self.decompte = self.temps
        self.bubbles = []
        self.spawn_bubbles = [(16.8333, 180.5), (155.63, 30.7), (225.23, 73.3), (138.83, 201.7), (80.03, 167.5), (19.433, 319.9), (167.033, 370.9), (336.23, 376.9), (230.83, 372.5), (219.23, 248.5), (198.233, 188.5), (360.8333, 125.5)]
        self.coin = Enemy("img/coin.png", 372.8333, 368.5)
        self.groupe.add(self.coin)
        self.has_key = 0
        self.player.speed = 0.6
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
        print(self.player.coord)
        self.decompte -= 1
        if self.sprite_collision(self.coin):
            self.groupe.remove(self.coin)
            self.has_key = 1

    def spawn(self):
        for x in range(len(self.spawn_bubbles)):
            bubble = Enemy("img/bubble.png", self.spawn_bubbles[x][0]  , self.spawn_bubbles[x][1])
            self.bubbles.append(bubble)
            self.groupe.add(bubble)
            self.decompte = self.temps
    def add_draw(self, screen):
        texte_render = self.font.render(str(round(self.decompte/60, 2)), True, (255, 255, 255))
        screen.blit(texte_render, (0, 0))








