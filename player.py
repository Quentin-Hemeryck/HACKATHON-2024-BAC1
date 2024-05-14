import pygame
from arrow import *

class Player:
    def __init__(self, x, y, width=50, height=50, health=3):
        self.__original_image = pygame.image.load('assets/elf_f_run_anim_f0.png')
        self.__image = pygame.transform.scale(self.__original_image, (width, height))
        self.__rect = self.__image.get_rect()
        self.__rect.x = x
        self.__rect.y = y
        self.__speed = 2
        self.__attack_Frame = 0
        self.__weapons = {
            'hammer': pygame.image.load("assets/weapon_big_hammer.png"),
            "bow": pygame.image.load("assets/weapon_bow.png")
        }
        self.__currentWeapon = 'hammer'
        self.__weaponImage = self.__weapons[self.__currentWeapon]
        self.__weapon_rect = self.__weaponImage.get_rect()
        self.__attacking = False
        self.__arrows = []
        self.__health = health

    @property
    def rect(self):
        return self.__rect

    @property
    def image(self):
        return self.__image

    @property
    def speed(self):
        return self.__speed

    @property
    def weapons(self):
        return self.__weapons

    @property
    def weaponImage(self):
        return self.__weaponImage

    @property
    def weapon_rect(self):
        return self.__weapon_rect

    @property
    def arrows(self):
        return self.__arrows

    @property
    def health(self):
        return self.__health

    # Setters
    @rect.setter
    def rect(self, value):
        self.__rect = value

    @image.setter
    def image(self, value):
        self.__original_image = value
        self.__image = pygame.transform.scale(self.__original_image, (self.__rect.width, self.__rect.height))
        self.__rect = self.__image.get_rect()

    @speed.setter
    def speed(self, value):
        self.__speed = value

    @weapons.setter
    def weapons(self, value):
        self.__speed = value

    @weaponImage.setter
    def weaponImage(self, value):
        self.__weaponImage = value

    @weapon_rect.setter
    def weapon_rect(self, value):
        self.__weapon_rect = value

    @arrows.setter
    def arrows(self, value):
        self.__arrows = value

    @health.setter
    def health(self, value):
        self.__health = value

    def move(self, key):

        def check_oob(x, y):
            """
            Check collision murs
            """
            limit_x = [18, 629]
            limit_y = [2, 557]
            if x < limit_x[0] or x > limit_x[1]:
                return False
            if y < limit_y[0] or y > limit_y[1]:
                return False

            return True

        if key[pygame.K_q]:
            if check_oob(self.__rect.x - self.__speed, self.__rect.y):
                self.__rect.x -= self.__speed
        if key[pygame.K_d]:
            if check_oob(self.__rect.x + self.__speed, self.__rect.y):
                self.__rect.x += self.__speed
        if key[pygame.K_z]:
            if check_oob(self.__rect.x, self.__rect.y - self.__speed):
                self.__rect.y -= self.__speed
        if key[pygame.K_s]:
            if check_oob(self.__rect.x, self.__rect.y + self.__speed):
                self.__rect.y += self.__speed

    def draw(self, screen):
        screen.blit(self.__image, self.__rect)
        if self.__attacking:
            attack_position = (
            self.__rect.right - 10, self.__rect.top + 10 + self.__rect.height // 2 - self.__weapon_rect.height // 2)
            screen.blit(self.__weaponImage, attack_position
                        )

    def attack(self):
        self.__attacking = True

    def updateArrows(self, screen):
        for arrows in self.__arrows[:]:
            if not arrows.update():
                self.__arrows.remove(arrows)
            else:
                arrows.draw(screen)
    def shootArrow(self):
        if self.__currentWeapon =="bow":
            direction = "right"
            new_arrow= Arrow(self.__rect.right, self.__rect.centery, direction)
            self.__arrows.append(new_arrow)
            print(f"arrow shot from position: ({new_arrow.rect.x}, {new_arrow.rect.y})")
    def stop_attack(self):
        self.__attacking = False

    def switchWeapon(self):
        self.__currentWeapon = "bow" if self.__currentWeapon == 'hammer' else 'hammer'
        self.__weaponImage = self.__weapons[self.__currentWeapon]
        self.__weapon_rect = self.__weaponImage.get_rect()
