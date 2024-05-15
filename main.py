import pygame
import sys
from player import Player, Lizard, Orc
from pause_menu import pause_menu
from arrow import Arrow

pygame.init()
width, height = 679, 676
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game Title")

background_image = pygame.image.load('assets/map.png')
center_image = pygame.image.load('assets/floor_3.png')
center_rect = center_image.get_rect(center=(width // 2, height // 2))
center_image = pygame.transform.scale(center_image, (int(center_image.get_width()*2.5), int(center_image.get_height()*2.5)))

heartFull = pygame.transform.scale(pygame.image.load('assets/ui_heart_full.png'), (32, 32))
heartHalf = pygame.transform.scale(pygame.image.load('assets/ui_heart_half.png'), (32, 32))
heartEmpty = pygame.transform.scale(pygame.image.load('assets/ui_heart_empty.png'), (32, 32))

player = Player(330, 300, 40, 75)
lizard = Lizard(0.4, width, height)
orc = Orc(0.4, width, height)

def drawHealth(screen, health):
    heart_x_start = 10
    heart_y = 10
    hearts_full = health // 10
    hearts_half = (health % 10) // 5

    for i in range(min(hearts_full, 3)):
        screen.blit(heartFull, (heart_x_start + 32 * i, heart_y))

    if hearts_half == 1 and hearts_full < 3:
        screen.blit(heartHalf, (heart_x_start + 32 * hearts_full, heart_y))

    for i in range(hearts_full + hearts_half, 3):
        screen.blit(heartEmpty, (heart_x_start + 32 * i, heart_y))

def checkCollide():
    global last_damage_time
    current_time = pygame.time.get_ticks()

    for enemy in [lizard, orc]:
        if player.rect.colliderect(enemy.rect):
            if current_time - last_damage_time > 1000:
                player.health -= 5
                last_damage_time = current_time

    arrowsToRemove = []
    for arrow in player.arrows:
        for enemy in [lizard, orc]:
            if arrow.rect.colliderect(enemy.rect):
                if enemy.applyDamage(50):
                    pass
                if arrow not in arrowsToRemove:
                    arrowsToRemove.append(arrow)
                break
    for arrow in arrowsToRemove:
        player.arrows.remove(arrow)

def gameOver(screen):
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, (255, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (width // 2, height // 2)
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(3000)


running = True
game_over = False
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

    screen.blit(background_image, (0, 0))
    screen.blit(center_image, center_rect)
    player.draw(screen)
    drawHealth(screen, player.health)

    lizard.move_towards_player(player.rect.x, player.rect.y)
    orc.move_towards_player(player.rect.x, player.rect.y)

    lizard.update()
    orc.update()
    lizard.draw(screen)
    orc.draw(screen)
    player.updateArrows(screen)

    checkCollide()

    if player.health == 0 and not game_over:
        gameOver(screen)
        game_over = True
        pygame.time.wait(1000)
        pause_menu(screen)

    if not game_over:
        pygame.display.flip()

    pygame.display.flip()

pygame.quit()
sys.exit()
