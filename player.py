import os

import pygame

class Player(pygame.sprite.Sprite):
    """
    Classe représentant le joueur dans le jeu.

    Hérite de `pygame.sprite.Sprite`.

    Fonctionnalités disponibles :
    - Déplacement du joueur (haut, bas, gauche, droite).
    - Mise à jour des hitbox du joueur (pied et corps).
    - Changement de direction du regard du joueur.
    - Test de déplacement en fonction des collisions avec les murs.
    """
    def __init__(self, x, y):
        """
        Initialise le joueur avec sa position et ses images de sprite.

        Args:
            x (int): Position X initiale du joueur.
            y (int): Position Y initiale du joueur.
        """
        super().__init__()
        self.image_sheet = pygame.image.load(self.get_url('img/player_sheet.png')).convert_alpha()  # Récupère l'image
        self.images = {"haut": self._cut_img(4, 16),  # Découpe les images des différentes directions
                       "droite": self._cut_img(4, 48),
                       "bas": self._cut_img(4, 80),
                       "gauche": self._cut_img(4, 112)}

        self.image = self.images['bas']  # Image initiale (joueur regardant vers le bas)

        self.rect = self.image.get_rect()  # Définit l'hitbox / le rectangle du joueur
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.4, 10)  # Hitbox des pieds
        self.under_feet = pygame.Rect(0, 0, self.rect.width * 0.4, 10)  # Sous-pieds pour les collisions
        self.mask = pygame.mask.from_surface(self.image.subsurface(self.feet))
        self.coord = [x, y]  # Position initiale du joueur

        self.vx = 0  # Déplacement en X (initialement 0)
        self.vy = 0  # Déplacement en Y (initialement 0)
        self.speed = 3  # Vitesse de déplacement du joueur

    @staticmethod
    def get_url(url):
        url_list = url.split("/")
        return os.path.join(*url_list)

    def update(self):
        """
        Met à jour la position du joueur et les hitbox.

        Ne pas renommer la méthode `_update` pour que `self.groupe._update()` fonctionne.
        """
        self.rect.topleft = self.coord
        self.feet.midbottom = self.rect.midbottom  # Place les pieds du joueur au bas du rectangle
        self.under_feet.midtop = self.feet.midbottom  # Place le sous-pied sous les pieds

    def _cut_img(self, x, y):
        """
        Découpe l'image du joueur dans le sprite sheet à l'emplacement donné.

        Args:
            x (int): Coordonnée X de l'image à découper.
            y (int): Coordonnée Y de l'image à découper.

        Returns:
            pygame.Surface: L'image découpée à la position spécifiée.
        """
        image = pygame.Surface([16, 16], pygame.SRCALPHA)
        image.blit(self.image_sheet, (0, 0), (x, y, 16, 16))
        return image

    def regarder(self, direction):
        """
        Change la direction dans laquelle le joueur regarde.

        Args:
            direction (str): Direction vers laquelle le joueur regarde.
                             Options possibles : 'haut', 'droite', 'bas', 'gauche'.
        """
        self.image = self.images[direction]  # Modifie l'image en fonction de la direction

    def haut(self, x=1):
        """
        Déplace le joueur vers le haut.

        Args:
            x (int): Multiplicateur pour la distance de déplacement (par défaut 1).
        """
        self.vy -= self.speed * x

    def bas(self, x=1):
        """
        Déplace le joueur vers le bas.

        Args:
            x (int): Multiplicateur pour la distance de déplacement (par défaut 1).
        """
        self.vy += self.speed * x

    def gauche(self, x=1):
        """
        Déplace le joueur vers la gauche.

        Args:
            x (int): Multiplicateur pour la distance de déplacement (par défaut 1).
        """
        self.vx -= self.speed * x

    def droite(self, x=1):
        """
        Déplace le joueur vers la droite.

        Args:
            x (int): Multiplicateur pour la distance de déplacement (par défaut 1).
        """
        self.vx += self.speed * x

    def test_deplacement(self, mur):
        """
        Teste si le joueur peut se déplacer sans toucher les murs.

        Args:
            mur (list): Liste des hitbox des murs contre lesquels le joueur ne doit pas se déplacer.

        Déplace le joueur si possible, sinon il reste immobile. Les déplacements sont testés sur les axes X et Y séparément.
        """
        if not self.feet.move(self.vx, 0).collidelist(mur) > -1:
            self.coord[0] += self.vx
        if not self.feet.move(0, self.vy).collidelist(mur) > -1:
            self.coord[1] += self.vy
        self.vx, self.vy = 0, 0

    @property
    def coord_int(self):
        """
        Retourne les coordonnées du joueur sous forme d'entiers.

        Returns:
            tuple: Coordonnées (X, Y) du joueur.
        """
        return int(self.coord[0]), int(self.coord[1])

    @property
    def middle(self):
        """
        Retourne la position centrale du joueur.

        Returns:
            tuple: Position centrale du joueur (X+8, Y+8) pour le centre du rectangle du joueur.
        """
        return self.coord[0] + 8, self.coord[1] + 8

    def get_image_transparent(self, x):
        """
        Applique une transparence à l'image du joueur.

        Args:
            x (int): Niveau de transparence, entre 0 (opaque) et 255 (complètement transparent).

        Returns:
            pygame.Surface: L'image avec la transparence appliquée.
        """
        image = self.image.copy()
        image.fill((0, 255, 0), special_flags=pygame.BLEND_RGB_ADD)  # Ajoute une couleur verte (non visible)
        image.set_alpha(x)  # Applique la transparence
        return pygame.transform.scale(image, (32, 32))

    def transparent(self, color=0):
        """
        Modifie la transparence de l'image du joueur.

        Args:
            color (float): Valeur de transparence entre 0 (opaque) et 1 (complètement transparent).
        """
        self.image = self.get_image_transparent(255 * color)
