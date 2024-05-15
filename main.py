import pygame
import sys
from player import *
from arrow import *
from enemy import *

pygame.init()
width, height = 679, 676
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("HadèsLike")

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

tp_x, tp_y = 330, 292
tp_width, tp_height = 50, 50
next_room_tp = pygame.Rect(tp_x, tp_y, tp_width, tp_height)

lizard = Lizard(speed=0.25, screen_width=width, screen_height=height)
orc = Orc(speed=0.25, screen_width=width, screen_height=height)

last_damage_time = 0

enemies = [lizard, orc]

player = Player(330, 300, 40, 75)
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

def checkCollide(arrows, enemies):
    arrows_to_remove = []
    enemies_to_remove = []

    for arrow in arrows:
        for enemy in enemies:
            if arrow.rect.colliderect(enemy.rect):
                if enemy.applyDamage(5):
                    enemies_to_remove.append(enemy)
                arrows_to_remove.append(arrow)
                break

    for enemy in enemies_to_remove:
        enemies.remove(enemy)

    for arrow in arrows_to_remove:
        arrows.remove(arrow)

def all_ennemy_defeated(enemies):
    return all(not enemy.isAlive() for enemy in enemies)

def load_next_room():
    global enemies
    double_count = len(enemies) * 2
    enemies = create_enemies(double_count // 2, 0.4, width, height, Lizard) + create_enemies(double_count // 2, 0.4, width, height, Orc)
    print(f"Loaded {double_count} enemies in the next room.")

def create_enemies(count, speed, width, height, enemy_type=Lizard):
    return [enemy_type(speed=speed, screen_width=width, screen_height=height) for _ in range(count)]

running = True
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if player.rect.colliderect(next_room_tp) and all_ennemy_defeated(enemies):
            load_next_room()
        if all_ennemy_defeated(enemies):
            print("La plaque de téléportation est maintenant utilisable!")
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

    for enemy in enemies:
        enemy.move_towards_player(player.rect.x, player.rect.y)
        enemy.update()
        enemy.draw(screen)

    lizard.move_towards_player(player.rect.x, player.rect.y)
    orc.move_towards_player(player.rect.x, player.rect.y)

    lizard.update()
    orc.update()
    lizard.draw(screen)
    orc.draw(screen)
    player.updateArrows(screen)

    checkCollide(player.arrows, enemies)

    pygame.display.flip()

pygame.quit()
sys.exit()
