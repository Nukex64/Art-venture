import pygame
from carte import Carte
from enemy import Enemy

class Swim(Carte):
    def __init__(self):
        super().__init__("map/jump.tmx")
