from symtable import Class

from carte import Carte
import settings
import pygame
import math

class Piano():
    def __init__(self):
        self.hg = 200
        self.dico ={100:[1]}
        self.frame = 0
        self.liste = [[],[],[],[]]
        self.image = pygame.image.load("img/fire.png")
        self.image2 = pygame.image.load("img/fire.png")
        self.image3 = pygame.image.load("img/fire.png")
        self.image4 = pygame.image.load("img/fire.png")
        largeurimage = self.image.get_rect()[3]/2
        self.xcolone = [125-largeurimage,225-largeurimage,325-largeurimage,425-largeurimage]
        print(self.xcolone)
    def draw(self, screen):
        pygame.draw.rect(screen,(255,255,255),(self.hg-100,0,175,600))
        pygame.draw.rect(screen, (0, 255, 255), (self.hg+75, 0, 100, 600))
        pygame.draw.rect(screen, (255, 0, 255), (self.hg+175, 0, 100, 600))
        pygame.draw.rect(screen, (255, 255, 0), (self.hg+275, 0, 100, 600))
        pygame.draw.rect(screen, (255, 0, 0), (self.hg+375, 0, 100, 600))

    def apparaitre(self):
        if self.frame / 60 in self.dico:
            for elt in self.dico[self.frame]:
                self.liste[elt].append(0)
                print(self.liste)
        pass


    def deplacement(self):
        for liste in self.liste:
            for y in liste :
                y += 1
        pass

    def update(self):
        self.frame+=1
        pass

