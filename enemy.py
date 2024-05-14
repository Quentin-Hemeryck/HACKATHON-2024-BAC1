import pygame as p
import random

class Enemy:
    def __init__(self, images, speed, new_size=(100, 100), screen_width=679, screen_height=676):
        self.__images = [p.transform.scale(p.image.load(img).convert_alpha(), new_size) for img in images]
        self.__speed = speed
        self.__new_size = new_size
        self.__screen_width = screen_width
        self.__screen_height = screen_height
        self.__x, self.__y = self.random_position()
        self.__current_frame = 0
        self.__animation_speed = 0.1
        self.__frame_counter = 0

    @property
    def images(self):
        return self.__images

    @property
    def speed(self):
        return self.__speed

    @property
    def new_size(self):
        return self.__new_size

    @property
    def screen_width(self):
        return self.__screen_width

    @property
    def screen_height(self):
        return self.__screen_height

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def current_frame(self):
        return self.__current_frame

    @property
    def animation_speed(self):
        return self.__animation_speed

    @property
    def frame_counter(self):
        return self.__frame_counter

    @images.setter
    def images(self,value):
        self.__images = value

    @speed.setter
    def speed(self,value):
        self.__speed = value

    @new_size.setter
    def new_size(self,value):
        self.__new_size = value

    @screen_width.setter
    def screen_width(self,value):
        self.__screen_width = value

    @screen_height.setter
    def screen_height(self,value):
        self.__screen_ = value

    @x.setter
    def x(self,value):
        self.__x = value

    @y.setter
    def y(self,value):
        self.__y = value

    @current_frame.setter
    def current_frame(self, value):
        self.__current_frame = value

    @animation_speed.setter
    def animation_speed(self, value):
        self.__animation_speed = value

    @frame_counter.setter
    def frame_counter(self, value):
        self.__frame_counter = value

    def random_position(self):
        return random.randint(0, self.__screen_width - self.__new_size[0]), random.randint(0, self.__screen_height - self.__new_size[1])

    def check_oob(self, x, y):
        """Check if the new position is out of the screen bounds."""
        if x < 0 or x + self.__new_size[0] > self.__screen_width or y < 0 or y + self.__new_size[1] > self.__screen_height:
            return False
        return True

    def draw(self, surface):
        frame = int(self.__frame_counter) % len(self.__images)
        surface.blit(self.__images[frame], (self.__x, self.y))
        self.__frame_counter += self.__animation_speed

    def update(self):
        move_x = random.choice([-1, 1]) * self.__speed
        move_y = random.choice([-1, 1]) * self.__speed
        if self.check_oob(self.x + move_x, self.y + move_y):
            self.__x += move_x
            self.__y += move_y

    def move_towards_player(self, player_x, player_y):
        dx = player_x - self.x
        dy = player_y - self.y
        distance = (dx ** 2 + dy ** 2) ** 0.5  # Calculer la distance euclidienne
        if distance != 0:
            step_x = dx / distance * self.speed
            step_y = dy / distance * self.speed
            if self.check_oob(self.x + step_x, self.y + step_y):
                self.x += step_x
                self.y += step_y
class Lizard(Enemy):
    def __init__(self, speed, screen_width=679, screen_height=676):
        lizard_frames = ["assets/big_demon_run_anim_f0.png", "assets/big_demon_run_anim_f1.png",
                         "assets/big_demon_run_anim_f2.png", "assets/big_demon_run_anim_f3.png"]
        super().__init__(lizard_frames, speed, new_size=(40, 80), screen_width=screen_width, screen_height=screen_height)

class Orc(Enemy):
    def __init__(self, speed, screen_width=679, screen_height=676):
        orc_frames = ["assets/ogre_run_anim_f0.png", "assets/ogre_run_anim_f1.png",
                      "assets/ogre_run_anim_f2.png", "assets/ogre_run_anim_f3.png"]
        super().__init__(orc_frames, speed, new_size=(50, 80), screen_width=screen_width, screen_height=screen_height)
