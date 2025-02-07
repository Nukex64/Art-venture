from carte import Carte
import pygame
import settings
class Laby(Carte):
    """
    Ce n'est pas un mini jeux juste un test de truc random
    (on peut peut etre en fair un plus tard)
    """
    def __init__(self):
        super().__init__("map/map.tmx"
                         )
        self.zoom = settings.ZOOM
    def __str__(self):
        return "Laby"

    def add_draw(self, screen):
        mask = pygame.Surface((800, 600), pygame.SRCALPHA)
        coord = self.fixe_coord(self.player.coord)
        mask.fill((0, 0, 0))
        pygame.draw.circle(mask, (0, 0, 0, 0), (coord[0], coord[1]), 100)
        screen.blit(mask, (0, 0))

