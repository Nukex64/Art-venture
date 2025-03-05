import pygame
from mini_jeux.ville import Ville
from mini_jeux.parcours import *
from mini_jeux.laby import Laby
from mini_jeux.undertale_2 import Undertale
from settings import *
from menu import Menu
from mini_jeux.road import Road
from mini_jeux.mask import Mask
from savefonction import sauvegarde

class Jeu:
    def __init__(self):
        """
        Initialise le jeu, configure la fenêtre de jeu, et définit les cartes et mini-jeux disponibles.
        """

        pygame.mixer.music.load("sounds\projectnsi.mp3")
        pygame.mixer.music.set_volume(0.05)


        self.saveload = sauvegarde()
        if self.saveload.changer_json("Musiques",None):
            pygame.mixer.music.play(loops=-1)
        self.run = True
        self.screen = pygame.display.set_mode(RES,pygame.NOFRAME|pygame.SCALED)
        self.clock = pygame.time.Clock()

        ville = Ville()
        parcour_1 = Game_Jump()
        laby = Laby()
        road = Road()
        mask = Mask()
        undertale = Undertale()


        self.dico_game = {"Ville": ville,"Parcours": parcour_1, "Laby":laby,"Road": road, "Mask":mask, "Undertale":undertale}

        self.carte = self.dico_game[self.saveload.save["world"]]  # lancer en premier la ville
        self.menu = Menu()

    def _get_suface(self):
        """
        Crée et renvoie la surface à dessiner sur l'écran.
        La surface contient la carte actuelle du jeu, qui est dessinée sur l'écran.
        (60/s)
        """
        surface = pygame.Surface(RES)
        self.carte.draw(surface)
        return surface

    def _update(self):
        """
        Met à jour l'état de la carte et affiche les changements à l'écran
        Cette méthode met à jour le jeu en appelant les méthodes d'_update et de dessin de la carte.
        (60/s)
        """
        self.clock.tick(60)  # fps 60/s
        self.carte.update()  # met a jour le jeu/carte actuelle
        self.screen.blit(self._get_suface(),(0, 0))  # affiche sur l'ecran
        pygame.display.set_caption(f"{self.clock.get_fps():.1f}")
        pygame.display.flip()  # met a jour tous les pixels de l'ecran


    def _changer_carte(self):
        """
        Change la carte en fonction de la carte actuelle,
        La méthode met à jour la carte avec une nouvelle valeur tirée du dictionnaire des jeux
        cf Carte.quitter()
        """
        objetif = self.carte.quitter()
        if objetif:
            if objetif in self.dico_game:
                self.carte = self.dico_game[objetif]
                print(f"Changement de carte : {str(self.carte)}")
                self.saveload.changer_json("world", str(self.carte))
            else: print(f"ERREUR : aucun {objetif}")

    def _gerer_event(self):
        """
        Gère les événements du jeu (clavier, fermeture de la fenêtre, etc.).
        (60/s)
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # quitter
                self.run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self._changer_carte()
                if event.key == pygame.K_F1:
                    print(pygame.mouse.get_pos())
                if event.key == pygame.K_KP0:
                    self.carte = self.dico_game["Ville"]
                    print(f"Changement de carte : ville (dev)")
                if event.key == pygame.K_ESCAPE:
                    self.menu.open()
                    if self.menu.end:
                        self.run = False

    def running(self):
        print("-" * 10 + " EVENEMENT " + "-" * 10)
        """
        Démarre la boucle principale du jeu.
        La méthode fait tourner le jeu en boucle jusqu'à ce que l'utilisateur décide de quitter.
        Elle gère les événements, met à jour le jeu et affiche le contenu de l'écran à chaque fram

        Button entrer : demande au jeu où le joueur doit aller ensuite (None ne change pas)
        Button quitter : quitte le jeu stop la boucle
        (60/s)
        """

        while self.run: #boucle du jeu
            self._gerer_event() # quitter / changer carte / crash
            self._update() #met a jour tous le jeu
        print("-" * 13 + " END " + "-" * 13)

if __name__ == '__main__':
    pygame.init()   # lance pygame
    jeu = Jeu()
    jeu.running()
    pygame.quit()   # stop pygame