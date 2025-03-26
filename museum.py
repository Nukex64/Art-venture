import pygame
from carte import Carte

class Museum(Carte):
    def __init__(self):
        super().__init__("map/museum/musée_couloir_1.tmx")
        self.dico_tableau = {}
        self.dico_rect = {}
        for obj in self.tmx_data.objects:
            if obj.type == "paint":
                img = pygame.image.load(f"img/tableau/{obj.name}.webp")
                x = img.get_width() / img.get_width()
                img = pygame.transform.smoothscale(img, (60, 60 * x))
                self.dico_tableau[obj.name] = ((obj.x, obj.y), img)
                self.dico_rect[(obj.x, obj.y, img.get_width(), img.get_height())] = obj.name

    def add_draw(self, screen):
        for name, info in self.dico_tableau.items():
            coord, img = info
            screen.blit(img, self.fixe_coord(coord))


    def add_verif(self):
        if self.touche("e"):
            x = self.player.rect.collidedict(self.dico_rect)[1]
            if x:
                self.quiz.open(x)

    def __str__(self):
        return "Museum"