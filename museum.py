import pygame
from carte import Carte
from savefonction import sauvegarde
from mini_jeux.quiz import Quiz

class Museum_haut(Carte):
    def __init__(self, nb_save):
        super().__init__("map/museum/musée_couloir_1.tmx")
        self.save = sauvegarde(nb_save)
        self.dico_tableau = {}
        self.dico_rect = {}
        self.quiz = Quiz()

        for obj in self.tmx_data.objects:
            if obj.type == "paint":
                img = pygame.image.load(f"img/tableau/{obj.name}.webp")
                x = img.get_width() / img.get_width()
                img = pygame.transform.smoothscale(img, (60, 60 * x))
                self.dico_tableau[obj.name] = ((obj.x, obj.y), img)
                self.dico_rect[(obj.x, obj.y, img.get_width(), img.get_height())] = obj.name
        self.porte = self.objet_par_nom("porte")

    def add_draw(self, screen):
        for name, info in self.dico_tableau.items():
            coord, img = info
            screen.blit(img, self.fixe_coord(coord))

        if self.touche("e"):
            x = self.player.rect.collidedict(self.dico_rect)[1]
            if x:
                quiz = self.quiz.open(x)
                if quiz : self.save.liste_changer_json("tableau_quiz", 1, quiz)
                
    def keypressed(self,event):
        super().keypressed(event)
        if event.key == pygame.K_RETURN:
            if self.player.rect.colliderect(self.porte):
                self.tuto_e()
                self.objetif = "Museum_hall"

    def __str__(self):
        return "Museum_haut"

#-----------------------------------------------------------------------------------------------------
class Museum_hall(Carte):
    def __init__(self, nb_save):
        super().__init__("map/museum/musée_hall.tmx")
        self.save = sauvegarde(nb_save)
        self.porte_haut = self.objet_par_nom("porte_haut")
        self.porte_bas = self.objet_par_nom("porte_bas")
        self.quiz = Quiz()

    def keypressed(self,event):
        super().keypressed(event)
        if event.key == pygame.K_RETURN:
            if self.player.rect.colliderect(self.porte_haut):
                self.objetif = "Museum_haut"
            if self.player.rect.colliderect(self.porte_bas):
                self.objetif = "Museum_bas"

    def __str__(self):
        return "Museum_hall"

#-----------------------------------------------------------------------------------------------------
class Museum_bas(Carte):
    def __init__(self, nb_save):
        super().__init__("map/museum/musée_couloir_2.tmx")
        self.save = sauvegarde(nb_save)
        self.dico_tableau = {}
        self.dico_rect = {}
        for obj in self.tmx_data.objects:
            if obj.type == "paint":
                img = pygame.image.load(f"img/tableau/{obj.name}.webp")
                x = img.get_width() / img.get_width()
                img = pygame.transform.smoothscale(img, (60, 60 * x))
                self.dico_tableau[obj.name] = ((obj.x, obj.y), img)
                self.dico_rect[(obj.x, obj.y, img.get_width(), img.get_height())] = obj.name
        self.porte = self.objet_par_nom("porte")
        self.quiz = Quiz()

    def add_draw(self, screen):
        for name, info in self.dico_tableau.items():
            coord, img = info
            screen.blit(img, self.fixe_coord(coord))

        if self.touche("e"):
            x = self.player.rect.collidedict(self.dico_rect)[1]
            if x:
                quiz = self.quiz.open(x)


    def keypressed(self,event):
        super().keypressed(event)
        if event.key == pygame.K_RETURN:
            if self.player.rect.colliderect(self.porte):
                self.objetif = "Museum_hall"

    def __str__(self):
        return "Museum_bas"