import pygame
from arrow import Arrow

class Player:
    def __init__(self, x, y, width, height, health=30):
        self.image = pygame.image.load('assets/elf_f_run_anim_f0.png')
        self.rect = self.image.get_rect(x=x, y=y)
        self.speed = 2
        self.weapons = {'hammer': 'path_to_hammer', 'bow': 'path_to_bow'}
        self.current_weapon = 'hammer'
        self.arrows = []
        self.health = health

    def move(self, keys):
        # Movement logic
        pass

    def draw(self, screen):
        # Drawing logic
        pass

    def updateArrows(self, screen):
        # Update arrows logic
        pass

# Additional classes like Lizard and Orc below
