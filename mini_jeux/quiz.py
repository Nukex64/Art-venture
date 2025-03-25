#Projet : Art'Venture
#Auteurs : Anthony Ibanez-Esteban, Raphaël Prost, Aëlys-Coleen Surma Valtaer, Louis Gagne, Mathéo Faure

import pygame
from  random import randint, shuffle
import json

class Quiz:
    def __init__(self):
        with open(f"tableau.json", "r+") as f:
            self.data = json.load(f)
            f.close()

        self.objetif = None
        self.nb = randint(1, 10)
        self.q_nb = randint(1, 3)
        self.q = {2: "Qui est l'auteur?", 3:"Quelle est la date ?", 1:"Quelle est le titre ?"}

        self.bonne_reponse = [self.data[str(self.nb)][self.q_nb]]
        mauvaise_r_nb = []
        while len(mauvaise_r_nb) < 4:
            x = randint(1, 10)
            if x not in mauvaise_r_nb : mauvaise_r_nb.append(x)
        self.mauvaise_r = [self.data[str(nb)][self.q_nb] for nb in mauvaise_r_nb]
        self.reponses = self.bonne_reponse + self.mauvaise_r

        self.img = pygame.image.load(f"img/tableau/{self.nb}.webp")
        self.font = pygame.font.Font(None, 14)
        self.font_2 = pygame.font.Font(None, 28)
        self.copyr = self.font.render(self.data[str(self.nb)][0], False, (0, 0, 0))
        self.question = self.font_2.render(self.q[self.q_nb], False, (0, 0, 0))

        shuffle(self.reponses)
        self.good =self.reponses.index(self.bonne_reponse[0])
        self.r_1 = self.font_2.render(self.reponses[0], False, (0, 0, 0))
        self.r_2 = self.font_2.render(self.reponses[1], False, (0, 0, 0))
        self.r_3 = self.font_2.render(self.reponses[2], False, (0, 0, 0))
        self.r_4 = self.font_2.render(self.reponses[3], False, (0, 0, 0))

        self.rect_1 = pygame.Rect(100, 415, self.r_1.get_width(), 19)
        self.rect_2 = pygame.Rect(400, 415, self.r_1.get_width(), 19)
        self.rect_3 = pygame.Rect(100, 500, self.r_1.get_width(), 19)
        self.rect_4 = pygame.Rect(400, 500, self.r_1.get_width(), 19)
        self.rects = {1:self.rect_1, 2:self.rect_2, 3:self.rect_3, 4:self.rect_4}
        self.rect_afficher = [(0, 0, 0, 0), (0, 0, 0, 0)]

    def draw(self, screen):
        screen.fill((255, 255, 255))
        x = (800-self.img.get_width())//2
        y = self.img.get_height()
        screen.blit(self.copyr, (x, 10 + self.img.get_height()))
        screen.blit(self.question, ((800-self.question.get_width())//2, 10+self.img.get_height() + self.copyr.get_height()))
        screen.blit(self.r_1, (100, 415))
        screen.blit(self.r_2, (400, 415))
        screen.blit(self.r_3, (100, 500))
        screen.blit(self.r_4, (400, 500))
        screen.blit(self.img, (x, 10))

        if self.rect_afficher != [(0, 0, 0, 0), (0, 0, 0, 0)]:
            print("ok")
            pygame.draw.rect(screen, (255, 0, 0), self.rect_afficher[0], 2)
            pygame.draw.rect(screen, (255, 0, 0), self.rect_afficher[1], 2)
            pygame.display.flip()
            pygame.time.wait(1000)
            #self.change()

    def keypressed(self, event):
        if event.key == pygame.K_z:
            self.change()

    def change(self):
        self.nb = randint(1, 10)
        self.q_nb = randint(1, 3)
        self.q = {2: "Qui est l'auteur?", 3:"Quelle est la date ?", 1:"Quelle est le titre ?"}

        self.bonne_reponse = [self.data[str(self.nb)][self.q_nb]]
        mauvaise_r_nb = []
        while len(mauvaise_r_nb) < 4:
            x = randint(1, 10)
            if x not in mauvaise_r_nb : mauvaise_r_nb.append(x)
        self.mauvaise_r = [self.data[str(nb)][self.q_nb] for nb in mauvaise_r_nb]
        self.reponses = self.bonne_reponse + self.mauvaise_r

        self.img = pygame.image.load(f"img/tableau/{self.nb}.webp")
        self.font = pygame.font.Font(None, 14)
        self.font_2 = pygame.font.Font(None, 28)
        self.copyr = self.font.render(self.data[str(self.nb)][0], False, (0, 0, 0))
        self.question = self.font_2.render(self.q[self.q_nb], False, (0, 0, 0))

        shuffle(self.reponses)
        self.good =self.reponses.index(self.bonne_reponse[0])
        self.r_1 = self.font_2.render(self.reponses[0], False, (0, 0, 0))
        self.r_2 = self.font_2.render(self.reponses[1], False, (0, 0, 0))
        self.r_3 = self.font_2.render(self.reponses[2], False, (0, 0, 0))
        self.r_4 = self.font_2.render(self.reponses[3], False, (0, 0, 0))

        self.rect_1 = pygame.Rect(100, 415, self.r_1.get_width(), 19)
        self.rect_2 = pygame.Rect(400, 415, self.r_1.get_width(), 19)
        self.rect_3 = pygame.Rect(100, 500, self.r_1.get_width(), 19)
        self.rect_4 = pygame.Rect(400, 500, self.r_1.get_width(), 19)
        self.rects = {1: self.rect_1, 2: self.rect_2, 3: self.rect_3, 4: self.rect_4}
        self.rect_afficher = [(0, 0, 0, 0), (0, 0, 0, 0)]

    def __str__(self):
        return "Quiz"

    def choice(self, nb):
        if nb == self.good:
            self.rect_afficher = [self.rects[self.good], self.rects[nb]]
            print("OUI")
        else:
            self.rect_afficher = [(0, 0, 0, 0), self.rects[nb]]

    def update(self):
        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            if self.rect_1.collidepoint(x, y): self.choice(1)
            if self.rect_2.collidepoint(x, y): self.choice(2)
            if self.rect_3.collidepoint(x, y): self.choice(3)
            if self.rect_4.collidepoint(x, y): self.choice(4)
