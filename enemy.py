import pygame

class Enemy(pygame.sprite.Sprite):
    """
    Joueur pygame

    Fonction utilisable:
    haut()/bas()/gauche()/haut(): bouge le joueur, multiplicateur en paramètre (haut(5): 5 fois haut)
    _update(): met à jour les hitbox du joueur (pied et corps)
    regarder(d): fait regarder le joueur --> d : 'haut'/'droite'/'bas'/'gauche'
    test_deplacement(mur) : bouge le joueur s'il peut --> mur : liste des murs à ne pas toucher

    """
    def __init__(self, src, x, y):
        super().__init__()
        self.image= pygame.image.load(src)
        self.image.set_colorkey([0, 0, 0])  # retire le fond noire au spawn du joueur

        self.rect = self.image.get_rect() # definit l'hitbox / le rectangle du joueur
        self.coord = [x, y]
        self.speed = 3

    def update(self):
        """
        Pose le haut gauche du joueur et ses pied où il faut
        Ne pas renommer la methode _update pour que self.groupe._update() fonctionne
        """
        self.rect.topleft = self.coord

    def regarder(self, angle):
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect()

    # x est un multiplieur si on ne met rien c'est *1
    def haut(self, x=1):
        self.coord[1] -= self.speed * x
    def bas(self, x=1):
        self.coord[1] += self.speed * x
    def gauche(self, x=1):
        self.coord[0] -= self.speed * x
    def droite(self, x=1):
        self.coord[0] += self.speed * x
