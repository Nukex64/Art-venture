from time import sleep
from tokenize import group

import pygame


class Animation:
    def __init__(self):
        self.time = 0
        self.notfinished = True

    def animer(self,player,groupe):
        groupe.remove(player)
        while self.notfinished :
            pass

    def update(self):
        print("aaa")