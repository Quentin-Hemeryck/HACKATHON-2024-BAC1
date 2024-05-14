import pygame
import sys
from button import Button

pygame.init()

SCREEN_WIDTH = 980
SCREEN_HEIGHT = 600

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pause Menu")

BG = pygame.image.load("Assets/background.png")
BG = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))

def get_font(size):
    font_size = int(size * SCREEN_WIDTH / 1920)
    return pygame.font.Font("assets/font.ttf", font_size)

# Ajoutez la fonction main_menu ici
def pause_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("PAUSE MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.15))

        RESUME_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.36),
                             text_input="RESUME", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SAVE_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.54),
                               text_input="Save", font=get_font(75), base_color="#d7fcd4",hovering_color="White")

        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.72),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [RESUME_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if RESUME_BUTTON.checkForInput(MENU_MOUSE_POS):
                    return  # Revenir au jeu
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()