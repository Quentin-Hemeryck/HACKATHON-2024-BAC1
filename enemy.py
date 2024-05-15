import pygame as p
import random

class Enemy:
    def __init__(self, images, speed, new_size, screen_width, screen_height):
        self.images = [p.transform.scale(p.image.load(img).convert_alpha(), new_size) for img in images]
        self.speed = speed
        self.new_size = new_size
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x, self.y = self.random_position()
        self.current_frame = 0
        self.animation_speed = 0.1
        self.frame_counter = 0
        self.mobHealth = 10
        self.rect = p.Rect(self.x, self.y, self.new_size[0], self.new_size[1])

    def random_position(self):
        return random.randint(0, self.screen_width - self.new_size[0]), random.randint(0, self.screen_height - self.new_size[1])

    def check_oob(self, x, y):
        return not (x < 0 or x + self.new_size[0] > self.screen_width or y < 0 or y + self.new_size[1] > self.screen_height)

    def draw(self, surface):
        if self.isAlive():
            frame = int(self.frame_counter) % len(self.images)
            surface.blit(self.images[frame], (self.x, self.y))
            self.frame_counter += self.animation_speed

    def update(self):
        move_x, move_y = random.choice([-1, 1]) * self.speed, random.choice([-1, 1]) * self.speed
        if self.check_oob(self.x + move_x, self.y + move_y):
            self.x += move_x
            self.y += move_y
        self.rect.x, self.rect.y = self.x, self.y

    def move_towards_player(self, player_x, player_y):
        dx, dy = player_x - self.x, player_y - self.y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance != 0:
            step_x = dx / distance * self.speed
            step_y = dy / distance * self.speed
            if self.check_oob(self.x + step_x, self.y + step_y):
                self.x += step_x
                self.y += step_y

    def applyDamage(self, damage):
        self.mobHealth -= damage
        if self.mobHealth <= 0:
            self.mobHealth = 0
            return True
        return False

    def isAlive(self):
        return self.mobHealth > 0

class Lizard(Enemy):
    def __init__(self, speed, screen_width, screen_height):
        super().__init__(["assets/big_demon_run_anim_f0.png", "assets/big_demon_run_anim_f1.png",
                          "assets/big_demon_run_anim_f2.png", "assets/big_demon_run_anim_f3.png"],
                         speed, new_size=(40, 80), screen_width=screen_width, screen_height=screen_height)

class Orc(Enemy):
    def __init__(self, speed, screen_width, screen_height):
        super().__init__(["assets/ogre_run_anim_f0.png", "assets/ogre_run_anim_f1.png",
                          "assets/ogre_run_anim_f2.png", "assets/ogre_run_anim_f3.png"],
                         speed, new_size=(50, 80), screen_width=screen_width, screen_height=screen_height)
