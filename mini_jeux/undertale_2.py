from random import *

import pygame

from carte import Carte
from enemy import Enemy


class Undertale(Carte):
    def __init__(self):
        super().__init__("map/map.tmx")
        self.enemies = []
        self.tableau = Enemy("img/fire.png", 0, 0)
        self.groupe.add(self.tableau)
        self.difficulty = 4
        self.enemies_timer = self.difficulty
        self.player.speed = 1.5
        self.decompte = 3600

        self.font = pygame.font.Font("img/police.otf", 30)



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
        if self.enemies_timer <= 0:
            self.create()
            self.enemies_timer = self.difficulty
        if self.enemies_timer > 0:
            self.enemies_timer -= 1
        for enemy in self.enemies:
            enemy.avancer()
            if enemy.is_off_screen():
                self.enemies.remove(enemy)
            if self.sprite_collision(enemy):
                exit()
        x, y = self.player.coord
        self.tableau.x, self.tableau.y = x-4, y - 10
        self.decompte -= 1
        if self.decompte <= 0: exit()

    def create(self):
        x, y = self.spawn()
        enemy = Enemy("img/fire.png", x, y)
        enemy.speed = 3
        enemy.regarder(randint(0, 90))
        self.enemies.append(enemy)
        self.groupe.add(enemy)

    def add_draw(self, screen):
        texte_render = self.font.render(str(round(self.decompte/60, 2)), True, (0, 0, 0))
        screen.blit(texte_render, (0, 0))






