from carte import Carte
import pygame
import settings
class Laby(Carte):
    """
    Ce n'est pas un mini jeux juste un test de truc random
    (on peut peut etre en fair un plus tard)
    """
    def __init__(self):
        super().__init__("map/laby.tmx")
        self.zoom = settings.ZOOM
    def __str__(self):
        return "Laby"
    def add_draw(self, screen):
        mask = pygame.Surface((800, 600), pygame.SRCALPHA)
        mask.fill((0, 0, 0, 255))
        pygame.draw.circle(mask, (0, 0, 0, 0), (self.player.coord[0]+100,self.player.coord[1]+100), 100)  # Alpha = 0 -> Transparent
        print(self.player.coord[0]*2,self.player.coord[1]*2)
        screen.blit(mask, (0, 0))

