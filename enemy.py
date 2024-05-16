"""
Module pour gérer les ennemis du jeu.
"""

import pygame as p
import random

class Enemy:
    """
    Classe de base représentant un ennemi.
    """
    def __init__(self, images, speed, new_size, screen_width, screen_height):
        self._images = [p.transform.scale(p.image.load(img).convert_alpha(), new_size) for img in images]
        self._speed = speed
        self._new_size = new_size
        self._screen_width = screen_width
        self._screen_height = screen_height
        self._x, self._y = self.random_position()
        self._current_frame = 0
        self._animation_speed = 0.1
        self._frame_counter = 0
        self._mobHealth = 50
        self._rect = p.Rect(self._x, self._y, self._new_size[0], self._new_size[1])

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, value):
        self._rect = value

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = value

    @property
    def mobHealth(self):
        return self._mobHealth

    @mobHealth.setter
    def mobHealth(self, value):
        self._mobHealth = value

    def random_position(self):
        """
        Génère une position aléatoire pour l'ennemi sur l'écran.
        """
        return random.randint(0, self._screen_width - self._new_size[0]), random.randint(0, self._screen_height - self._new_size[1])

    def check_oob(self, x, y):
        """
        Vérifie si une position est hors des limites de l'écran.
        """
        return not (x < 0 or x + self._new_size[0] > self._screen_width or y < 0 or y + self._new_size[1] > self._screen_height)

    def draw(self, surface):
        """
        Dessine l'ennemi à l'écran.
        """
        if self.isAlive():
            frame = int(self._frame_counter) % len(self._images)
            surface.blit(self._images[frame], (self._x, self._y))
            self._frame_counter += self._animation_speed

    def update(self):
        """
        Met à jour la position de l'ennemi de manière aléatoire.
        """
        move_x, move_y = random.choice([-1, 1]) * self._speed, random.choice([-1, 1]) * self._speed
        if self.check_oob(self._x + move_x, self._y + move_y):
            self._x += move_x
            self._y += move_y
        self._rect.x, self._rect.y = self._x, self._y

    def move_towards_player(self, player_x, player_y):
        """
        Déplace l'ennemi vers la position du joueur.
        """
        dx, dy = player_x - self._x, player_y - self._y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance != 0:
            step_x = dx / distance * self._speed
            step_y = dy / distance * self._speed
            if self.check_oob(self._x + step_x, self._y + step_y):
                self._x += step_x
                self._y += step_y

    def applyDamage(self, damage):
        """
        Inflige des dégâts à l'ennemi.
        """
        self._mobHealth -= damage
        if self._mobHealth <= 0:
            self._mobHealth = 0
            return True
        return False

    def isAlive(self):
        """
        Vérifie si l'ennemi est encore vivant.
        """
        return self._mobHealth > 0

class Lizard(Enemy):
    """
    Classe représentant un ennemi de type lézard.
    """
    def __init__(self, speed, screen_width, screen_height):
        """
        Initialise un nouvel ennemi de type lézard.

        """
        super().__init__(["assets/big_demon_run_anim_f0.png", "assets/big_demon_run_anim_f1.png",
                          "assets/big_demon_run_anim_f2.png", "assets/big_demon_run_anim_f3.png"],
                         speed, new_size=(40, 80), screen_width=screen_width, screen_height=screen_height)

class Orc(Enemy):
    """
    Classe représentant un ennemi de type orc.
    """
    def __init__(self, speed, screen_width, screen_height):
        """
        Initialise un nouvel ennemi de type orc.
        """
        super().__init__(["assets/ogre_run_anim_f0.png", "assets/ogre_run_anim_f1.png",
                          "assets/ogre_run_anim_f2.png", "assets/ogre_run_anim_f3.png"],
                         speed, new_size=(50, 80), screen_width=screen_width, screen_height=screen_height)

class Boss(Enemy):
    """
    Classe représentant un ennemi de type boss.
    """
    def __init__(self, speed, screen_width, screen_height):
        """
        Initialise un nouvel ennemi de type boss.
        """
        super().__init__(["assets/pumpkin_dude_run_anim_f0.png", "assets/pumpkin_dude_run_anim_f1.png",
                          "assets/pumpkin_dude_run_anim_f2.png", "assets/pumpkin_dude_run_anim_f3.png"],
                         speed, new_size=(80, 120), screen_width=screen_width, screen_height=screen_height)
        self._mobHealth = 125
        self._speed = speed + 0.4
