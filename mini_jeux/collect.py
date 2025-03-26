from platform import python_implementation

from enemy import Enemy
import pygame
from carte import Carte
from random import randint
class Collect(Carte):
    def __init__(self):
        super().__init__("map/map.tmx")
        self.enemies = []
        self.billet = Enemy("img/billet.png", 0, 0)
        self.groupe.add(self.billet)
        self.difficulty = 4
        self.player.speed = 1.5
        self.temps = 0.8*60
        self.timer_ = self.temps
        self.compte = 0

    def spawn(self):
        enemy = Enemy("img/billet.png", randint(5, 395), 0)
        enemy.image.set_colorkey([0, 255, 0])
        enemy.speed = 1
        self.groupe.add(enemy)
        self.enemies.append(enemy)
        enemy.regarder(90)

    def add_verif(self):
        if self.timer_ <= 0:
            self.spawn()
            self.timer_ = self.temps
        self.timer_ -= 1
        for enemy in self.enemies:
            enemy.avancer()
            if self.sprite_collision(enemy):
                self.compte += 1
                self.enemies.remove(enemy)
                self.groupe.remove(enemy)


    def add_draw(self, screen):
        texte_render = self.font.render(str(round(self.compte)), True, (0, 0, 0))
        screen.blit(texte_render, (0, 0))



