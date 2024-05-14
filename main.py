import pygame
from player import *

pygame.init()

LARGEUR, HAUTEUR = 679, 676
surface = pygame.display.set_mode(LARGEUR, HAUTEUR)
pygame.display.set_caption('HadèsLikeGaming')
background = pygame.image.load("assets/map.png").convert_alpha()


running = True
FPS = 60
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(FPS)

pygame.quit()
