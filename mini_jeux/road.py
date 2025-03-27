#Projet : Art'Venture
#Auteurs : Anthony Ibanez-Esteban, Raphaël Prost, Aëlys-Coleen Surma Valtaer, Louis Gagne, Mathéo Faure

from random import randint

import pygame

from carte import Carte
from enemy import Enemy


class Car(Enemy):
    """
    Classe représentant une voiture ennemie dans le jeu.
    Hérite de la classe Enemy et ajoute des propriétés spécifiques à la voiture, comme sa vitesse et son toit.
    Gere les collisions pixel par pixel
    """
    def __init__(self, src, x, y, image_toit, speed=2):
        """
        Initialise une nouvelle voiture avec une position (x, y), une image de base et une image de toit.

        Args:
        - src (str): Le chemin de l'image de la voiture (vue de côté).
        - x (int): La coordonnée x de la voiture.
        - y (int): La coordonnée y de la voiture.
        - image_toit (pygame.Surface): L'image représentant le toit de la voiture.
        - speed (int): La vitesse de déplacement de la voiture (par défaut 2).
        """
        super().__init__(src, x, y) #src = image bas voiture
        self.speed = speed
        self.toit = image_toit #src = image du tois (hors hit box)


class Road(Carte):
    """
    Classe représentant la route dans le jeu.
    Hérite de la classe Carte et gère les voitures ennemies, leur apparition, et la logique du jeu sur la route.
    """
    def __init__(self):
        """
        Initialise une nouvelle instance de la route, charge l'image de la feuille de voiture et initialise les voitures ennemies.
        Définit également la difficulté et l'objectif du jeu.
        """
        super().__init__(self.get_url("map/road.tmx"))
        self.tp_1 = self.objet_par_nom('tp_1')

        self.image_sheet = pygame.image.load(self.get_url("img/car_sheet.png"))
        self.images = {1:self._cut_img_bas(0, 6), 4:self._cut_img_bas(37, 6),
                       2:self._cut_img_bas(0, 31), 5:self._cut_img_bas(37, 31),
                       3:self._cut_img_bas(0, 56), 6:self._cut_img_bas(37, 56),}

        self.images_toits = {1: self._cut_img_haut(0, 0), 4: self._cut_img_haut(37, 0),
                       2: self._cut_img_haut(0, 25), 5: self._cut_img_haut(37, 25),
                       3: self._cut_img_haut(0, 50), 6: self._cut_img_haut(37, 50), }

        self.cars = []
        self.spawn_car()
        self.difficulty = 25
        self.counter = self.difficulty
        self.spawn = self.objet_par_nom("spawn").midbottom
        self.player.speed = 1.5
        self.a = pygame.transform.scale(self.image_sheet, (10, 10))

    def _cut_img_bas(self, x, y):
        """
        Découpe une section de l'image de la feuille de voiture pour obtenir l'image de la voiture vue de côté.

        Args:
        - x (int): La position x de la section à découper.
        - y (int): La position y de la section à découper.

        Returns:
        - pygame.Surface: L'image découpée et redimensionnée de la voiture vue de côté.
        """
        image = pygame.Surface([36, 19])
        image.blit(self.image_sheet, (0, 0), (x, y, 36, 25))
        image = pygame.transform.scale(image, (36*1.2,19*1.2))
        image.set_colorkey((0, 0, 0))
        return image

    def _cut_img_haut(self, x, y):
        """
        Découpe une section de l'image de la feuille de voiture pour obtenir l'image du toit de la voiture.

        Args:
        - x (int): La position x de la section à découper.
        - y (int): La position y de la section à découper.

        Returns:
        - pygame.Surface: L'image découpée et redimensionnée du toit de la voiture.
        """
        image = pygame.Surface([35, 5])
        image.blit(self.image_sheet, (0, 0), (x, y, 35, 5))
        image = pygame.transform.scale(image, (35*1.2*2,5*1.2*2))
        image.set_colorkey((0, 0, 0))
        return image

    def add_verif(self):
        """
        Vérifie si une nouvelle voiture doit apparaître et gère les collisions avec les voitures existantes.
        Si une collision est détectée, le jeu se termine.
        """
        if self.counter <= 0:
            self.counter = self.difficulty
            self.spawn_car()
        self.counter -= 1

        if self.multi_collision(self.cars):
            self.game_over()


    def add_draw(self, screen):
        """
        Dessine les éléments de la route et des voitures sur l'écran.
        - Dessine les voitures, leurs toits et les déplacements.
        - Supprime les voitures qui sortent de l'écran.
        - Gère l'objectif du joueur (atteindre la ville).

        Args:
        - screen (pygame.Surface): L'écran sur lequel dessiner les éléments.
        """
        screen.blit(self.a , (0, 0))
        for car in self.cars:
            car.avancer()
            screen.blit(car.toit, self.fixe_coord((car.rect.x, car.rect.y - 5)))
            if car.coord[0] > 600 or car.coord[0] < -100:
                self.cars.remove(car)
                car.kill()

            if self.player.coord[1] < 50:
                self.objetif = "Museum_hall"


    def spawn_car(self):
        """
        Fait apparaître de nouvelles voitures ennemies à des positions aléatoires sur la route.
        Chaque voiture a une position, une image et une vitesse différentes.
        """
        route = randint(0, 1)
        x = randint(4, 6)
        car = Car(self.images[x], -100, 101 + route*128, self.images_toits[x], 5-route)
        self.groupe.add(car)
        self.cars.append(car)
        route = randint(2, 3)
        x = randint(4, 6)
        car = Car(self.images[x], -100, 101 + route * 128, self.images_toits[x], 5-route)
        self.groupe.add(car)
        self.cars.append(car)
        route = randint(0, 1)
        x = randint(1, 3)
        car = Car(self.images[x], 600, 165 + route*128, self.images_toits[x], 5-route)
        car.regarder(180)
        self.groupe.add(car)
        self.cars.append(car)
        route = randint(2, 3)
        x = randint(1, 3)
        car = Car(self.images[x], 600, 165 + route * 128, self.images_toits[x], 5-route)
        car.regarder(180)
        self.groupe.add(car)
        self.cars.append(car)

    def game_over(self):
        self.death_animation()
        self.tp(self.spawn[0], self.spawn[1])

    def __str__(self):
        return "Road"

