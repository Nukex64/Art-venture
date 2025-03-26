#Projet : Art'Venture
#Auteurs : Anthony Ibanez-Esteban, Raphaël Prost, Aëlys-Coleen Surma Valtaer, Louis Gagne, Mathéo Faure

from math import atan2, cos, sin

import pygame.draw

from carte import Carte
from enemy import Enemy


class Game_Jump(Carte):
    """
    Exemple de mini jeux de jump / parcoure
    """
    def __init__(self):
        super().__init__("map/jump.tmx") # on donne la map
        self.liste_echelle = self.objets_par_classe('echelle') # on recupere les echelles
        self.liste_saut = self.objets_par_classe('saut')  # on recupere les echelles
        self.sortie = self.objets_par_classe('sortie')
        self.liste_sol = self.objet_par_calque('sol') # on recupere les sols
        self.liste_spike = self.get_spike_liste()
        self.frame_jump = 0 # timer de jump
        self.last_y = 0
        self.start_y = 0
        self.can_dash = True
        self.frame_dash = 0
        self.dash_animation = []
        self.dash_vector = (0, 0)
        self.docenter = True

        self.spike_mask = pygame.mask.from_surface(self.tmx_data.get_tile_image_by_gid(53))
        self.liste_spike_sprite = []
        self.spike_1 = Enemy('img/spike.png', 110, 120)
        self.liste_spike_sprite.append(self.spike_1)
        self.spike_2 = Enemy('img/spike.png', 485, 120)
        self.liste_spike_sprite.append(self.spike_2)
        self.spike_3 = Enemy('img/spike.png', 350, 100)
        self.liste_spike_sprite.append(self.spike_3)

        for sprite in self.liste_spike_sprite:
            sprite.speed = 2
            self.groupe.add(sprite)

    def add_verif(self):
        if self.frame_jump > 0:
            self.anti_gravity()
            self.jump()

        if self.frame_dash > 0: # dash annule vitesse saut
            self.anti_gravity()
            self.dash()

        if self.multi_collision(self.liste_echelle):
            self.anti_gravity()


        self.test_spkie_collision()

        self.gravity()

        self.spike_1.alpha -= 0.05
        self.spike_1.avancer()

        self.spike_2.alternate(((485, 120), (485, 40)))
        self.spike_3.alternate(((350, 100), (405, 100) , (405, 116), (450, 116)))


    def add_draw(self, screen):
        y = self.fixe_coord(self.player.feet.midbottom)[1]
        color = (0, 0, 0) if self.can_dash else (255, 0, 0)
        #pygame.draw.line(screen, color,(0, y) ,(800, y))
        #self.draw_grid(screen, tile_size=18)


        for info in self.dash_animation:
            coord, flou = info
            if flou == 0 : self.dash_animation.remove(info)
            coord = self.fixe_coord(coord)
            img = self.player.get_image_transparent(flou)
            info[1] -= 6
            screen.blit(img, coord)

    def clavier(self):
        keys = pygame.key.get_pressed()

        if self.can_dash and pygame.mouse.get_pressed()[0]:
            direction = (keys[pygame.K_z] * 1, keys[pygame.K_q] * -1, keys[pygame.K_s] * -1, keys[pygame.K_d] * 1)
            alpha = self.calcule_direction(direction)
            self.start_dash(alpha)

        if keys[pygame.K_d]:
            self.player.droite()
            self.player.regarder('droite')

        if keys[pygame.K_q]:
            self.player.gauche()
            self.player.regarder('gauche')

        if self.multi_collision(self.liste_echelle) and not self.frame_dash: # si il est sur l'echelle
            self.player.regarder('haut')
            if keys[pygame.K_z]:
                self.player.haut()
            if keys[pygame.K_s]:
                self.player.bas()
        else:
            if self.frame_jump == 0:
                if keys[pygame.K_SPACE] : # jump
                    if self.player.under_feet.collidelist(self.mur) > -1 : #touche un mur
                        self.frame_jump = 36
                        self.start_y = self.player.coord[1]
                        self.last_y  = self.player.coord[1]
                        #if self.frame_dash < 1 and not self.can_dash:
                        #    self.can_dash = True

        if self.frame_dash < 2 and not self.can_dash:
            if self.player.under_feet.collidelist(self.mur) > -1:
                self.can_dash = True


        if self.touche("RETURN") and self.multi_collision(self.sortie):
            self.objetif = "Ville"

    def __str__(self):
        return "Parcours"

    @staticmethod
    def f(x):
        return (x * (36 - x)) / 162

    @staticmethod
    def round_alpha(x):
        if x < 0 : x = 360+x
        return round((x%360)/45)*45

    def gravity(self):
        self.player.vy += 2

    def anti_gravity(self):
        self.player.vy -= 2

    def jump(self):
        new_y = self.f(self.frame_jump)*18 + self.start_y #nouvelle coordonné
        vy = new_y - self.last_y # de combien il doit monter
        self.player.vy -= vy
        self.last_y = new_y
        self.frame_jump -= 1


    def draw_grid(self, surface, tile_size, color=(0, 0, 0)):
        width, height = surface.get_size()

        for y in range(0, height, tile_size):
            f = self.fixe_coord((0, y))[1]
            pygame.draw.line(surface, color, (0, f), (width, f))

    def start_dash(self, alpha):
        pygame.time.wait(50)
        self.can_dash = False
        self.frame_dash = 15
        dist = 7 #puissance de dash
        vx, vy = cos(alpha)*dist , sin(alpha)*dist
        self.dash_vector = (vx, vy)

    def dash(self):
        vx, vy = self.dash_vector
        self.player.vx = vx
        self.player.vy = vy
        self.dash_animation.append([self.player.coord.copy(), 90])
        self.frame_dash -= 1

    def get_spike_liste(self):
        spike_layer = self.tmx_data.get_layer_by_name("spike")
        spike_liste = []
        for x, y, gid in spike_layer:
            if gid: # Si une tuile est présente
                rect = pygame.Rect(x * 18 ,y * 18, 18, 18)
                spike_liste.append(rect)
        return spike_liste

    def test_spkie_collision(self):
        spkie_col = self.player.rect.collidelist(self.liste_spike)
        if spkie_col != -1:
            x1, y1 = self.liste_spike[spkie_col].topleft
            x2, y2 = self.player.feet.topleft
            offset = x1 - x2, y1 - y2
            if self.player.mask.overlap(self.spike_mask, offset):
                self.game_over()
        if self.multi_sprite_collision(self.liste_spike_sprite):
            self.game_over()

    def game_over(self):
        self.death_animation()
        self.tp(130, 240)
        print("oof")

    @staticmethod
    def calcule_direction(direction):
        x, y  = direction[0] + direction[2], direction[1] + direction[3]
        return -atan2(x, y) # *-1 car pygame inverse cercle trigo

