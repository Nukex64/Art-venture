import math
import pygame
from carte import Carte
from tuto import Tuto


class Tresor(Carte):
    """
    Classe représentant la carte des trésors dans le jeu.
    Gère l'apparition des trésors et la logique du radar pour localiser les trésors.
    """

    def __init__(self):
        """
        Initialise une instance de la carte des trésors.
        Charge la carte associée, le tutoriel, la liste des trésors et l'initialisation du radar.
        """
        super().__init__(self.get_url("map/maptresortest.tmx"))  # Charge la carte
        self.tuto = Tuto()  # Initialise le tutoriel
        self.tresors = self.points_par_classe("tresor")  # Récupère les points de trésor
        self.son01 = pygame.mixer.Sound(self.get_url("sounds/bip.mp3"))  # Son pour le bip du radar
        self.frame = 0  # Compteur de frame
        self.lastbip = 1  # Dernière frame du bip
        self.bip = 1  # Frame actuelle du bip

        self.radar = Radar()  # Initialise le radar
        self.groupe.add(self.radar)  # Ajoute le radar au groupe de sprites

    def add_draw(self, screen):
        """
        Méthode pour dessiner les éléments à l'écran.
        Affiche le radar et gère la localisation des trésors.

        Args:
        - screen (pygame.Surface): L'écran où les éléments sont dessinés.
        """
        if self.tresors:
            self.getraytresor(screen)  # Affiche la ligne du radar vers le trésor
            self.trouver_tresor()  # Vérifie si un trésor est trouvé

    def add_verif(self):
        """
        Vérifie les actions du joueur à chaque frame.
        Si la touche "RETURN" est pressée, ouvre un tutoriel.
        """
        self.frame += 1
        self.radar.set_middle(self.player.middle)  # Met à jour la position du radar
        if self.touche("RETURN"):
            self.tuto.open("Sed quid est quod in hac causa...", "img/fire.png")

    def ray(self, screen, coord, ray=True):
        """
        Trace une ligne (rayon) entre le joueur et le trésor.

        Args:
        - screen (pygame.Surface): L'écran où dessiner la ligne.
        - coord (tuple): Les coordonnées du trésor.
        - ray (bool): Si True, la ligne est dessinée.

        Returns:
        - float: La distance entre le joueur et le trésor.
        """
        x2, y2 = self.fixe_coord(coord)
        x1, y1 = self.fixe_coord(self.player.rect.center)
        vx, vy = x2 - x1, y2 - y1
        norm = math.sqrt(vx ** 2 + vy ** 2)
        vx, vy = vx / (norm + 0.0001), vy / (norm + 0.0001)
        if norm < 75:
            x, y = x2, y2
        else:
            x, y = x1 + vx * 75, y1 + vy * 75
        if ray:
            pygame.draw.line(screen, 'red', (x1, y1), (x, y), 1)
        return norm
    def __str__(self):
        return "Tresor"
    def getraytresor(self, screen):
        """
        Cherche le trésor le plus proche en mesurant les distances avec le radar.
        Joue un bip lorsque le radar détecte un trésor à proximité.

        Args:
        - screen (pygame.Surface): L'écran où dessiner les éléments du radar.
        """
        liste = []
        self.coord = (0, 0)
        pluspetit = 8000
        for tresor in self.tresors:
            distance = self.ray(screen, tresor, False)
            liste.append(distance)
            if distance < pluspetit:
                pluspetit = distance
                self.coord = tresor
        min_dist = round(min(liste)) + 5
        self.min_dist = min_dist - 5
        if self.bip == self.frame or min_dist < self.bip - self.lastbip - min_dist + 10:
            pygame.mixer.Sound.play(self.son01)  # Joue le bip
            self.bip = self.frame
            self.bip, self.lastbip = self.bip + min_dist, self.bip
            x = min(255, max(0, pluspetit))
            self.radar.green = x  # Change la couleur du radar
            self.radar.create()  # Met à jour le radar

        self.ray(screen, self.coord)  # Dessine la ligne vers le trésor

    def trouver_tresor(self):
        """
        Vérifie si le trésor a été trouvé (si la distance est inférieure à 5).
        Si trouvé, supprime le trésor de la liste.
        """
        if self.min_dist < 5:
            self.tresors.remove(self.coord)  # Supprime le trésor trouvé


class Radar(pygame.sprite.Sprite):
    """
    Classe représentant le radar qui affiche la proximité des trésors.
    Il dessine des cercles autour du joueur en fonction de la distance aux trésors.
    """

    def __init__(self):
        """
        Initialise le radar avec une image vide, un rectangle pour la position et une couleur de radar initiale.
        """
        super().__init__()
        self.image = pygame.Surface([50, 50], pygame.SRCALPHA)
        self.image.set_colorkey((0, 0, 0))  # Rendre l'arrière-plan transparent
        self.rect = self.image.get_rect()
        self.coord = [100, 100]  # Position initiale du radar
        self.green = 0  # Initialisation de la couleur du radar
        self.liste_radar = [0]  # Liste de tailles de cercles pour l'animation

    def update(self):
        """
        Met à jour l'image du radar, dessine les cercles représentant la distance aux trésors.
        """
        self.rect.topleft = self.coord
        self.image.fill((0, 0, 0))  # Efface l'ancienne image
        N = len(self.liste_radar)
        for i in range(N - 1, -1, -1):
            circle = self.liste_radar[i]
            if circle < 25:
                pygame.draw.circle(self.image, (255 - self.green, self.green, 0, 250 - circle * 9), (25, 25), circle, 3)
                self.liste_radar[i] += 0.5
            else:
                del self.liste_radar[i]

    def set_middle(self, coord):
        """
        Définit la position du centre du radar (le centre du joueur).

        Args:
        - coord (tuple): Les coordonnées du joueur.
        """
        x, y = coord
        self.coord = (x - 25, y - 25)  # Positionne le radar autour du joueur

    def create(self):
        """
        Crée un nouveau cercle dans la liste du radar pour l'animation.
        """
        self.liste_radar.append(0)
