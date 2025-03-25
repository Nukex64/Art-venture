import pygame
from carte import Carte
class Museum(Carte):
    def __init__(self):
        super().__init__("map/map.tmx")
    def __str__(self):
        return "Museum"