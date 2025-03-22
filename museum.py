import pygame
from carte import Carte
class Museum(Carte):
    def __init__(self):
        super().__init__("map/museum/musée_couloir_1.tmx")
    def __str__(self):
        return "Museum"