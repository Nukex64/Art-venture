
import pygame

from mini_jeux.piano_tiles_gurenge import tiles
from savefonction import sauvegarde


class Piano:
    def __init__(self):
        self.hg = 200
        self.saveload = sauvegarde()
        self.dico = tiles
        self.multiplicateur = 1
        self.point = 0
        self.font = pygame.font.Font("img/police.otf", 30)
        self.frame = 0
        self.liste = [[],[],[],[]]
        self.img = [pygame.image.load("img/fire.png"),pygame.image.load("img/fire.png"),pygame.image.load("img/fire.png"),pygame.image.load("img/fire.png")]
        largeurimage = self.img[0].get_rect()[3]/2
        self.hauteurimage = self.img[0].get_rect()[2]
        self.hauteurtrait = 10
        self.xcolone = [self.hg+125-largeurimage,self.hg+225-largeurimage,self.hg+325-largeurimage,self.hg+425-largeurimage]

    def draw(self, screen):
        pygame.draw.rect(screen,(255,255,255),(self.hg-100,0,175,600))
        pygame.draw.rect(screen, (0, 255, 255), (self.hg+75, 0, 100, 600))
        pygame.draw.rect(screen, (255, 0, 255), (self.hg+175, 0, 100, 600))
        pygame.draw.rect(screen, (255, 255, 0), (self.hg+275, 0, 100, 600))
        pygame.draw.rect(screen, (255, 100, 0), (self.hg+375, 0, 100, 600))
        pygame.draw.line(screen, (0,0,0),(self.hg+75,525),(800,525),self.hauteurtrait)
        texte_render = self.font.render(str(round(self.point)), True, (0, 0, 0))
        texte_render2 = self.font.render("Points", True, (0, 0, 0))
        screen.blit(texte_render, (120,100))
        screen.blit(texte_render2, (120, 70))

        for i in range(len(self.liste)):
            for j in self.liste[i]:
                screen.blit(self.img[i],(self.xcolone[i],j))
                if j>600 :
                    self.multiplicateur = 1
                    self.liste[i].remove(j)




    def apparaitre(self):
        print(self.frame)
        if self.frame / 60 in self.dico:
            for elt in self.dico[self.frame/60]:
                self.liste[elt].append(0)
            print(self.liste)
        pass


    def deplacement(self):
        for liste in self.liste:
            for y in range(len(liste)):
                liste[y] += 2

        pass

    def update(self):
        self.frame+=1
        self.apparaitre()
        self.deplacement()


    def keypressed(self,event):
        if event.key == pygame.K_d:
            self.click(0)
        if event.key == pygame.K_f:
            self.click(1)
        if event.key == pygame.K_j:
            self.click(2)
        if event.key == pygame.K_k:
            self.click(3)

    def click(self,key):
        for y in self.liste[key]:
            if abs(525-y)<= self.hauteurimage+self.hauteurtrait/2 :
                self.liste[key].remove(y)
                self.point += 100*self.multiplicateur
                self.multiplicateur+=0.2
            else:
                self.multiplicateur = 1