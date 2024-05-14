import pygame
import sys
from player import *
from enemy import *

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

heartWidth = 32
heartHeight = 32

heartFull = pygame.transform.scale(pygame.image.load('assets/ui_heart_full.png'), (heartWidth, heartHeight))
heartHalf = pygame.transform.scale(pygame.image.load('assets/ui_heart_half.png'), (heartWidth, heartHeight))
heartEmpty = pygame.transform.scale(pygame.image.load('assets/ui_heart_empty.png'), (heartWidth, heartHeight))

lizard = Lizard(speed=3, screen_width=width, screen_height=height)
orc = Orc(speed=0.8, screen_width=width, screen_height=height)

player = Player(330, 300, 40, 75)
def drawHealth(screen, health):
    for i in range(3):
        if health > 2*i + 1:
            screen.blit(heartFull, (10+ 32 *i, 10))
        elif health == 2*i + 1:
            screen.blit(heartHalf, (10+ 32 *i, 10))
        else:
            screen.blit(heartEmpty, (10+ 32 *i, 10))

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
    screen.blit(center_image, center_rect)
    player.draw(screen)
    drawHealth(screen, player.health)

    lizard.update()
    orc.update()
    lizard.draw(screen)
    orc.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()
