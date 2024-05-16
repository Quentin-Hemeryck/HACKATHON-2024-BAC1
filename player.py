import pygame
from arrow import *

class Player:
    """
    Classe représentant le joueur.
    """
    def __init__(self, x, y, width=50, height=50, health=30):
        self.__images = {
            'right': pygame.image.load("assets/elf_f_run_anim_f0.png"),
            'left': pygame.image.load("assets/left_view_elf_f_run_anim_f0.png"),
            'up': pygame.image.load("assets/elf_f_run_anim_f1.png"),
            'down': pygame.image.load("assets/left_view_elf_f_run_anim_f0.png")
        }
        self.__current_direction = "right"
        self.__current_image = pygame.transform.scale(self.__images[self.__current_direction], (width, height))
        self.__rect = self.__current_image.get_rect()
        self.__rect.x = x
        self.__rect.y = y
        self.__speed = 1.7
        self.__attack_frame = 0
        self.__weapons = {
            'hammer': {
                'right': pygame.image.load("assets/weapon_big_hammer.png"),
                'left': pygame.image.load("assets/weapon_big_hammer.png"),
                'up': pygame.image.load("assets/weapon_big_hammer.png"),
                'down': pygame.image.load("assets/weapon_big_hammer.png")
            },
            "hammer_attack": {
                'right': pygame.image.load("assets/right_weapon_big_hammer.png"),
                'left': pygame.image.load("assets/left_weapon_big_hammer.png"),
                'up': pygame.image.load("assets/weapon_big_hammer.png"),
                'down': pygame.image.load("assets/weapon_big_hammer.png")
            },
            "bow": {
                'right': pygame.image.load("assets/weapon_bow.png"),
                'left': pygame.image.load("assets/reverse_weapon_bow.png"),
                'up': pygame.image.load("assets/weapon_bow.png"),
                'down': pygame.image.load("assets/reverse_weapon_bow.png")
            }
        }
        self.__current_weapon = 'hammer'
        self.__weapon_image = self.__weapons[self.__current_weapon][self.__current_direction]
        self.__weapon_rect = self.__weapon_image.get_rect()
        self.__attacking = False
        self.__arrows = []
        self.__health = health
        self.__invincible = False
        self.__invincible_start_time = 0

    @property
    def images(self):
        return self.__images

    @images.setter
    def images(self, value):
        self.images = value

    @property
    def current_direction(self):
        return self.__current_direction

    @current_direction.setter
    def current_direction(self, value):
        self.__current_direction = value

    @property
    def current_image(self):
        return self.__current_image

    @current_image.setter
    def current_image(self, value):
        self.__current_image = value

    @property
    def rect(self):
        return self.__rect

    @rect.setter
    def rect(self, value):
        self.__rect = value

    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self, value):
        self.__speed = value

    @property
    def attack_frame(self):
        return self.__attack_frame

    @attack_frame.setter
    def attack_frame(self, value):
        self.__attack_frame = value

    @property
    def weapons(self):
        return self.__weapons

    @weapons.setter
    def weapons(self, value):
        self.__weapons = value

    @property
    def current_weapon(self):
        return self.__current_weapon

    @current_weapon.setter
    def current_weapon(self, value):
        self.__current_weapon = value

    @property
    def weapon_image(self):
        return self.__weapon_image

    @weapon_image.setter
    def weapon_image(self, value):
        self.__weapon_image = value

    @property
    def weapon_rect(self):
        return self.__weapon_rect

    @weapon_rect.setter
    def weapon_rect(self, value):
        self.__weapon_rect = value

    @property
    def attacking(self):
        return self.__attacking

    @attacking.setter
    def attacking(self, value):
        self.__attacking = value

    @property
    def arrows(self):
        return self.__arrows

    @arrows.setter
    def arrows(self, value):
        self.__arrows = value

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, value):
        self.__health = value

    @property
    def invincible(self):
        return self.__invincible

    @invincible.setter
    def invincible(self, value):
        self.__invincible = value

    @property
    def invincible_start_time(self):
        return self.__invincible_start_time

    @invincible_start_time.setter
    def invincible_start_time(self, value):
        self.__invincible_start_time = value

    def move(self, keys):
        """
        Déplace le joueur en fonction des touches pressées.
        """
        def check_oob(x, y):
            limit_x = [18, 629]
            limit_y = [2, 557]
            if x < limit_x[0] or x > limit_x[1]:
                return False
            if y < limit_y[0] or y > limit_y[1]:
                return False
            return True

        moved = False
        if keys[pygame.K_q] and check_oob(self.__rect.x - self.__speed, self.__rect.y):
            self.__rect.x -= self.__speed
            self.__current_direction = 'left'
            moved = True
        if keys[pygame.K_d] and check_oob(self.__rect.x + self.__speed, self.__rect.y):
            self.__rect.x += self.__speed
            self.__current_direction = 'right'
            moved = True
        if keys[pygame.K_z] and check_oob(self.__rect.x, self.__rect.y - self.__speed):
            self.__rect.y -= self.__speed
            self.__current_direction = 'up'
            moved = True
        if keys[pygame.K_s] and check_oob(self.__rect.x, self.__rect.y + self.__speed):
            self.__rect.y += self.__speed
            self.__current_direction = 'down'
            moved = True

        if moved:
            self.__current_image = pygame.transform.scale(self.__images[self.__current_direction],
                                                        (self.__rect.width, self.__rect.height))
            self.__rect = self.__current_image.get_rect(center=self.__rect.center)
            if self.__current_weapon == 'bow' or self.__current_weapon == 'hammer':
                self.__weapon_image = self.__weapons[self.__current_weapon][self.__current_direction]
                self.__weapon_rect = self.__weapon_image.get_rect()

    def draw(self, screen):
        """
        Dessine le joueur à l'écran.
        """
        screen.blit(self.__current_image, self.__rect.topleft)
        if self.__attacking:
            attack_position = (self.__rect.right - 10, self.__rect.top + 10 + self.__rect.height // 2 - self.__weapon_rect.height // 2)
            screen.blit(self.__weapon_image, attack_position)

    def attack(self):
        """
        Déclenche l'attaque du joueur.
        """
        self.__attacking = True

    def updateArrows(self, screen):
        """
        Met à jour et dessine les flèches du joueur.
        """
        for arrow in self.__arrows[:]:
            arrow.draw(screen)
            if not arrow.update():
                self.__arrows.remove(arrow)

    def shootArrow(self):
        """
        Tire une flèche dans la direction actuelle du joueur.
        """
        if self.__current_weapon == "bow":
            direction = self.__current_direction
            arrow_image_paths = {
                'right': "assets/weapon_arrow.png",
                'left': "assets/reverse_weapon_arrow.png",
                'up': "assets/up_weapon_arrow.png",
                'down': "assets/down_weapon_arrow.png"
            }
            if direction == 'right':
                new_arrow = Arrow(self.__rect.right, self.__rect.centery, direction, arrow_image_paths[direction])
            elif direction == 'left':
                new_arrow = Arrow(self.__rect.left, self.__rect.centery, direction, arrow_image_paths[direction])
            elif direction == 'up':
                new_arrow = Arrow(self.__rect.centerx, self.__rect.top, direction, arrow_image_paths[direction])
            elif direction == 'down':
                new_arrow = Arrow(self.__rect.centerx, self.__rect.bottom, direction, arrow_image_paths[direction])
            self.__arrows.append(new_arrow)
            print(f"arrow shot from position: ({new_arrow.rect.x}, {new_arrow.rect.y})")

    def swingHammer(self, enemies):
        """
        Frappe avec le marteau et vérifie les collisions avec les ennemis.
        """
        if self.__current_weapon == "hammer":
            self.__weapon_image = self.__weapons['hammer_attack'][self.__current_direction]
            self.__weapon_rect = self.__weapon_image.get_rect(center=self.__rect.center)
            hammer_damage = 25
            for enemy in enemies:
                if self.__weapon_rect.colliderect(enemy.rect):
                    enemy.applyDamage(hammer_damage)
                    print(f"Hit enemy with hammer at position: ({enemy.rect.x}, {enemy.rect.y})")
            self.__weapon_image = self.__weapons[self.__current_weapon][self.__current_direction]

    def stop_attack(self):
        """
        Arrête l'attaque du joueur.
        """
        self.__attacking = False

    def switchWeapon(self):
        """
        Change l'arme actuelle du joueur.
        """
        if self.__current_weapon == 'hammer':
            self.__current_weapon = 'bow'
        else:
            self.__current_weapon = 'hammer'
        self.__weapon_image = self.__weapons[self.__current_weapon][self.__current_direction]
        self.__weapon_rect = self.__weapon_image.get_rect()

    def take_damage(self, damage):
        """
        Inflige des dégâts au joueur.
        """
        if not self.__invincible:
            self.__health -= damage
            self.__invincible = True
            self.__invincible_start_time = pygame.time.get_ticks()
            print(f"Player health: {self.__health}")

    def update_invincibility(self):
        """
        Met à jour l'état d'invincibilité du joueur.
        """
        if self.__invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.__invincible_start_time >= 1000:
                self.__invincible = False
