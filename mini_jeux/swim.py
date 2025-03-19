import pygame
from carte import Carte
from enemy import Enemy

class Swim(Carte):
    def __init__(self):
        super().__init__("map/map.tmx")
        self.temps = 5 * 60
        self.decompte = self.temps
        self.bubbles = []
        self.spawn_bubbles = [(0, 0), (10, 10), (40, 70), (40, 20)]
        self.spawn()

    def add_verif(self):
        if self.decompte <= 0:
            exit()
        for bubble in self.bubbles:
            if self.collision(bubble):
                self.groupe.remove(bubble)
                self.bubbles.remove(bubble)
        self.decompte -= 1

    def spawn(self):
        for x in self.spawn_bubbles:
            bubble = Enemy("img/bubble.png", 40, 40)
            self.groupe.add(bubble)
            self.decompte = self.temps

    def add_draw(self, screen):
        texte_render = self.font.render(str(round(self.decompte/60, 2)), True, (0, 0, 0))
        screen.blit(texte_render, (0, 0))







