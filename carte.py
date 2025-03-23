#Projet : Art'Venture
#Auteurs : Anthony Ibanez-Esteban, Raphaël Prost, Aëlys-Coleen Surma Valtaer, Louis Gagne, Mathéo Faure

from math import atan2

import pygame
import pyscroll
import pytmx

from dialogue import Dialogue
from enemy import Enemy
from player import Player
from settings import *
from animation import Animation


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
        self.objetif = None
        self.tmx_data = pytmx.util_pygame.load_pygame(map_file)  # recupere les info de map.tmx
        map_data = pyscroll.TiledMapData(self.tmx_data)  # recupere les info des couches
        self.map_layer = pyscroll.orthographic.BufferedRenderer(map_data, RES)  # genere les couches d'image
        self.map_layer.zoom = ZOOM  # ZOOM de la carte
        player_pos = self.tmx_data.get_object_by_name('spawn') # coord du joueur sur l'objet spawn
        self.player = Player(player_pos.x, player_pos.y - 10)  # creer le joueur

        self.animation = Animation()

        self.pclick = False

        self.groupe = pyscroll.PyscrollGroup(map_layer=self.map_layer,
                                             default_layer=2)  # groupe de toutes les image pour pygame (default_layer = couche du joueur)
        self.groupe.add(self.player)  # rajoute le joueur au groupe d'image

        self.supp = []
        self.projectiles = {}
        self.nombre = 0
        self.bullettimer = 0
        self.timer = 0
        self.canbullet = True

        self.mur = []  # liste de mur (leur hitbox)
        calque_mur = self.tmx_data.get_layer_by_name('mur') #calque des murs
        for obj in calque_mur:
            self.mur.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height)) # ajoute toute les hitbox des murs

        self.font = pygame.font.Font(None, 24)
        self.docenter = True

        self.liste_dialogue = self.get_dialogues()

    def get_dialogues(self):
        temp = {}
        for obj in self.tmx_data.objects:
            if 'Texte' in obj.properties:
                temp[(obj.x, obj.y, obj.width, obj.height)] = obj.properties['Texte']
        if temp : return temp
        else : return False

    def keypressed(self,event):
        if event.key == pygame.K_RETURN or event.key == pygame.K_e:
            self.verif_dialogue()

    def verif_dialogue(self):
        if self.liste_dialogue:
            txt = self.player.rect.collidedict(self.liste_dialogue)
            if txt:
                #self.liste_dialogue.pop(txt[0])
                dialogue = Dialogue(txt[1])
                dialogue.open()
                del dialogue

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
        if keys[pygame.K_p]:
            self.appelanimation()


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

        self.clavier()  # verifie les touches
        self.player.test_deplacement(self.mur) #bouge le joueur si aucune collision (teste x et y separement)
        self.groupe.update()  # met à jour tous le groupe (player._update())

        if self.docenter:
            self.groupe.center(self.player.rect)  # centre cam sur le carré du joueur
        if self.canbullet:
            if self.touche("SPACE") and self.timer >= self.bullettimer:
                self.creer_projectiles()

        self.projectilesdeplacements()

        self.timer += 1
        self.add_verif()  # rajoute les verifs propres a chaque minijeux


    def draw(self, screen):
        """
        NE PAS APPELEZ !
        Dessine tous les éléments de la carte sur l'écran.

        Args:
            screen (pygame.Surface): Surface où dessiner la carte.

        """
        self.groupe.draw(screen) # la carte et le joueur
        self.add_draw(screen) # les truc en plus

    def quitter(self):
        """
        Ne sert plus a rien
        utiliser self.objetif = nom de la prochaine carte
        """
        pass

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
    def points_par_classe(self, classe):
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
                temp.append((obj.x, obj.y))
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

    def fixe_coord(self, coord):
        """
        Renvoi les coordonnés sur l'ecran en prenant en compte la camera
        (les rends fixe sur les coords) (possible sur le joueur)
        """
        return self.map_layer.translate_point(coord)

    def sprite_collision(self, sprite):

        offset = sprite.rect.x - self.player.feet.x, sprite.rect.y - self.player.feet.y
        return self.player.mask.overlap(sprite.mask, offset)

    def multi_sprite_collision(self, liste):
        for sprite in liste:
            offset = sprite.rect.x - self.player.rect.x, sprite.rect.y - self.player.rect.y
            if self.player.mask.overlap(sprite.mask, offset):
                return True
        return False

    def angletir(self):#,obj):
        x2, y2 = pygame.mouse.get_pos()#obj
        x1, y1 = self.fixe_coord(self.player.rect.center)
        return atan2((y2-y1),(x2-x1))

    def creer_projectiles(self):
        self.projectiles["enemie"+str(self.nombre)] = Enemy("img/fire.png",self.player.rect.center[0],self.player.rect.center[1])
        self.projectiles["enemie"+str(self.nombre)].alpha = self.angletir()
        self.projectiles["enemie" + str(self.nombre)].speed = 1
        self.groupe.add(self.projectiles["enemie" + str(self.nombre)])
        self.nombre += 1
        self.bullettimer = self.timer + 60*5 #tps * sec

    def projectilesdeplacements(self):
        for key in list(self.projectiles.keys()):  # Copie des clés
            enemie = self.projectiles[key]

            if enemie.is_off_screen():
                self.supp.append(key)  # On marque pour suppression
            else:
                enemie.avancer()

        # Deuxième boucle : suppression après l'itération
        for sup in self.supp:
            self.projectiles.pop(sup, None)  # pop() évite l'erreur si la clé a déjà été supprimée

    def appelanimation(self):
        coord = self.player.coord
        self.docenter = False
        self.player.coord = [-16,16]
        self.player.update()
        self.groupe.draw(pygame.display.get_surface())
        pygame.display.flip()
        self.animation.open(self.fixe_coord(coord))
        self.docenter = True
        self.player.coord = coord

    def death_animation(self):
        self.animation.game_over(self.fixe_coord(self.player.middle))
