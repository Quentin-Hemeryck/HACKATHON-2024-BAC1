import pygame
from arrow import *

class Player:
    def __init__(self, x, y, width=50, height=50, health=30):
        self.original_image = pygame.image.load('assets/elf_f_run_anim_f0.png')
        self.image = pygame.transform.scale(self.original_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.attack_frame = 0
        self.weapons = {
            'hammer': pygame.image.load("assets/weapon_big_hammer.png"),
            "bow": pygame.image.load("assets/weapon_bow.png")
        }
        self.current_weapon = 'hammer'
        self.weapon_image = self.weapons[self.current_weapon]
        self.weapon_rect = self.weapon_image.get_rect()
        self.attacking = False
        self.arrows = []
        self.health = health

    def move(self, keys):
        def check_oob(x, y):
            limit_x = [18, 629]
            limit_y = [2, 557]
            if x < limit_x[0] or x > limit_x[1]:
                return False
            if y < limit_y[0] or y > limit_y[1]:
                return False
            return True

        if keys[pygame.K_q] and check_oob(self.rect.x - self.speed, self.rect.y):
            self.rect.x -= self.speed
        if keys[pygame.K_d] and check_oob(self.rect.x + self.speed, self.rect.y):
            self.rect.x += self.speed
        if keys[pygame.K_z] and check_oob(self.rect.x, self.rect.y - self.speed):
            self.rect.y -= self.speed
        if keys[pygame.K_s] and check_oob(self.rect.x, self.rect.y + self.speed):
            self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        if self.attacking:
            attack_position = (self.rect.right - 10, self.rect.top + 10 + self.rect.height // 2 - self.weapon_rect.height // 2)
            screen.blit(self.weapon_image, attack_position)

    def attack(self):
        self.attacking = True

    def updateArrows(self, screen):
        for arrow in self.arrows[:]:
            arrow.draw(screen)
            if not arrow.update():
                self.arrows.remove(arrow)

    def shootArrow(self):
        if self.current_weapon == "bow":
            direction = "right"
            new_arrow = Arrow(self.rect.right, self.rect.centery, direction)
            self.arrows.append(new_arrow)
            print(f"arrow shot from position: ({new_arrow.rect.x}, {new_arrow.rect.y})")

    def stop_attack(self):
        self.attacking = False

    def switchWeapon(self):
        if self.current_weapon == 'hammer':
            self.current_weapon = 'bow'
        else:
            self.current_weapon = 'hammer'
        self.weapon_image = self.weapons[self.current_weapon]
        self.weapon_rect = self.weapon_image.get_rect()
