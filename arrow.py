import pygame

class Arrow:
    """
    Classe représentant une flèche tirée par le joueur.
    """
    def __init__(self, x, y, direction, image_path, speed=1.9):
        self.__original_image = pygame.image.load(image_path)
        self.__new_width = int(self.__original_image.get_width() * 1)
        self.__new_height = int(self.__original_image.get_height() * 1)

        self.__image = pygame.transform.scale(self.__original_image, (self.__new_width, self.__new_height))
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

    @rect.setter
    def rect(self, value):
        self.__rect = value

    def update(self):
        """
        Met à jour la position de la flèche.
        """
        if self.__direction == 'right':
            self.__rect.x += self.__speed
        elif self.__direction == 'left':
            self.__rect.x -= self.__speed
        elif self.__direction == 'up':
            self.__rect.y -= self.__speed
        elif self.__direction == 'down':
            self.__rect.y += self.__speed

        self.__distance += self.__speed
        print(f"Arrow moving to: ({self.__rect.x}, {self.__rect.y})")

        if self.__distance >= self.__max_distance:
            return False
        return True

    def draw(self, screen):
        """
        Dessine la flèche à l'écran.
        """
        screen.blit(self.__image, self.__rect)
