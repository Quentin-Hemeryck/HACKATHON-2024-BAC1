import pygame

class Arrow:
    def __init__(self, x, y, direction, speed=1.9):
        self.image = pygame.image.load("assets/weapon_arrow.png")
        self.rect = self.image.get_rect(x=x, y=y)
        self.direction = direction
        self.speed = speed

    def update(self):
        # Arrow movement logic
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)
