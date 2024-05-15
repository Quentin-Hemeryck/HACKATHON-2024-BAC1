import pygame
class Button:
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect(center=pos)
        self.text = font.render(text_input, True, base_color)
        self.text_rect = self.text.get_rect(center=pos)

    def update(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)
