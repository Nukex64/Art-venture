import pygame
import pytmx
import pyscroll
from player import Player
from settings import *

class Carte:
    """
     Classe générique pour gérer les cartes du jeu, y compris le musée et les mini-jeux.

    Cette classe fournit les fonctionnalités de base pour :
    - Charger une carte depuis un fichier `.tmx`.
    - Gérer les collisions avec des objets (murs, plateformes, etc.).
    - Déplacer un joueur sur la carte.
    - Afficher les éléments de la carte et des couches supplémentaires.

    Les mini-jeux hérite de cette classe
    Redéfinir certaines méthodes pour personnaliser la carte (ex. : mouvements, vérifications).

    """
    def __init__(self, map_file):
        """
        Args:
            map_file (str): Chemin vers le fichier `.tmx` de la carte.
        """
        self.tmx_data = pytmx.util_pygame.load_pygame(map_file)  # recupere les info de map.tmx
        map_data = pyscroll.TiledMapData(self.tmx_data)  # recupere les info des couches
        self.map_layer = pyscroll.orthographic.BufferedRenderer(map_data, RES)  # genere les couches d'images
        self.map_layer.zoom = ZOOM  # ZOOM de la carte
        player_pos = self.tmx_data.get_object_by_name('spawn') # coord du joueur sur l'objet spawn
        self.player = Player(player_pos.x, player_pos.y - 10)  # creer le joueur

        self.groupe = pyscroll.PyscrollGroup(map_layer=self.map_layer,
                                             default_layer=2)  # groupe de toutes les images pour pygame (default_layer = couche du joueur)
        self.groupe.add(self.player)  # rajoute le joueur au groupe d'images

        self.mur = []  # liste de mur (leur hitbox)
        calque_mur = self.tmx_data.get_layer_by_name('mur') #calque des murs
        for obj in calque_mur:
            self.mur.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height)) # ajoute toute les hitbox des murs

        self.run = True
        self.dialogue = None
        self.font = pygame.font.Font(None, 24)
        self.docenter = True

    def clavier(self):
        """
        Gère touches pressées.
        Redéfinir cette méthode pour changer les mouvements ou les comportements associés.
        """
        keys = pygame.key.get_pressed()  # Récupère l'état de toutes les touches
        # Vérifier les touches spécifiques
        if keys[pygame.K_z] or keys[pygame.K_UP]:
            self.player.haut()
            self.player.regarder('haut')
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.player.bas()
            self.player.regarder('bas')
        if keys[pygame.K_q] or keys[pygame.K_LEFT]:
            self.player.gauche()
            self.player.regarder('gauche')
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.player.droite()
            self.player.regarder('droite')

    def add_verif(self):
        """
        Ajoute des vérifications spécifiques à chaque mini-jeu.
        Doit être redéfinie.
        """
        pass

    def add_draw(self, screen):
        """
        Ajoute des éléments à dessiner spécifiques à chaque mini-jeu
        Ne pas appeler cette fonctions dans le code juste la redéfinir.
        """
        pass

    def update(self):
        """
        NE PAS APPELEZ !
        Met à jour la logique de la carte :
        - Effectue les vérifications ajouter via `add_verif`.
        - Met à jour les déplacements et les collisions du joueur.
        - Centre la caméra sur le joueur.
        Ne pas appeller !
        """
        self.add_verif() #rajoute les verifs propres a chaque minijeux

        self.clavier()  # verifie les touches
        self.player.test_deplacement(self.mur) #bouge le joueur si aucune collision (teste x et y separement)
        self.groupe.update()  # met à jour tous le groupe (player._update())

        if self.docenter:
            self.groupe.center(self.player.rect)  # centre cam sur le carré du joueur

    def draw(self, screen):
        """
        NE PAS APPELEZ !
        Dessine tous les éléments de la carte sur l'écran.

        Args:
            screen (pygame.Surface): Surface où dessiner la carte.

        """
        self.groupe.draw(screen) # la carte et le joueur
        self.add_draw(screen) # les truc en plus
        if self.dialogue:
            self.dialogue.draw(screen) # le dialogue

    def quitter(self):
        """
        Donne le nom de la carte suivante à charger ou pas.

        Redéfinir pour les conditions (s'il touche la porte, s'il a gagné...)

        Returns:
            str : Nom de la prochaine carte à charger
            None : None si le joueur reste
        """
        return None

    def __str__(self):
        return "PAS DE NOM"

    ### Simplification
    # Plus d'explication :https://docs.google.com/spreadsheets/d/1jfWB1jZg1Kn6NuOeZZX2NOPTQOpE2bIST9sUAH3L1MM/edit?usp=sharing
    def touche(self, id):
        """
        Vérifie si une touche spécifique est pressée.

        Args:
            id (str): Nom de la touche (ex. : "a", "e", "z", "SPACE") sans le K_.
                      Consultez : https://www.pygame.org/docs/ref/key.html.

        Returns:
            bool: True si la touche est pressée, False sinon.
        """
        return pygame.key.get_pressed()[getattr(pygame, f"K_{id}")]
    def objets_par_classe(self, classe):
        """
        Récupère tous les objets d'une classe spécifique définis dans Tiled.

        Args:
            classe (str): Type d'objet défini dans les propriétés Tiled.

        Returns:
            list[pygame.Rect]: Liste des hitboxes des objets correspondants.
        """
        temp = []
        for obj in self.tmx_data.objects:
            if obj.type == classe:
                temp.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        return temp
    def objet_par_nom(self, name):
        """
        Récupère l'hitbox d'un objet nommé dans Tiled (name).

        Args:
            name (str): Nom de l'objet dans Tiled.

        Returns:
            pygame.Rect: Hitbox de l'objet.
        """
        obj = self.tmx_data.get_object_by_name(name)
        return pygame.Rect(obj.x, obj.y, obj.width, obj.height)
    def objet_par_calque(self, name):
        """
        Récupère tous les objets d'un calque spécifique.

        Args:
            name (str): Nom du calque dans Tiled.

        Returns:
            list[pygame.Rect]: Liste des hitboxes des objets du calque.
        """
        temp = []
        calque_mur = self.tmx_data.get_layer_by_name(name)  # calque des murs
        for obj in calque_mur:
            temp.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))  # ajoute toute les hitbox des murs
        return temp
    def multi_collision(self, liste):
        """
        Vérifie si le joueur touche un des objets d'une liste (mur, echelle, piege ...)

        Args:
            liste (list[pygame.Rect]): Liste des hitboxes à vérifier.

        Returns:
            bool: True si une collision est détectée, False sinon.
        """
        return  self.player.feet.collidelist(liste) > -1
    def collision(self, rect):
        """
        Vérifie si le joueur touche une hitbox spécifique (ex:porte).

        Args:
            rect (pygame.Rect): Hitbox à vérifier.

        Returns:
            bool: True si une collision est détectée, False sinon.
        """
        return self.player.feet.colliderect(rect)

    def tp(self, x, y):
        self.player.coord = [x, y]

    def coord_camera(self, coord):
        """
        Renvoi les coordonnés sur l'ecran en prenant en compte la camera
        """
        return self.map_layer.translate_points([coord])[0]
