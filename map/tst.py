import pygame

# Initialisation
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Paramètres du trou
r = 100  # Rayon du trou
pos = (400, 300)  # Position du trou

running = True
while running:
    screen.fill((0, 0, 255))  # Fond bleu pour bien voir l'effet

    # Créer une surface noire avec transparence
    mask = pygame.Surface((800, 600), pygame.SRCALPHA)
    mask.fill((0, 0, 0, 200))  # Couleur noire semi-transparente (A=200)

    # Dessiner un cercle transparent dans la surface noire
    pygame.draw.circle(mask, (0, 0, 0, 0), pos, r)  # Alpha = 0 -> Transparent

    # Afficher la surface masquée sur l’écran
    screen.blit(mask, (0, 0))

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            pos = event.pos  # Déplacer le trou avec la souris
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                r += 10  # Augmenter le rayon
            elif event.key == pygame.K_DOWN:
                r = max(10, r - 10)  # Diminuer le rayon, minimum 10

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
