import pygame


class Painting:
    def __init__(self):
        self.img = pygame.image.load("img/car.png")

    def draw(self, screen):
        screen.fill((255, 255, 255))
        screen.blit(self.img, (66, 10))
        pygame.draw.rect(screen, (255, 0, 0), (0, 0, 10, 10))

    def __str__(self):
        return "Painting"

    def update(self):
        pass