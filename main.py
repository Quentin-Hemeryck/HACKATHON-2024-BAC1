import pygame
import sys
from player import Player

pygame.init()

width, height = 679, 676
screen = pygame.display.set_mode((width, height))

background_image = pygame.image.load('assets/map.png')
center_image = pygame.image.load('assets/floor_3.png')
center_rect = center_image.get_rect()
center_rect.center = (width // 2, height // 2)

new_width = int(center_image.get_width()*2.5)
new_height = int(center_image.get_height()*2.5)
center_image = pygame.transform.scale(center_image, (new_width, new_height))

player = Player(330, 300, 40, 75)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_l:
                player.attack()
            elif event.key == pygame.K_m:
                player.shootArrow()
            elif event.key == pygame.K_1:
                player.switchWeapon()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_l:
                player.stop_attack()

    keys = pygame.key.get_pressed()
    player.move(keys)
    player.updateArrows(screen)

    screen.blit(background_image, (0, 0))
    screen.blit(center_image, center_rect)  # Blit the central image
    player.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()
