import pygame
from carte import Carte
from savefonction import sauvegarde
from mini_jeux.quiz import Quiz
# SI VOUS ETES BLOQUER TOUCHE 0 DU PAD
class Museum_haut(Carte):
    """
    Classe représentant la carte du "Musée - Haut". Cette carte contient des tableaux que le joueur peut observer,
    ainsi qu'un quiz associé à chaque tableau. Elle permet également de se déplacer entre différentes zones du musée.

    Hérite de la classe `Carte`.
    """
    def __init__(self, nb_save):
        """
        Initialise la carte du musée haut, charge les objets de type "paint" (tableaux) et les associe à une image,
        les coordonnées et un rectangle pour la détection des collisions. Charge également la porte permettant d'accéder à une autre zone.

        Args:
            nb_save (int): Le numéro de la sauvegarde à charger.
        """
        super().__init__(self.get_url("map/museum/musée_couloir_1.tmx"))
        self.save = sauvegarde(nb_save)
        self.dico_tableau = {}
        self.dico_rect = {}
        self.quiz = Quiz()
        self.game_5 = self.objet_par_nom("game_5")
        self.game_6 = self.objet_par_nom("game_6")
        self.game_7 = self.objet_par_nom("game_7")
        for obj in self.tmx_data.objects:
            if obj.type == "paint":
                img = pygame.image.load(self.get_url(f"img/tableau/{obj.name}.webp"))
                x = img.get_height() / img.get_width()
                img = pygame.transform.smoothscale(img, (60, int(60 * x)))
                self.dico_tableau[obj.name] = ((obj.x, obj.y), img)
                self.dico_rect[(obj.x, obj.y, img.get_width(), img.get_height())] = obj.name
        self.porte = self.objet_par_nom("porte")

    def add_draw(self, screen):
        """
        Affiche les tableaux dans la zone du musée haut et gère les collisions avec le joueur. Si le joueur entre en collision
        avec un tableau, un quiz s'affiche. Si le joueur entre en collision avec la porte, un objectif de déplacement est activé.

        Args:
            screen (pygame.Surface): L'écran sur lequel dessiner les éléments de la carte.
        """

        for name, info in self.dico_tableau.items():
            coord, img = info
            screen.blit(img, self.fixe_coord(coord))



        x = self.player.rect.collidedict(self.dico_rect)
        if x:
            self.affe(screen)
            if self.touche("e"):
                quiz = self.quiz.open(x[1])
                print(quiz)
                if quiz > 0: self.save.liste_changer_json("tableau_quiz", int(x[1]), quiz)

        if self.player.rect.colliderect(self.porte):
            self.affe(screen)

    def keypressed(self,event):
        super().keypressed(event)
        if event.key == pygame.K_e:
            if self.player.rect.colliderect(self.porte):
                self.objetif = "Museum_hall"

            if self.player.rect.colliderect(self.game_5):
                self.objetif = "Tresor"
            if self.player.rect.colliderect(self.game_6):
                self.objetif = "swim"
            if self.player.rect.colliderect(self.game_7):
                self.objetif = "piano"

    def __str__(self):
        return "Museum_haut"

#-----------------------------------------------------------------------------------------------------
class Museum_hall(Carte):
    def __init__(self, nb_save):
        super().__init__(self.get_url("map/museum/musée_hall.tmx"))
        self.save = sauvegarde(nb_save)
        self.porte_haut = self.objet_par_nom("porte_haut")
        self.porte_bas = self.objet_par_nom("porte_bas")
        self.game_3 = self.objet_par_nom("game_3")
        self.game_4 = self.objet_par_nom("game_4")
        self.quiz = Quiz()

    def add_draw(self, screen):
        if self.player.rect.colliderect(self.porte_haut) or self.player.rect.colliderect(self.porte_bas) :
            self.affe(screen)

    def keypressed(self,event):
        super().keypressed(event)
        if event.key == pygame.K_e:
            if self.player.rect.colliderect(self.porte_haut):
                self.objetif = "Museum_haut"
            if self.player.rect.colliderect(self.porte_bas):
                self.objetif = "Museum_bas"

            if self.player.rect.colliderect(self.game_3):
                self.objetif = "Road"
            if self.player.rect.colliderect(self.game_4):
                self.objetif = "Undertale"

    def __str__(self):
        return "Museum_hall"

#-----------------------------------------------------------------------------------------------------
class Museum_bas(Carte):
    def __init__(self, nb_save):
        super().__init__(self.get_url("map/museum/musée_couloir_2.tmx"))
        self.save = sauvegarde(nb_save)
        self.dico_tableau = {}
        self.dico_rect = {}
        self.parcoure = self.objet_par_nom("game_1")
        self.laby = self.objet_par_nom("game_2")

        for obj in self.tmx_data.objects:
            if obj.type == "paint":
                img = pygame.image.load(self.get_url(f"img/tableau/{obj.name}.webp"))
                x = img.get_height() / img.get_width()
                img = pygame.transform.smoothscale(img, (60, int(60 * x)))
                self.dico_tableau[obj.name] = ((obj.x, obj.y), img)
                self.dico_rect[(obj.x, obj.y, img.get_width(), img.get_height())] = obj.name
        self.porte = self.objet_par_nom("porte")
        self.quiz = Quiz()

    def add_draw(self, screen):
        for name, info in self.dico_tableau.items():
            coord, img = info
            screen.blit(img, self.fixe_coord(coord))


        x = self.player.rect.collidedict(self.dico_rect)
        if x:
            self.affe(screen)
            if self.touche("e"):
                quiz = self.quiz.open(x[1])
                print(quiz)
                if quiz > 0: self.save.liste_changer_json("tableau_quiz", int(x[1]), quiz)

        if self.player.rect.colliderect(self.porte):
            self.affe(screen)

    def keypressed(self,event):
        super().keypressed(event)
        if event.key == pygame.K_e:
            if self.player.rect.colliderect(self.porte):
                self.objetif = "Museum_hall"

            if self.player.rect.colliderect(self.parcoure):
                self.objetif = "Parcours"

            if self.player.rect.colliderect(self.laby):
                self.objetif = "Laby"


    def __str__(self):
        return "Museum_bas"