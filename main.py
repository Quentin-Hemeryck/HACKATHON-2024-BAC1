import pygame
import sys
from player import *
from arrow import *
from enemy import *
import json

pygame.init()
pygame.mixer.init()
width, height = 679, 676
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Underworld's Call")
pygame.display.set_icon(pygame.image.load('assets/logo.png'))

background_image = pygame.image.load('assets/map.png')
center_image = pygame.image.load('assets/floor_3.png')
center_rect = center_image.get_rect()
center_rect.center = (width // 2, height // 2)

new_width = int(center_image.get_width() * 2.5)
new_height = int(center_image.get_height() * 2.5)
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
boss = Boss(speed=0.3, screen_width=width, screen_height=height)

last_damage_time = 0

enemies = [lizard, orc]

player = Player(330, 300, 40, 75)

pygame.mixer.music.load('sounds/GameIsOn.wav')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

game_over_sound = pygame.mixer.Sound('sounds/gameOver.wav')
teleport_sound = pygame.mixer.Sound('sounds/Teleport.wav')
power_up_sound = pygame.mixer.Sound('sounds/powerUp.wav')


def drawHealth(screen, health):
    """
    Dessine les cœurs représentant la santé du joueur à l'écran.
    """
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
    """
    Vérifie les collisions entre les flèches et les ennemis.
    """
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


def checkHammerCollide(player, enemies):
    """
    Vérifie les collisions entre le marteau du joueur et les ennemis.
    """
    if player.attacking and player.current_weapon == 'hammer':
        player.swingHammer(enemies)


def check_player_enemy_collisions(player, enemies):
    """
    Vérifie les collisions entre le joueur et les ennemis.
    """
    for enemy in enemies:
        if player.rect.colliderect(enemy.rect):
            player.take_damage(5)


def all_enemies_defeated(enemies):
    """
    Vérifie si tous les ennemis ont été vaincus.
    """
    return all(not enemy.isAlive() for enemy in enemies)


def load_next_wave(enemies, wave):
    """
    Charge la prochaine vague d'ennemis.
    """
    new_enemies = create_enemies(len(enemies) * 2, 0.4, width, height, Lizard) + create_enemies(len(enemies) * 2, 0.4,
                                                                                                width, height, Orc)
    if wave == 2:
        new_enemies.append(Boss(speed=0.3, screen_width=width, screen_height=height))
    return new_enemies


def create_enemies(count, speed, width, height, enemy_type=Lizard):
    """
    Crée une liste d'ennemis.
    """
    return [enemy_type(speed=speed, screen_width=width, screen_height=height) for _ in range(count)]


def render_text_with_outline(font, text, text_color, outline_color):
    """
    Rendu d'un texte avec un contour.
    """
    base = font.render(text, True, text_color)
    width = base.get_width() + 2
    height = base.get_height() + 2

    img = pygame.Surface((width, height), pygame.SRCALPHA)

    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]:
        img.blit(font.render(text, True, outline_color), (dx + 1, dy + 1))

    img.blit(base, (1, 1))

    return img


def main_menu():
    """
    Affiche le menu principal et gère la sélection des options.
    """
    menu = True
    selected = "start"
    background_menu_image = pygame.image.load('assets/backgroundMenu.png')
    font = pygame.font.Font("fonts/font.ttf", 30)
    text_color = (255, 255, 0)
    outline_color = (255, 255, 255)

    while menu:
        screen.blit(background_menu_image, (0, 0))

        normal_mode = render_text_with_outline(font, "Normal Mode", text_color, outline_color)
        time_trial_mode = render_text_with_outline(font, "Time Trial Mode", text_color, outline_color)
        exit_game = render_text_with_outline(font, "Exit", text_color, outline_color)

        normal_mode_rect = normal_mode.get_rect(center=(width // 2, height // 2))
        time_trial_mode_rect = time_trial_mode.get_rect(center=(width // 2, height // 2 + 60))
        exit_game_rect = exit_game.get_rect(center=(width // 2, height // 2 + 120))

        if selected == "start":
            pygame.draw.rect(screen, (255, 0, 0), normal_mode_rect.inflate(20, 10), 3)
        if selected == "time_trial":
            pygame.draw.rect(screen, (255, 0, 0), time_trial_mode_rect.inflate(20, 10), 3)
        if selected == "exit":
            pygame.draw.rect(screen, (255, 0, 0), exit_game_rect.inflate(20, 10), 3)

        screen.blit(normal_mode, normal_mode_rect)
        screen.blit(time_trial_mode, time_trial_mode_rect)
        screen.blit(exit_game, exit_game_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if selected == "time_trial":
                        selected = "start"
                    elif selected == "exit":
                        selected = "time_trial"
                elif event.key == pygame.K_DOWN:
                    if selected == "start":
                        selected = "time_trial"
                    elif selected == "time_trial":
                        selected = "exit"
                elif event.key == pygame.K_RETURN:
                    if selected == "start":
                        pygame.mixer.music.load('sounds/DemonsSouls.wav')
                        pygame.mixer.music.play(-1)
                        menu = False
                    elif selected == "time_trial":
                        pygame.mixer.music.load('sounds/DemonsSouls.wav')
                        pygame.mixer.music.play(-1)
                        menu = False
                    elif selected == "exit":
                        pygame.quit()
                        sys.exit()


def game_over_screen():
    """
    Affiche l'écran de game over.
    """
    pygame.mixer.music.stop()
    game_over_sound.play()
    font = pygame.font.Font("fonts/font.ttf", 64)
    text_color = (255, 0, 0)
    outline_color = (0, 0, 0)
    game_over_text = render_text_with_outline(font, "Game Over", text_color, outline_color)
    game_over_rect = game_over_text.get_rect(center=(width // 2, height // 2))
    screen.blit(game_over_text, game_over_rect)
    pygame.display.update()


def save_game(player, enemies, wave):
    """
    Sauvegarde l'état actuel du jeu dans un fichier JSON.
    """
    game_state = {
        'player': {
            'x': player.rect.x,
            'y': player.rect.y,
            'health': player.health,
            'current_weapon': player.current_weapon
        },
        'enemies': [{
            'type': type(enemy).__name__,
            'x': enemy.rect.x,
            'y': enemy.rect.y,
            'health': enemy.mobHealth
        } for enemy in enemies],
        'wave': wave
    }
    with open('save/savegame.json', 'w') as save_file:
        json.dump(game_state, save_file)


def pause_menu():
    """
    Affiche le menu de pause et gère la sélection des options.
    """
    paused = True
    selected = "resume"
    background_menu_image = pygame.image.load('assets/backgroundMenu.png')
    font = pygame.font.Font("fonts/font.ttf", 30)
    text_color = (255, 255, 0)
    outline_color = (255, 255, 255)

    pygame.mixer.music.load('sounds/GameIsOn.wav')
    pygame.mixer.music.play(-1)

    while paused:
        screen.blit(background_menu_image, (0, 0))

        resume_text = render_text_with_outline(font, "Resume", text_color, outline_color)
        save_text = render_text_with_outline(font, "Save Game", text_color, outline_color)
        upgrade_text = render_text_with_outline(font, "Upgrade", text_color, outline_color)
        quit_text = render_text_with_outline(font, "Quit", text_color, outline_color)

        resume_rect = resume_text.get_rect(center=(width // 2, height // 2 - 60))
        save_rect = save_text.get_rect(center=(width // 2, height // 2))
        upgrade_rect = upgrade_text.get_rect(center=(width // 2, height // 2 + 60))
        quit_rect = quit_text.get_rect(center=(width // 2, height // 2 + 120))

        if selected == "resume":
            pygame.draw.rect(screen, (255, 0, 0), resume_rect.inflate(20, 10), 3)
        if selected == "save":
            pygame.draw.rect(screen, (255, 0, 0), save_rect.inflate(20, 10), 3)
        if selected == "upgrade":
            pygame.draw.rect(screen, (255, 0, 0), upgrade_rect.inflate(20, 10), 3)
        if selected == "quit":
            pygame.draw.rect(screen, (255, 0, 0), quit_rect.inflate(20, 10), 3)

        screen.blit(resume_text, resume_rect)
        screen.blit(save_text, save_rect)
        screen.blit(upgrade_text, upgrade_rect)
        screen.blit(quit_text, quit_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if selected == "save":
                        selected = "resume"
                    elif selected == "upgrade":
                        selected = "save"
                    elif selected == "quit":
                        selected = "upgrade"
                elif event.key == pygame.K_DOWN:
                    if selected == "resume":
                        selected = "save"
                    elif selected == "save":
                        selected = "upgrade"
                    elif selected == "upgrade":
                        selected = "quit"
                elif event.key == pygame.K_RETURN:
                    if selected == "resume":
                        paused = False
                        pygame.mixer.music.load('sounds/DemonsSouls.wav')
                        pygame.mixer.music.play(-1)
                    elif selected == "save":
                        save_game(player, enemies, wave)
                    elif selected == "upgrade":
                        paused = False
                        player.speed += 0.5
                        power_up_sound.play()
                    elif selected == "quit":
                        main_menu()


running = True
game_over = False
wave = 1

main_menu()

""" Boucle de jeu """
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pause_menu()
            elif event.key == pygame.K_l:
                player.attack()
            elif event.key == pygame.K_m and player.attacking:
                if player.current_weapon == 'bow':
                    player.shootArrow()
                elif player.current_weapon == 'hammer':
                    player.swingHammer(enemies)
            elif event.key == pygame.K_1:
                player.switchWeapon()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_l:
                player.stop_attack()

    keys = pygame.key.get_pressed()
    player.move(keys)

    if all_enemies_defeated(enemies) and player.rect.colliderect(next_room_tp):
        teleport_sound.play()
        if wave < 2:
            wave += 1
            enemies = load_next_wave(enemies, wave)
        else:
            enemies.append(Boss(speed=0.3, screen_width=width, screen_height=height))

    checkHammerCollide(player, enemies)
    check_player_enemy_collisions(player, enemies)
    player.update_invincibility()

    screen.blit(background_image, (0, 0))
    screen.blit(center_image, center_rect)
    player.draw(screen)
    drawHealth(screen, player.health)

    for enemy in enemies:
        enemy.move_towards_player(player.rect.x, player.rect.y)
        enemy.update()
        enemy.draw(screen)

    if player.health <= 0:
        game_over_screen()
        pygame.time.wait(3000)
        running = False
    player.updateArrows(screen)

    checkCollide(player.arrows, enemies)

    pygame.display.flip()

pygame.quit()
sys.exit()
