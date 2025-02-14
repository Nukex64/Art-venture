import pygame

class Player(pygame.sprite.Sprite):
    """
    Joueur pygame

    Fonction utilisable:
    haut()/bas()/gauche()/haut(): bouge le joueur, multiplicateur en paramètre (haut(5): 5 fois haut)
    _update(): met à jour les hitbox du joueur (pied et corps)
    regarder(d): fait regarder le joueur --> d : 'haut'/'droite'/'bas'/'gauche'
    test_deplacement(mur) : bouge le joueur s'il peut --> mur : liste des murs à ne pas toucher

    """
    def __init__(self, x, y):
        super().__init__()
        self.image_sheet = pygame.image.load('img/player_sheet.png') # recupere les images
        self.images = {"haut":self._cut_img(4, 16),  # recupere les quatres images
                       "droite":self._cut_img(4, 48),
                       "bas":self._cut_img(4, 80),
                       "gauche": self._cut_img(4, 112)}

        self.image = self.images['bas']  # recupere l'image du joueur regardant vers le bas

        self.image.set_colorkey([0, 0, 0])  # retire le fond noire au spawn du joueur

        self.rect = self.image.get_rect() # definit l'hitbox / le rectangle du joueur
        self.feet = pygame.Rect(0, 0, self.rect.width*0.4, 10) # definit l'hitbox des jambes du joueurs pour les collisions (on peut changer la taille si il faut)
        self.mask = pygame.mask.from_surface(self.image.subsurface(self.feet))
        self.coord = [x, y]

        self.vx = 0 # changer de coord x a la prochaine frame
        self.vy = 0 # changer de coord y a la prochaine frame
        self.speed = 3

    def update(self):
        """
        Pose le haut gauche du joueur et ses pied où il faut
        Ne pas renommer la methode _update pour que self.groupe._update() fonctionne
        """
        self.rect.topleft = self.coord
        self.feet.midbottom = self.rect.midbottom # milieu pied = milieu bas joueur

    def _cut_img(self, x, y):
        """
        :x/y: int (coord)
        Decoupe l'image du joueur de taille 16x16 a l'emplacement (x,y)
        """
        image = pygame.Surface([16, 16])
        image.blit(self.image_sheet, (0, 0), (x, y, 16, 16))
        return image

    def regarder(self, direction):
        """
        Fait regarder le joueur
        :direction: 'haut'/'droite'/'bas'/'gauche'

        """
        self.image = self.images[direction] # change l'image pour regarder
        self.image.set_colorkey([0, 0, 0]) #retire le fond noir du joueur

    # x est un multiplieur si on ne met rien c'est *1
    def haut(self, x=1):
        self.vy -= self.speed * x
    def bas(self, x=1):
        self.vy += self.speed * x
    def gauche(self, x=1):
        self.vx -= self.speed * x
    def droite(self, x=1):
        self.vx += self.speed * x

    def test_deplacement(self, mur):
        """
        :mur: liste d'hitbox de mur

        Déplace le joueur s'il ne touche pas la liste des murs donnée en paramètre
        Le bouge de façon imaginaire et regarde s'il touche un mur
        (les 2 axes sont séparés pour que ça marche)
        """
        if not self.feet.move(self.vx, 0).collidelist(mur) > -1:
            self.coord[0] += self.vx
        if not self.feet.move(0, self.vy).collidelist(mur) > -1:
            self.coord[1] += self.vy
        self.vx, self.vy = 0, 0