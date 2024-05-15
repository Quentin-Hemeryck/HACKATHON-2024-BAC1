import pygame

class Arrow:
    def __init__(self, x, y, direction, speed=1.9):
        originalImage =pygame.image.load("assets/weapon_arrow.png")
        newWidth = int(originalImage.get_width()*1)
        newHeight = int(originalImage.get_height()*1)

        self.__image = pygame.transform.scale(originalImage, (newWidth, newHeight))
        self.__rect = self.__image.get_rect()
        self.__rect.x = x
        self.__rect.y = y
        self.__direction = direction
        self.__speed = speed
        self.__distance = 0
        self.__max_distance = 250

    @property
    def rect(self):
        return self.__rect

    @property
    def image(self):
        return self.__image

    @property
    def direction(self):
        return self.__direction

    @property
    def speed(self):
        return self.__speed

    @property
    def distance(self):
        return self.__distance

    @property
    def max_distance(self):
        return self.__max_distance

    @rect.setter
    def rect(self, value):
        self.__rect = value

    @image.setter
    def image(self, value):
        self.__image = value

    @direction.setter
    def direction(self, value):
        self.__direction = value

    @speed.setter
    def speed(self, value):
        self.__speed = value

    @distance.setter
    def distance(self, value):
        self.__distance = value

    @max_distance.setter
    def max_distance(self, value):
        self.__max_distance = value

    def update(self):
        if self.__direction == 'right':
            self.__rect.x += self.__speed
        elif self.__direction == 'left':
            self.__rect.x -= self.__speed
        elif self.__direction == 'up':
            self.__rect.y -= self.__speed
        elif self.__direction == 'down':
            self.__rect.y += self.__speed

        self.__distance += self.__speed
        print(f"Arrow moving to:({self.__rect.x},{self.__rect.y})")

        if self.__distance >= self.__max_distance:
            return False
        return True

    def draw(self, screen):
        screen.blit(self.__image, self.__rect)






